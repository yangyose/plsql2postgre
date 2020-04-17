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

    # replace bind variant in string constant
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
            str_ret = str_ret + "' || " if str_ret else str_ret
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
            str_ret = str_ret + "' || " + str_proc
        return str_ret

    # comment the whole content
    def commentContext(self, ctx):
        self.rewriter.replaceSingleToken(ctx.start, '/* '+ctx.start.text)
        self.rewriter.replaceSingleToken(ctx.stop, ctx.stop.text+' */')
        
    # Exit a parse tree produced by PlSqlParser#sql_script.
    def exitSql_script(self, ctx:PlSqlParser.Sql_scriptContext):
        self.replaceEveryRemark()

    # Exit a parse tree produced by PlSqlParser#sql_plus_command.
    def exitSql_plus_command(self, ctx:PlSqlParser.Sql_plus_commandContext):
        token = ctx.start
        txt = token.text

        # convert / command to nothing
        if txt == '/':
            self.rewriter.replaceSingleToken(token, '')
        # convert exit command to \q
        elif txt.upper() == 'EXIT':
            self.rewriter.replaceSingleToken(token, r'\q')
        # convert prompt command to \echo
        elif txt[:6].upper() == 'PROMPT':
            self.rewriter.replaceSingleToken(token, r'\echo' + txt[6:])
        elif txt[:3].upper() == 'PRO':
            self.rewriter.replaceSingleToken(token, r'\echo' + txt[3:])
        # convert 'show errors' command to \errverbose
        elif txt.upper() == 'SHOW':
            self.rewriter.replaceSingleToken(token, r'\errverbose')
            self.rewriter.replaceSingleToken(ctx.stop, '')
        
    # Exit a parse tree produced by PlSqlParser#whenever_command.
    def exitWhenever_command(self, ctx:PlSqlParser.Whenever_commandContext):
        self.commentContext(ctx)
        
    # Exit a parse tree produced by PlSqlParser#set_command.
    def exitSet_command(self, ctx:PlSqlParser.Set_commandContext):
        # comment whole command at first
        self.commentContext(ctx)

        # change some system variable by postgre's manner
        child_num = len(ctx.children)
        var_name = ''
        var_value = ''
        if child_num >= 2:
            var_name = ctx.children[1].getText()
        if child_num >= 3:
            var_value = ctx.children[2].getText()
        
        # autocommit config
        if var_name.upper() in ('AUTO', 'AUTOCOMMIT'):
            if var_value.upper() not in ('ON', 'OFF'):
                var_value = 'on'
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\set AUTOCOMMIT ' + var_value) 
        # colsep config
        elif var_name.upper() == 'COLSEP':
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\pset fieldsep ' + var_value) 
        # echo config
        elif var_name.upper() == 'ECHO':
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\set ECHO_HIDDEN ' + var_value) 
        # linesize config
        elif var_name.upper() in ('LIN', 'LINESIZE'):
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\pset columns ' + var_value) 
        # null text config
        elif var_name.upper() == 'NULL':
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\pset null ' + var_value) 
        # pagesize config
        elif var_name.upper() in ('PAGES', 'PAGESIZE'):
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\pset pager_min_lines ' + var_value) 
        # recsepchar config
        elif var_name.upper() == 'RECSEPCHAR':
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\pset recordsep ' + var_value) 
        # timing config
        elif var_name.upper() in ('TIMI', 'TIMING'):
            self.rewriter.insertAfterToken(ctx.stop, '\r\n' + r'\timing ' + var_value) 
        
    # Exit a parse tree produced by PlSqlParser#define_command.
    def exitDefine_command(self, ctx:PlSqlParser.Define_commandContext):
        # convert define command to \set and erase '=' sign
        self.rewriter.replaceSingleToken(ctx.start, r'\set')
        if ctx.EQUALS_OP():
            self.rewriter.replaceSingleToken(ctx.EQUALS_OP().symbol, '')

    # Exit a parse tree produced by PlSqlParser#string_function.
    def exitString_function(self, ctx:PlSqlParser.String_functionContext):
        fname_token = ctx.start
        # change NVL function to COALESCE
        if fname_token.text.upper() == 'NVL':
            self.rewriter.replaceSingleToken(fname_token, 'COALESCE')

    # Exit a parse tree produced by PlSqlParser#regular_id.
    def exitRegular_id(self, ctx:PlSqlParser.Regular_idContext):
        # convert variable's sign from '&' to ':'
        if ctx.start.text == '&':
            self.rewriter.replaceSingleToken(ctx.start, ':')
        # convert sysdate to current_timestamp
        elif ctx.start.text.upper() == 'SYSDATE':
            self.rewriter.replaceSingleToken(ctx.start, 'CURRENT_TIMESTAMP')

    # Exit a parse tree produced by PlSqlParser#physical_attributes_clause.
    def exitPhysical_attributes_clause(self, ctx:PlSqlParser.Physical_attributes_clauseContext):
        # convert variable's sign from '&' to ':'
        if ctx.AMPERSAND():
            for child in ctx.AMPERSAND():
                self.rewriter.replaceSingleToken(child.symbol, ':')

    # Exit a parse tree produced by PlSqlParser#literal.
    def exitLiteral(self, ctx:PlSqlParser.LiteralContext):
        # convert variable's sign from '&' to ':'
        if ctx.AMPERSAND():
            for child in ctx.AMPERSAND():
                self.rewriter.replaceSingleToken(child.symbol, ':')

    # Exit a parse tree produced by PlSqlParser#native_datatype_element.
    def exitNative_datatype_element(self, ctx:PlSqlParser.Native_datatype_elementContext):
       # convert datatype
        if len(ctx.children) == 1:
            if ctx.start.text in self.DATA_TYPE.keys():
                self.rewriter.replaceSingleToken(ctx.start, self.DATA_TYPE[token.text])
        else:
            # convert LONG ROW type
            if ctx.start.text == 'LONG':
                self.rewriter.replaceSingleToken(ctx.start, 'BYTEA')
                self.rewriter.replaceSingleToken(ctx.stop, '')

    # Exit a parse tree produced by PlSqlParser#quoted_string.
    def exitQuoted_string(self, ctx:PlSqlParser.Quoted_stringContext):
        # convert variable's sign from '&' to ':' in string
        self.rewriter.replaceSingleToken(ctx.start, self.replaceBindVarInQuote(ctx.start.text))

    # Exit a parse tree produced by PlSqlParser#logging_clause.
    def exitLogging_clause(self, ctx:PlSqlParser.Logging_clauseContext):
        # comment logging clause
        self.rewriter.replaceSingleToken(ctx.start, r'/* ' + ctx.start.text + r' */')

    # Exit a parse tree produced by PlSqlParser#anonymous_block.
    def exitAnonymous_block(self, ctx:PlSqlParser.Anonymous_blockContext):
        # insert DO statement
        self.rewriter.replaceSingleToken(ctx.start, 'DO $$\r\n' + ctx.start.text)
        self.rewriter.replaceSingleToken(ctx.stop, '$$' + ctx.stop.text)

    # Exit a parse tree produced by PlSqlParser#execute_immediate.
    def exitExecute_immediate(self, ctx:PlSqlParser.Execute_immediateContext):
        # delete keyword immediate
        self.rewriter.replaceSingleToken(ctx.IMMEDIATE().symbol, '')
        
    # Enter a parse tree produced by PlSqlParser#query_block.
    def enterQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        # allocate select statement's infomation area
        self.__query_elements.append({'select_list':[],
                                      'from_list':[],
                                      'where_list':[]})

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
        # if from dual then comment from clause 
        if query_element['from_list'][0].upper() == 'DUAL':
            from_ctx = ctx.from_clause()
            self.rewriter.replaceSingleToken(from_ctx.start, '/* '+ from_ctx.start.text)
            self.rewriter.replaceSingleToken(from_ctx.stop, from_ctx.stop.text+' */')

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
                self.rewriter.replaceSingleToken(token, '/* ' + token.text)
                token = ctx.external_table_clause().stop
                self.rewriter.replaceSingleToken(token, token.text + ' */')
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
           self.rewriter.replaceSingleToken(token, 'FOREIGN ' + token.text)
                           