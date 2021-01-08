import shutil
import os
from .utils import build_and_test_module
from .utils import TestCase
from .utils import transpile_source
from .utils import remove_ansi


class Test(TestCase):

    def setUp(self):
        os.makedirs('tests/build', exist_ok=True)

    def test_string(self):
        build_and_test_module('string')

    def test_iterate_over_range_string(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    for i in range("a"):\n'
                             '        print(i)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        for i in range("a"):\n'
            '                       ^\n'
            "CompileError: parameter type must be an integer, not 'string'\n")

    def test_iterate_over_enumerate_string(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    for i, j in enumerate(range(2), ""):\n'
                             '        print(i)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        for i, j in enumerate(range(2), ""):\n'
            '                                        ^\n'
            "CompileError: initial value must be an integer, not 'string'\n")

    def test_global_string(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('"Hello!"\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    "Hello!"\n'
            '    ^\n'
            "CompileError: syntax error\n")

    def test_string_member_access(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo(v: string):\n'
                             '    v.a = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        v.a = 1\n'
            '        ^\n'
            "CompileError: 'string' has no member 'a'\n")

    def test_string_to_utf8_too_many_parameters(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    "".to_utf8(1)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        "".to_utf8(1)\n'
            "        ^\n"
            'CompileError: expected 0 parameters, got 1\n')

    def test_string_upper_too_many_parameters(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    "".upper(1)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        "".upper(1)\n'
            "        ^\n"
            'CompileError: expected 0 parameters, got 1\n')

    def test_string_lower_too_many_parameters(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    "".lower(1)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        "".lower(1)\n'
            "        ^\n"
            'CompileError: expected 0 parameters, got 1\n')

    def test_string_bad_method(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    "".foobar()\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        "".foobar()\n'
            "        ^\n"
            'CompileError: string method not implemented\n')

    def test_positive_string(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    print(+"hi")\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        print(+"hi")\n'
            '              ^\n'
            "CompileError: unary '+' can only operate on numbers\n")
