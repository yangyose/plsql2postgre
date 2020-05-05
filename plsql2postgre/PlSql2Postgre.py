import sys
import os

from antlr4                                 import CommonTokenStream, ParseTreeWalker, FileStream, InputStream
from plsql2postgre.PlSqlLexer               import PlSqlLexer
from plsql2postgre.PlSqlParser              import PlSqlParser
from plsql2postgre.PlSql2PostgreListener    import PlSql2PostgreListener
from plsql2postgre.CaseChangingStream       import CaseChangingStream

DEFAULT_ENCODING = 'ansi'
DEFAULT_FILE_NAME = '.\work\output.postgre.sql'

class PlSql2Postgre:

    def __init__(self, stream):
        self.__input_stream = stream

    def run(self):
        upper_stream = CaseChangingStream(self.__input_stream, True)
        lexer = PlSqlLexer(upper_stream)
        tokens = CommonTokenStream(lexer)
        parser = PlSqlParser(tokens)
        tree = parser.sql_script()

        listener = PlSql2PostgreListener(tokens)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.rewriter.getDefaultText().encode(DEFAULT_ENCODING)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding = DEFAULT_ENCODING)
        file_name, file_ext = os.path.splitext(sys.argv[1])
        output_file = file_name + '.postgre' + file_ext
    else:
        input_stream = InputStream(sys.stdin.readline())
        output_file = DEFAULT_FILE_NAME
    
    f = open(output_file, 'wb')
    converter = PlSql2Postgre(input_stream)   
    f.write(converter.run())
    f.close()
