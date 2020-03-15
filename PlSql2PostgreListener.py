from antlr4                     import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from PlSqlParserListener        import PlSqlParserListener
from PlSqlParser                import PlSqlParser
from PlSqlLexer                 import PlSqlLexer


class PlSql2PostgreListener(PlSqlParserListener):

    # need rewriter to change token stream
    def __init__(self, tokens:TokenStream):
        self.tokens = tokens
        self.rewriter = TokenStreamRewriter(tokens)
    
    # change all remark comments to -- comments    
    def replaceEveryRemark(self):
        for token in self.tokens.tokens:
            if token.channel == PlSqlLexer.REMCOMMENTS:
                txt = token.text
                if txt[:6].upper() == 'REMARK':
                    new_txt = '--' + txt[6:]
                else:
                    new_txt = '--' + txt[3:]
                self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#sql_script.
    def exitSql_script(self, ctx:PlSqlParser.Sql_scriptContext):
        self.replaceEveryRemark()

    # Enter a parse tree produced by PlSqlParser#sql_plus_command.
    def enterSql_plus_command(self, ctx:PlSqlParser.Sql_plus_commandContext):
        token = ctx.start
        txt = token.text

        # change / command to nothing
        if txt == '/':
            new_txt = ''
            self.rewriter.replaceSingleToken(token, new_txt)
        # change exit command to \q
        elif txt.upper() == 'EXIT':
            new_txt = r'\q'
            self.rewriter.replaceSingleToken(token, new_txt)
        # change prompt command to \echo
        elif txt[:6].upper() == 'PROMPT':
            new_txt = r'\echo' + txt[6:]
            self.rewriter.replaceSingleToken(token, new_txt)
        elif txt[:3].upper() == 'PRO':
            new_txt = r'\echo' + txt[3:]
            self.rewriter.replaceSingleToken(token, new_txt)
        # change show errors command to \errverbose
        elif txt.upper() == 'SHOW':
            for child in ctx.children:
                if isinstance(child, TerminalNode):
                    if child.symbol == ctx.start:
                        new_txt = r'\errverbose'
                    else:
                        new_txt = ''
                    self.rewriter.replaceSingleToken(child.symbol, new_txt)
                    
        
    # Enter a parse tree produced by PlSqlParser#whenever_command.
    def enterWhenever_command(self, ctx:PlSqlParser.Whenever_commandContext):
        token = ctx.start
        txt = token.text

        # comment whenever command
        new_txt = '-- ' + txt
        self.rewriter.replaceSingleToken(token, new_txt)
                