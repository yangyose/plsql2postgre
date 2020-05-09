"""Provide main module of plsql2postgre.

    [class]PlSql2Postgre - Run converter from oracle to postgreSQL.
    [routine]main - Provide the main entry for converter.
"""
import sys
import os

from antlr4                 import CommonTokenStream, FileStream, InputStream, ParseTreeWalker
if __name__ is not None and "." in __name__:
    from .PlSqlLexer            import PlSqlLexer
    from .PlSqlParser           import PlSqlParser
    from .plsql2postgrelistener import PlSql2PostgreListener
    from .casechangingstream    import CaseChangingStream
else:
    from PlSqlLexer             import PlSqlLexer
    from PlSqlParser            import PlSqlParser
    from plsql2postgrelistener  import PlSql2PostgreListener
    from casechangingstream     import CaseChangingStream

DEFAULT_ENCODING = 'ansi'
DEFAULT_FILE_NAME = r'.\tests\data\output.postgre.sql'

class PlSql2Postgre:
    """Run converter from oracle to postgreSQL.

        [method]run - Run converter from oracle to postgreSQL.
    """
    def __init__(self, stream):
        """Init the properties of class.

            [argument]stream - Set the original oracle script string.
        """
        self.__input_stream = stream

    def run(self):
        """Run converter from oracle to postgreSQL and return valid postgreSQL script."""
        #Parse the original oracle script.
        upper_stream = CaseChangingStream(self.__input_stream, True)
        lexer = PlSqlLexer(upper_stream)
        tokens = CommonTokenStream(lexer)
        parser = PlSqlParser(tokens)
        tree = parser.sql_script()
        #Traverse the AST and generate postgreSQL script.
        listener = PlSql2PostgreListener(tokens)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.rewriter.getDefaultText().encode(DEFAULT_ENCODING)

def main():
    """The main entry for converter."""
    #Get input oracle script string.
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding=DEFAULT_ENCODING)
        file_name, file_ext = os.path.splitext(sys.argv[1])
        output_file = file_name + '.postgre' + file_ext
    else:
        input_stream = InputStream(sys.stdin.readline())
        output_file = DEFAULT_FILE_NAME
    #Convert to postgreSQL script and write to output file.
    f_out = open(output_file, 'wb')
    converter = PlSql2Postgre(input_stream)
    f_out.write(converter.run())
    f_out.close()

if __name__ == '__main__':
    main()
