import textwrap
from pathlib import Path
from ..parser import ast
from .utils import CompileError
from .utils import InternalError
from .utils import get_import_from_info
from .base import TypeVisitor
from .base import INTEGER_TYPES
from .base import Context
from .base import BaseVisitor
from .base import indent
from .base import indent_lines
from .base import has_docstring
from .base import mys_to_cpp_type_param
from .base import BodyCheckVisitor
from .base import make_name
from .base import format_parameters
from .base import format_return_type
from .base import format_method_name
from .base import mys_to_cpp_type
from .definitions import is_method

def default_value(cpp_type):
    if cpp_type in INTEGER_TYPES:
        return '0'
    elif cpp_type in ['f32', 'f64']:
        return '0.0'
    elif cpp_type == 'Bool':
        return 'Bool(false)'
    elif cpp_type == 'String':
        return 'String()'
    elif cpp_type == 'Char':
        return 'Char()'
    else:
        return 'nullptr'

def create_class_init(class_name, member_names, member_types):
    params = []
    body = []

    for member_name, member_type in zip(member_names, member_types):
        if member_name.startswith('_'):
            value = default_value(member_type)
            body.append(f'this->{make_name(member_name)} = {value};')
        else:
            params.append(f'{member_type} {make_name(member_name)}')
            body.append(f'this->{make_name(member_name)} = {make_name(member_name)};')

    params = ', '.join(params)

    return [
        f'{class_name}::{class_name}({params})',
        '{'
    ] + indent_lines(body) + [
        '}'
    ]

def create_class_del(class_name):
    return [
        f'{class_name}::~{class_name}()',
        '{',
        '}'
    ]

def create_class_str(class_name):
    return [
        f'String {class_name}::__str__() const',
        '{',
        '    std::stringstream ss;',
        '    __format__(ss);',
        '    return String(ss.str().c_str());',
        '}'
    ]

def create_class_format(class_name, member_names):
    members = []

    for name in member_names[:-1]:
        members.append(f'    os << "{name}=" << this->{make_name(name)} << ", ";')

    if member_names:
        name = member_names[-1]
        members.append(f'    os << "{name}=" << this->{make_name(name)};')

    return [
        f'void {class_name}::__format__(std::ostream& os) const',
        '{',
        f'    os << "{class_name}(";'
    ] + members + [
        '    os << ")";',
        '}'
    ]

def create_enum_from_integer(enum):
    code = [
        f'{enum.type} enum_{enum.name}_from_value({enum.type} value)',
        '{',
        '    switch (value) {'
    ]

    for name, value in enum.members:
        code += [
            f'    case {value}:',
            f'        return ({enum.type}){enum.name}::{name};'
        ]

    code += [
        '    default:',
        '        throw ValueError("bad enum value");',
        '    }',
        '}'
    ]

    return code

