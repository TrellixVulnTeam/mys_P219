"""
    pygments.formatters._mapping
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Formatter mapping definitions. This file is generated by itself. Everytime
    you change something on a builtin formatter definition, run this script from
    the formatters folder to update it.

    Do not alter the FORMATTERS dictionary by hand.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

FORMATTERS = {
    'BBCodeFormatter': ('pygments.formatters.bbcode', 'BBCode', ('bbcode', 'bb'), (), 'Format tokens with BBcodes. These formatting codes are used by many bulletin boards, so you can highlight your sourcecode with pygments before posting it there.'),
    'BmpImageFormatter': ('pygments.formatters.img', 'img_bmp', ('bmp', 'bitmap'), ('*.bmp',), 'Create a bitmap image from source code. This uses the Python Imaging Library to generate a pixmap from the source code.'),
    'GifImageFormatter': ('pygments.formatters.img', 'img_gif', ('gif',), ('*.gif',), 'Create a GIF image from source code. This uses the Python Imaging Library to generate a pixmap from the source code.'),
    'HtmlFormatter': ('pygments.formatters.html', 'HTML', ('html',), ('*.html', '*.htm'), "Format tokens as HTML 4 ``<span>`` tags within a ``<pre>`` tag, wrapped in a ``<div>`` tag. The ``<div>``'s CSS class can be set by the `cssclass` option."),
    'IRCFormatter': ('pygments.formatters.irc', 'IRC', ('irc', 'IRC'), (), 'Format tokens with IRC color sequences'),
    'ImageFormatter': ('pygments.formatters.img', 'img', ('img', 'IMG', 'png'), ('*.png',), 'Create a PNG image from source code. This uses the Python Imaging Library to generate a pixmap from the source code.'),
    'JpgImageFormatter': ('pygments.formatters.img', 'img_jpg', ('jpg', 'jpeg'), ('*.jpg',), 'Create a JPEG image from source code. This uses the Python Imaging Library to generate a pixmap from the source code.'),
    'LatexFormatter': ('pygments.formatters.latex', 'LaTeX', ('latex', 'tex'), ('*.tex',), 'Format tokens as LaTeX code. This needs the `fancyvrb` and `color` standard packages.'),
    'NullFormatter': ('pygments.formatters.other', 'Text only', ('text', 'null'), ('*.txt',), 'Output the text unchanged without any formatting.'),
    'PangoMarkupFormatter': ('pygments.formatters.pangomarkup', 'Pango Markup', ('pango', 'pangomarkup'), (), 'Format tokens as Pango Markup code. It can then be rendered to an SVG.'),
    'RawTokenFormatter': ('pygments.formatters.other', 'Raw tokens', ('raw', 'tokens'), ('*.raw',), 'Format tokens as a raw representation for storing token streams.'),
    'RtfFormatter': ('pygments.formatters.rtf', 'RTF', ('rtf',), ('*.rtf',), 'Format tokens as RTF markup. This formatter automatically outputs full RTF documents with color information and other useful stuff. Perfect for Copy and Paste into Microsoft(R) Word(R) documents.'),
    'SvgFormatter': ('pygments.formatters.svg', 'SVG', ('svg',), ('*.svg',), 'Format tokens as an SVG graphics file.  This formatter is still experimental. Each line of code is a ``<text>`` element with explicit ``x`` and ``y`` coordinates containing ``<tspan>`` elements with the individual token styles.'),
    'Terminal256Formatter': ('pygments.formatters.terminal256', 'Terminal256', ('terminal256', 'console256', '256'), (), 'Format tokens with ANSI color sequences, for output in a 256-color terminal or console.  Like in `TerminalFormatter` color sequences are terminated at newlines, so that paging the output works correctly.'),
    'TerminalFormatter': ('pygments.formatters.terminal', 'Terminal', ('terminal', 'console'), (), 'Format tokens with ANSI color sequences, for output in a text console. Color sequences are terminated at newlines, so that paging the output works correctly.'),
    'TerminalTrueColorFormatter': ('pygments.formatters.terminal256', 'TerminalTrueColor', ('terminal16m', 'console16m', '16m'), (), 'Format tokens with ANSI color sequences, for output in a true-color terminal or console.  Like in `TerminalFormatter` color sequences are terminated at newlines, so that paging the output works correctly.'),
    'TestcaseFormatter': ('pygments.formatters.other', 'Testcase', ('testcase',), (), 'Format tokens as appropriate for a new testcase.')
}

if __name__ == '__main__':  # pragma: no cover
    import os
    import sys

    # lookup formatters
    found_formatters = []
    imports = []
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from pygments.util import docstring_headline

    for root, dirs, files in os.walk('.'):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = 'pygments.formatters%s.%s' % (
                    root[1:].replace('/', '.'), filename[:-3])
                print(module_name)
                module = __import__(module_name, None, None, [''])
                for formatter_name in module.__all__:
                    formatter = getattr(module, formatter_name)
                    found_formatters.append(
                        '%r: %r' % (formatter_name,
                                    (module_name,
                                     formatter.name,
                                     tuple(formatter.aliases),
                                     tuple(formatter.filenames),
                                     docstring_headline(formatter))))
    # sort them to make the diff minimal
    found_formatters.sort()

    # extract useful sourcecode from this file
    with open(__file__) as fp:
        content = fp.read()
        # replace crnl to nl for Windows.
        #
        # Note that, originally, contributers should keep nl of master
        # repository, for example by using some kind of automatic
        # management EOL, like `EolExtension
        #  <https://www.mercurial-scm.org/wiki/EolExtension>`.
        content = content.replace("\r\n", "\n")
    header = content[:content.find('FORMATTERS = {')]
    footer = content[content.find("if __name__ == '__main__':"):]

    # write new file
    with open(__file__, 'w') as fp:
        fp.write(header)
        fp.write('FORMATTERS = {\n    %s\n}\n\n' % ',\n    '.join(found_formatters))
        fp.write(footer)

    print ('=== %d formatters processed.' % len(found_formatters))
