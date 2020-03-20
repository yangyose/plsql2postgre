from antlr4                     import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from PlSqlParserListener        import PlSqlParserListener
from PlSqlParser                import PlSqlParser
from PlSqlLexer                 import PlSqlLexer


class PlSql2PostgreListener(PlSqlParserListener):
    DATA_TYPE = {   'BFILE'         :'BYTEA',
                    'BINARY_DOUBLE' :'DOUBLE PRECISION',
                    'BINARY_FLOAT'  :'DOUBLE PRECISION',
                    'BINARY_INTEGER':'INTEGER',
                    'BLOB'          :'BYTEA',
                    'CLOB'          :'TEXT',
                    'DATE'          :'TIMESTAMP',
                    'DEC'           :'DECIMAL',
                    'FLOAT'         :'DOUBLE PRECISION',
                    'INT'           :'INTEGER',
                    'LONG'          :'TEXT',
                    'NCHAR'         :'CHAR',
                    'NCLOB'         :'TEXT',
                    'NVARCHAR2'     :'VARCHAR',
                    'NUMBER'        :'NUMERIC',
                    'PLS_INTEGER'   :'INTEGER',
                    'RAW'           :'BYTEA',
                    'ROWID'         :'OID',
                    'VARCHAR2'      :'VARCHAR'
                }

    # need rewriter to change token stream
    def __init__(self, tokens:TokenStream):
        self.tokens = tokens
        self.rewriter = TokenStreamRewriter(tokens)
    
    # convert all remark comments to -- comments    
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

    # Exit a parse tree produced by PlSqlParser#sql_plus_command.
    def exitSql_plus_command(self, ctx:PlSqlParser.Sql_plus_commandContext):
        token = ctx.start
        txt = token.text

        # convert / command to nothing
        if txt == '/':
            new_txt = ''
            self.rewriter.replaceSingleToken(token, new_txt)
        # convert exit command to \q
        elif txt.upper() == 'EXIT':
            new_txt = r'\q'
            self.rewriter.replaceSingleToken(token, new_txt)
        # convert prompt command to \echo
        elif txt[:6].upper() == 'PROMPT':
            new_txt = r'\echo' + txt[6:]
            self.rewriter.replaceSingleToken(token, new_txt)
        elif txt[:3].upper() == 'PRO':
            new_txt = r'\echo' + txt[3:]
            self.rewriter.replaceSingleToken(token, new_txt)
        # convert show errors command to \errverbose
        elif txt.upper() == 'SHOW':
            for child in ctx.children:
                if isinstance(child, TerminalNode):
                    if child.symbol == ctx.start:
                        new_txt = r'\errverbose'
                    else:
                        new_txt = ''
                    self.rewriter.replaceSingleToken(child.symbol, new_txt)
                    
        
    # Exit a parse tree produced by PlSqlParser#whenever_command.
    def exitWhenever_command(self, ctx:PlSqlParser.Whenever_commandContext):
        token = ctx.start
        txt = token.text

        # comment whenever command
        new_txt = '-- ' + txt
        self.rewriter.replaceSingleToken(token, new_txt)
        
    # Exit a parse tree produced by PlSqlParser#set_command.
    def exitSet_command(self, ctx:PlSqlParser.Set_commandContext):
        token = ctx.start

        # convert set command to \set
        new_txt = r'\set'
        self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#define_command.
    def exitDefine_command(self, ctx:PlSqlParser.Define_commandContext):
        # convert define command to \set and erase '=' sign
        for child in ctx.children:
            if isinstance(child, TerminalNode):
                if child.symbol == ctx.start:
                    new_txt = r'\set'
                    self.rewriter.replaceSingleToken(child.symbol, new_txt)
                elif child.symbol.text == '=':
                    new_txt = ''
                    self.rewriter.replaceSingleToken(child.symbol, new_txt)

    # Exit a parse tree produced by PlSqlParser#regular_id.
    def exitRegular_id(self, ctx:PlSqlParser.Regular_idContext):
        token = ctx.start
        
        # convert variable's sign from '&' to ':'
        new_txt = ':' if token.text == '&' else token.text
        self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#native_datatype_element.
    def exitNative_datatype_element(self, ctx:PlSqlParser.Native_datatype_elementContext):
        token = ctx.start
        
        # convert datatype
        if ctx.start == ctx.stop:
            if token.text in self.DATA_TYPE.keys():
                new_txt = self.DATA_TYPE[token.text]
                self.rewriter.replaceSingleToken(token, new_txt)
        else:
            # convert LONG ROW type
            if ctx.start.text == 'LONG':
                new_txt = 'BYTEA'
                self.rewriter.replaceSingleToken(ctx.start, new_txt)
                self.rewriter.replaceSingleToken(ctx.stop, '')

    # Exit a parse tree produced by PlSqlParser#quoted_string.
    def exitQuoted_string(self, ctx:PlSqlParser.Quoted_stringContext):
        token = ctx.start
        txt = token.text
        
        # convert variable's sign from '&' to ':' in string
        new_txt = txt.replace('&', ':')
        self.rewriter.replaceSingleToken(token, new_txt)
                