class SourceVisitor(ast.NodeVisitor):

    def __init__(self,
                 namespace,
                 module_levels,
                 module_hpp,
                 filename,
                 source_lines,
                 definitions,
                 module_definitions,
                 skip_tests):
        self.module_levels = module_levels
        self.source_lines = source_lines
        self.module_hpp = module_hpp
        self.filename = filename
        self.skip_tests = skip_tests
        self.namespace = namespace
        self.forward_declarations = []
        self.add_package_main = False
        self.before_namespace = []
        self.context = Context(module_levels)
        self.definitions = definitions
        self.module_definitions = module_definitions
        self.enums = []

        for name, functions in module_definitions.functions.items():
            self.context.define_function(
                name,
                self.context.make_full_name_this_module(name),
                functions)

        for name, trait_definitions in module_definitions.traits.items():
            self.context.define_trait(name,
                                      self.context.make_full_name_this_module(name),
                                      trait_definitions)

        for name, class_definitions in module_definitions.classes.items():
            self.context.define_class(name,
                                      self.context.make_full_name_this_module(name),
                                      class_definitions)

        for enum in module_definitions.enums.values():
            self.enums += self.visit_enum(enum)
            self.enums += create_enum_from_integer(enum)

    def define_parameters(self, args):
        for param, node in args:
            self.context.define_local_variable(param.name, param.type, node)

    def visit_AnnAssign(self, node):
        return AnnAssignVisitor(self.source_lines,
                                self.context,
                                self.source_lines).visit(node)

    def visit_Module(self, node):
        body = []

        for item in node.body:
            body += self.visit(item)

        for name, definitions in self.module_definitions.classes.items():
            body += self.visit_class_definition(name, definitions)

        for functions in self.module_definitions.functions.values():
            for function in functions:
                body += self.visit_function_defaults(function)
                body += self.visit_function_definition(function)

        return '\n'.join([
            '// This file was generated by mys. DO NOT EDIT!!!',
            '#include "mys.hpp"',
            f'#include "{self.module_hpp}"'
        ] + self.before_namespace + [
            f'namespace {self.namespace}',
            '{'
        ] + self.forward_declarations
          + self.enums
          + [constant[1] for constant in self.context.constants.values()]
          + body + [
            '}'
        ] + self.main())

    def main(self):
        if self.add_package_main:
            return [
                'void package_main(int argc, const char *argv[])',
                '{',
                f'    {self.namespace}::main(argc, argv);',
                '}'
            ]
        else:
            return []

    def visit_ImportFrom(self, node):
        module, name, asname = get_import_from_info(node, self.module_levels)
        imported_module = self.definitions.get(module)

        if name.startswith('_'):
            raise CompileError(f"cannot import private definition '{name}'", node)

        if asname is None:
            asname = name

        full_name = f'{module}.{name}'

        if name in imported_module.variables:
            self.context.define_global_variable(
                asname,
                full_name,
                imported_module.variables[name].type,
                node)
        elif name in imported_module.functions:
            for function in imported_module.functions[name]:
                if function.returns is None:
                    continue
                if '.' in function.returns:
                    n = '.'.join(function.returns.split('.')[:-1])
                    k = function.returns.split('.')[-1]
                    im = self.definitions.get(n)

                    if k in im.classes:
                        self.context.define_class(function.returns,
                                                  function.returns,
                                                  im.classes[k])

            self.context.define_function(asname,
                                         full_name,
                                         imported_module.functions[name])
        elif name in imported_module.classes:
            for methods in imported_module.classes[name].methods.values():
                for method in methods:
                    if method.returns is None:
                        continue
                    if '.' in method.returns:
                        n = '.'.join(method.returns.split('.')[:-1])
                        k = method.returns.split('.')[-1]
                        im = self.definitions.get(n)

                        if k in im.classes:
                            self.context.define_class(method.returns,
                                                      method.returns,
                                                      im.classes[k])

            self.context.define_class(asname,
                                      full_name,
                                      imported_module.classes[name])
        elif name in imported_module.traits:
            self.context.define_trait(asname,
                                      full_name,
                                      imported_module.traits[name])
        else:
            raise CompileError(
                f"imported module '{module}' does not contain '{name}'",
                node)

        return []

    def visit_enum(self, enum):
        members = [
            f"    {name} = {value},"
            for name, value in enum.members
        ]

        self.context.define_enum(enum.name,
                                 self.context.make_full_name_this_module(enum.name),
                                 enum.type)

        return [
            f'enum class {enum.name} : {enum.type} {{'
        ] + members + [
            '};'
        ]

    def visit_ClassDef(self, node):
        return []

    def visit_method_defaults(self, method, class_name):
        code = []

        for param, default in method.args:
            if default is None:
                continue

            cpp_type = mys_to_cpp_type(param.type, self.context)
            body = BaseVisitor(self.source_lines,
                               self.context,
                               self.filename).visit_value_check_type(default, param.type)

            if method.name == '__init__':
                method_name = class_name
            else:
                method_name = method.name

            code += [
                f'{cpp_type} {class_name}_{method_name}_{param.name}_default()',
                '{',
                f'    return {body};',
                '}'
            ]

        return code

    def visit_class_methods_definition(self,
                                       class_name,
                                       method_names,
                                       methods_definitions):
        body = []

        for method in methods_definitions:
            body += self.visit_method_defaults(method, class_name)
            self.context.push()
            self.context.define_local_variable(
                'self',
                self.context.make_full_name_this_module(class_name),
                method.node.args.args[0])
            self.define_parameters(method.args)
            method_names.append(method.name)
            method_name = format_method_name(method, class_name)
            parameters = format_parameters(method.args, self.context)
            self.context.return_mys_type = method.returns

            if method_name == class_name:
                body.append(f'{class_name}::{method_name}({parameters})')
            else:
                return_cpp_type = format_return_type(method.returns, self.context)
                body.append(f'{return_cpp_type} {class_name}::{method_name}({parameters})')

            body.append('{')
            body_iter = iter(method.node.body)

            if has_docstring(method.node, self.source_lines):
                next(body_iter)

            for item in body_iter:
                BodyCheckVisitor().visit(item)
                body.append(indent(BodyVisitor(self.source_lines,
                                               self.context,
                                               self.filename).visit(item)))

            body.append('}')
            self.context.pop()

        return body

    def visit_class_definition(self, class_name, definitions):
        member_cpp_types = []
        member_names = []
        method_names = []
        body = []

        for member in definitions.members.values():
            if not self.context.is_type_defined(member.type):
                raise CompileError(f"undefined type '{member.type}'",
                                   member.node.annotation)

            member_cpp_types.append(mys_to_cpp_type_param(member.type, self.context))
            member_names.append(member.name)

        for methods in definitions.methods.values():
            body += self.visit_class_methods_definition(class_name,
                                                        method_names,
                                                        methods)

        if '__init__' not in method_names:
            body += create_class_init(class_name,
                                      member_names,
                                      member_cpp_types)

        if '__del__' not in method_names:
            body += create_class_del(class_name)

        if '__str__' not in method_names:
            body += create_class_str(class_name)

        body += create_class_format(class_name, member_names)

        return body

    def visit_FunctionDef(self, node):
        return []

    def visit_function_defaults(self, function):
        code = []

        for param, default in function.args:
            if default is None:
                continue

            cpp_type = mys_to_cpp_type(param.type, self.context)
            body = BaseVisitor(self.source_lines,
                               self.context,
                               self.filename).visit_value_check_type(default, param.type)
            code += [
                f'{cpp_type} {function.name}_{param.name}_default()',
                '{',
                f'    return {body};',
                '}'
            ]

        return code

    def visit_function_definition(self, function):
        self.context.push()
        self.define_parameters(function.args)
        function_name = function.node.name
        parameters = format_parameters(function.args, self.context)
        return_cpp_type = format_return_type(function.returns, self.context)
        self.context.return_mys_type = function.returns
        body = []
        body_iter = iter(function.node.body)

        if has_docstring(function.node, self.source_lines):
            next(body_iter)

        for item in body_iter:
            BodyCheckVisitor().visit(item)
            body.append(indent(BodyVisitor(self.source_lines,
                                           self.context,
                                           self.filename).visit(item)))

        if function_name == 'main':
            self.add_package_main = True

            if return_cpp_type != 'void':
                raise CompileError("main() must not return any value", function.node)

            if parameters not in ['const SharedList<String>& argv', 'void']:
                raise CompileError("main() takes 'argv: [string]' or no arguments",
                                   function.node)

            if parameters == 'void':
                body = [
                    '    (void)__argc;',
                    '    (void)__argv;'
                ] + body
            else:
                body = ['    auto argv = create_args(__argc, __argv);'] + body

            parameters = 'int __argc, const char *__argv[]'

        prototype = f'{return_cpp_type} {function_name}({parameters})'

        if function.is_test:
            if self.skip_tests:
                code = []
            else:
                parts = Path(self.module_hpp).parts
                full_test_name = list(parts[1:-1])
                full_test_name += [parts[-1].split('.')[0]]
                full_test_name += [function_name]
                full_test_name = '::'.join([part for part in full_test_name])
                code = [
                    '#if defined(MYS_TEST)',
                    f'static {prototype}',
                    '{'
                ] + body + [
                    '}',
                    f'static Test mys_test_{function_name}("{full_test_name}", '
                    f'{function_name});',
                    '#endif'
                ]
        else:
            self.forward_declarations.append(prototype + ';')
            code = [
                prototype,
                '{'
            ] + body + [
                '}'
            ]

        self.context.pop()

        return code

    def visit_Expr(self, node):
        return self.visit(node.value) + [';']

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            if node.value.startswith('mys-embedded-c++-before-namespace'):
                self.before_namespace += [
                    '/* mys-embedded-c++-before-namespace start */',
                    textwrap.dedent(node.value[33:]).strip(),
                    '/* mys-embedded-c++-before-namespace stop */'
                ]
                return []
            elif node.value.startswith('mys-embedded-c++'):
                return [
                    '/* mys-embedded-c++ start */',
                    '',
                    textwrap.dedent(node.value[17:]).strip(),
                    '',
                    '/* mys-embedded-c++ stop */']

        raise CompileError("syntax error", node)

    def generic_visit(self, node):
        raise InternalError("unhandled node", node)

class BodyVisitor(BaseVisitor):
    pass

class AnnAssignVisitor(BaseVisitor):

    def visit_AnnAssign(self, node):
        target, mys_type, code = self.visit_ann_assign(node)
        self.context.define_global_variable(
            target,
            self.context.make_full_name_this_module(target),
            mys_type,
            node.target)

        return [code]
