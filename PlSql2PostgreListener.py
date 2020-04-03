import re

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
    EXT_FSERVER_NAME = 'PG_FILE_SERVER'

    # need rewriter to change token stream
    def __init__(self, tokens:TokenStream):
        self.tokens = tokens
        self.rewriter = TokenStreamRewriter(tokens)
        self.__query_elements = []
        self.__crtl_elements = []
    
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

    def replaceBindVarInQuote(self, str):
        if str[-1] != "'":
            return str
            
        pattern = re.compile(r'([^&]*)(&[0-9]+|&[a-zA-Z][a-zA-Z0-9_]*)(.*)')
        str_proc = str
        str_ret = ""
        result = pattern.match(str_proc)
        if not result:
            return str
        while result:
            if result.group(1) == "'":
                str_ret = str_ret + ":'" + result.group(2)[1:]
            else:
                str_ret = str_ret + result.group(1) + "' || :'" + result.group(2)[1:]
            if result.group(3) != "'":
                str_proc = "'" + result.group(3)
            else:
                str_proc = result.group(3)
            result = pattern.match(str_proc)
        if str_proc == "'":
            str_ret = str_ret + str_proc
        else:
            str_ret = str_ret + "' || '" + str_proc
        return str_ret
        
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
        # convert 'show errors' command to \errverbose
        elif txt.upper() == 'SHOW':
            new_txt = r'\errverbose'
            self.rewriter.replaceSingleToken(token, new_txt)
            token = ctx.stop
            new_txt = ''
            self.rewriter.replaceSingleToken(token, new_txt)
        
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
        txt = token.text

        # at first comment set command
        new_txt = '-- ' + txt
        self.rewriter.replaceSingleToken(token, new_txt)
        
        # then chang some system variable by postgre's manner
        i = 1
        var_name = ''
        var_value = ''
        for child in ctx.children:
            if i == 2:
                var_name = child.getText()
            elif i == 3:
                var_value = child.getText()
                break
            i += 1
        token = ctx.stop
        # autocommit config
        if var_name.upper() in ('AUTO', 'AUTOCOMMIT'):
            if var_value.upper() not in ('ON', 'OFF'):
                var_value = 'on'
            new_txt = '\r\n' + r'\set AUTOCOMMIT ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # colsep config
        elif var_name.upper() == 'COLSEP':
            new_txt = '\r\n' + r'\pset fieldsep ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # echo config
        elif var_name.upper() == 'ECHO':
            new_txt = '\r\n' + r'\set ECHO_HIDDEN ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # linesize config
        elif var_name.upper() in ('LIN', 'LINESIZE'):
            new_txt = '\r\n' + r'\pset columns ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # null text config
        elif var_name.upper() == 'NULL':
            new_txt = '\r\n' + r'\pset null ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # pagesize config
        elif var_name.upper() in ('PAGES', 'PAGESIZE'):
            new_txt = '\r\n' + r'\pset pager_min_lines ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # recsepchar config
        elif var_name.upper() == 'RECSEPCHAR':
            new_txt = '\r\n' + r'\pset recordsep ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        # timing config
        elif var_name.upper() in ('TIMI', 'TIMING'):
            new_txt = '\r\n' + r'\timing ' + var_value
            self.rewriter.insertAfterToken(token, new_txt) 
        
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
        if token.text == '&':
            new_txt = ':'
            self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#physical_attributes_clause.
    def exitPhysical_attributes_clause(self, ctx:PlSqlParser.Physical_attributes_clauseContext):
        # convert variable's sign from '&' to ':'
        if ctx.AMPERSAND():
            for child in ctx.AMPERSAND():
                new_txt = ':'
                self.rewriter.replaceSingleToken(child.symbol, new_txt)

    # Exit a parse tree produced by PlSqlParser#literal.
    def exitLiteral(self, ctx:PlSqlParser.LiteralContext):
        # convert variable's sign from '&' to ':'
        if ctx.AMPERSAND():
            for child in ctx.AMPERSAND():
                new_txt = ':'
                self.rewriter.replaceSingleToken(child.symbol, new_txt)

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
        new_txt = self.replaceBindVarInQuote(txt)
        self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#logging_clause.
    def exitLogging_clause(self, ctx:PlSqlParser.Logging_clauseContext):
        token = ctx.start
        
        # comment logging clause
        new_txt = r'/* ' + token.text + r' */' 
        self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#anonymous_block.
    def exitAnonymous_block(self, ctx:PlSqlParser.Anonymous_blockContext):
        # insert DO statement
        token = ctx.start
        new_txt = 'DO $$\r\n' + token.text
        self.rewriter.replaceSingleToken(token, new_txt)
        
        token = ctx.stop
        new_txt = '$$' + token.text
        self.rewriter.replaceSingleToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#execute_immediate.
    def exitExecute_immediate(self, ctx:PlSqlParser.Execute_immediateContext):
        # delete keyword immediate
        token = ctx.IMMEDIATE().symbol
        self.rewriter.replaceSingleToken(token, '')
        
    # Enter a parse tree produced by PlSqlParser#query_block.
    def enterQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        # allocate select statement's infomation area
        self.__query_elements.append({})

    # Enter a parse tree produced by PlSqlParser#selected_list.
    def enterSelected_list(self, ctx:PlSqlParser.Selected_listContext):
        if self.__query_elements:
            query_element = self.__query_elements[-1]
            select_list = []
            for child in ctx.children:
                if isinstance(child, TerminalNode):
                    if child.symbol.text == '*':
                        select_list.append(child.symbol.text)
                else:
                    select_list.append(child.getText())
            query_element['select_list'] = select_list
        
    # Enter a parse tree produced by PlSqlParser#table_ref_list.
    def enterTable_ref_list(self, ctx:PlSqlParser.Table_ref_listContext):
        if self.__query_elements:
            query_element = self.__query_elements[-1]
            from_list = []
            for child in ctx.children:
                if not isinstance(child, TerminalNode): 
                    from_list.append(child.getText())
            query_element['from_list'] = from_list

    # Enter a parse tree produced by PlSqlParser#where_clause.
    def enterWhere_clause(self, ctx:PlSqlParser.Where_clauseContext):
        if self.__query_elements:
            query_element = self.__query_elements[-1]
            where_list = ''
            for child in ctx.children:
                if child.getText() != 'WHERE':
                    where_list = where_list + child.getText()
            query_element['where_list'] = where_list

    # Exit a parse tree produced by PlSqlParser#query_block.
    def exitQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        query_element = self.__query_elements.pop()

    # Enter a parse tree produced by PlSqlParser#create_table.
    def enterCreate_table(self, ctx:PlSqlParser.Create_tableContext):
        # allocate create table statement's infomation area
        self.__crtl_elements.append({'foreign_table':False,
                                     'file_location':''})

    # Enter a parse tree produced by PlSqlParser#external_table_clause.
    def enterExternal_table_clause(self, ctx:PlSqlParser.External_table_clauseContext):
        if self.__crtl_elements:
            crtl_element = self.__crtl_elements[-1]
            crtl_element['foreign_table'] = True

    # Enter a parse tree produced by PlSqlParser#external_data_properties.
    def enterExternal_data_properties(self, ctx:PlSqlParser.External_data_propertiesContext):
        if self.__crtl_elements:
            crtl_element = self.__crtl_elements[-1]
            crtl_element['file_location'] = self.replaceBindVarInQuote(ctx.quoted_string()[0].getText())

    # Exit a parse tree produced by PlSqlParser#physical_properties.
    def exitPhysical_properties(self, ctx:PlSqlParser.Physical_propertiesContext):
        if self.__crtl_elements:
            crtl_element = self.__crtl_elements[-1]
            if crtl_element['foreign_table']:
                token = ctx.ORGANIZATION().symbol
                new_txt = '/* ' + token.text
                self.rewriter.replaceSingleToken(token, new_txt)
                token = ctx.external_table_clause().stop
                new_txt = token.text + ' */'
                self.rewriter.replaceSingleToken(token, new_txt)
                new_txt = '\r\nSERVER ' + self.EXT_FSERVER_NAME
                new_txt = new_txt + '\r\nOPTIONS ('
                new_txt = new_txt + "\r\n    FILENAME " + crtl_element['file_location']
                new_txt = new_txt + '\r\n)'
                self.rewriter.insertAfterToken(token, new_txt)

    # Exit a parse tree produced by PlSqlParser#create_table.
    def exitCreate_table(self, ctx:PlSqlParser.Create_tableContext):
        crtl_element = self.__crtl_elements.pop()
        if crtl_element['foreign_table']:
           token = ctx.TABLE().symbol
           new_txt = 'FOREIGN ' + token.text
           self.rewriter.replaceSingleToken(token, new_txt)
                           