import sys
import os

from antlr4 import *

from PlSqlLexer             import PlSqlLexer
from PlSqlParser            import PlSqlParser
from PlSql2PostgreListener  import PlSql2PostgreListener
from CaseChangingStream     import CaseChangingStream

DEFAULT_FILE_NAME = '.\work\output.postgre.sql'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding = 'utf-8')
        file_name, file_ext = os.path.splitext(sys.argv[1])
        output_file = file_name + '.postgre' + file_ext
    else:
        input_stream = InputStream(sys.stdin.readline())
        output_file = DEFAULT_FILE_NAME
    
    upper_stream = CaseChangingStream(input_stream, True)
    lexer = PlSqlLexer(upper_stream)
    tokens = CommonTokenStream(lexer)
    parser = PlSqlParser(tokens)
    tree = parser.sql_script()

    listener = PlSql2PostgreListener(tokens)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    
    f = open(output_file, 'wb')
    out_stream = listener.rewriter.getDefaultText().encode('utf-8')
    f.write(out_stream)
    f.close()
