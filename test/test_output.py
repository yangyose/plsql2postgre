TEST_OUTSTR =   ['--\r\n',                                                      #シングルラインコメント - ハイフン内容なし
                 '--\r\n',                                                      #シングルラインコメント - rem内容なし
                 '--\r\n',                                                      #シングルラインコメント - remark内容なし
                 '--\r\n',                                                      #シングルラインコメント - REM内容なし
                 '--\r\n',                                                      #シングルラインコメント - REMARK内容なし
                 '/**/\r\n',                                                    #シングルラインコメント - マルチライン方式内容なし
                 '--これはコメントです。\r\n',                                  #シングルラインコメント - ハイフンのスペース区切りなし
                 '---------------------\r\n',                                   #シングルラインコメント - ハイフン続き
                 '--------------------\r\n',                                    #シングルラインコメント - remスペース区切りなし
                 '--------------------\r\n',                                    #シングルラインコメント - remarkスペース区切りなし
                 '--------------------\r\n',                                    #シングルラインコメント - REMスペース区切りなし
                 '--------------------\r\n',                                    #シングルラインコメント - REMARKスペース区切りなし
                 '/*------------------*/\r\n',                                  #シングルラインコメント - マルチライン方式スペース区切りなし
                 '-- これはコメントです。\r\n',                                 #シングルラインコメント - ハイフンのスペース区切りあり
                 '-- これはコメントです。\r\n',                                 #シングルラインコメント - remスペース区切りあり
                 '-- これはコメントです。\r\n',                                 #シングルラインコメント - remarkスペース区切りあり
                 '-- これはコメントです。\r\n',                                 #シングルラインコメント - REMスペース区切りあり
                 '-- これはコメントです。\r\n',                                 #シングルラインコメント - REMARKスペース区切りあり
                 '/* これはコメントです。 */\r\n',                              #シングルラインコメント - マルチライン方式スペース区切りあり
                 '-- SELECT NVL(1,2) FROM DUAL;\r\n',                           #シングルラインコメント - ハイフン後擬似ステートメント無効
                 '--  SELECT NVL(1,2) FROM DUAL;\r\n',                          #シングルラインコメント - rem後擬似ステートメント無効
                 '--  SELECT NVL(1,2) FROM DUAL;\r\n',                          #シングルラインコメント - remark後擬似ステートメント無効
                 '--  SELECT NVL(1,2) FROM DUAL;\r\n',                          #シングルラインコメント - REM後擬似ステートメント無効
                 '--  SELECT NVL(1,2) FROM DUAL;\r\n',                          #シングルラインコメント - REMARK後擬似ステートメント無効
                 '/* コメント SELECT NVL(1,2) FROM DUAL; */\r\n',               #シングルラインコメント - マルチライン方式中擬似ステートメント無効
                 'SELECT COALESCE(1,2) /* FROM DUAL */; -- コメント\r\n',       #シングルラインコメント - ハイフン前ステートメント有効
                 'SELECT COALESCE(1,2) /* FROM DUAL */; /* コメント */\r\n',    #シングルラインコメント - マルチライン方式前ステートメント有効
                 '/* コメント */SELECT COALESCE(1,2) /* FROM DUAL */;\r\n',     #シングルラインコメント - マルチライン方式後ステートメント有効
                 'SELECT/* コメント */COALESCE(1,2) /* FROM DUAL */;\r\n',      #シングルラインコメント - マルチライン方式前後ステートメント有効
                 '/*\r\n*/\r\n',                                                #マルチラインコメント - 内容なし
                 '/*---------\r\n---------*/\r\n',                              #マルチラインコメント - スペース区切りなし
                 '/* コメント行１\r\nコメント行２。 */\r\n',                    #マルチラインコメント - スペース区切りあり
                 '/* コメント\r\nSELECT NVL(1,2) FROM DUAL; */\r\n',            #マルチラインコメント - 中擬似ステートメント無効
                 'SELECT COALESCE(1,2) /* FROM DUAL */; /* コメント行１\r\nコメント行２ */\r\n',
                                                                                #マルチラインコメント - 前ステートメント有効
                 '/* コメント行１\r\nコメント行２ */ SELECT COALESCE(1,2) /* FROM DUAL */;\r\n',
                                                                                #マルチラインコメント - 後ステートメント有効
                 'SELECT/* コメント行１\r\nコメント行２ */COALESCE(1,2) /* FROM DUAL */;\r\n',
                                                                                #マルチラインコメント - 前後ステートメント有効

                 '\r\n',                                                        #SQL文即時実行コマンド
                 '\\q\r\n',                                                     #exitコマンド
                 '\\q\r\n',                                                     #EXITコマンド
                 '\\echo select NVL(1,2) FROM DUAL;\r\n',                       #proメッセージ表示 - 後ステートメント無効
                 '\\echo select NVL(1,2) FROM DUAL;\r\n',                       #promptメッセージ表示 - 後ステートメント無効
                 '\\echo select NVL(1,2) FROM DUAL;\r\n',                       #PROメッセージ表示 - 後ステートメント無効
                 '\\echo select NVL(1,2) FROM DUAL;\r\n',                       #PROMPTメッセージ表示 - 後ステートメント無効
                 '\\errverbose \r\n',                                           #show errコマンド
                 '\\errverbose \r\n',                                           #SHOW ERRコマンド
                 '\\errverbose \r\n',                                           #show errorsコマンド
                 '\\errverbose \r\n',                                           #SHOW ERRORSコマンド
                 '/* whenever sqlerror exit failure rollback */\r\n',           #wheneverコマンド
                 '/* WHENEVER OSERROR CONTINUE NONE */\r\n',                    #WHENEVERコマンド
                 '/* set echo off */\r\n\\set ECHO_HIDDEN off\r\n',             #set echoコマンド
                 '/* SET ECHO ON */\r\n\\set ECHO_HIDDEN ON\r\n',               #SET ECHOコマンド
                 '/* set auto on */\r\n\\set AUTOCOMMIT on\r\n',                #set autoコマンド
                 '/* SET AUTO OFF */\r\n\\set AUTOCOMMIT OFF\r\n',              #SET AUTOコマンド
                 '/* set autocommit off */\r\n\\set AUTOCOMMIT off\r\n',        #set autocommitコマンド
                 '/* SET AUTOCOMMIT ON */\r\n\\set AUTOCOMMIT ON\r\n',          #SET AUTOCOMMITコマンド
                 '/* set colsep "" */\r\n\\pset fieldsep ""\r\n',               #set colsepコマンド
                 "/* SET COLSEP ',' */\r\n\\pset fieldsep ','\r\n",             #SET COLSEPコマンド
                 '/* set lin 2000 */\r\n\\pset columns 2000\r\n',               #set linコマンド
                 '/* SET LIN 2000 */\r\n\\pset columns 2000\r\n',               #SET LINコマンド
                 '/* set linesize 2000 */\r\n\\pset columns 2000\r\n',          #set linesizeコマンド
                 '/* SET LINESIZE 2000 */\r\n\\pset columns 2000\r\n',          #SET LINESIZEコマンド
                 "/* set null '' */\r\n\\pset null ''\r\n",                     #set nullコマンド
                 "/* SET NULL '' */\r\n\\pset null ''\r\n",                     #SET NULLコマンド
                 '/* set pages 0 */\r\n\\pset pager_min_lines 0\r\n',           #set pagesコマンド
                 '/* SET PAGES 0 */\r\n\\pset pager_min_lines 0\r\n',           #SET PAGESコマンド
                 '/* set pagesize 0 */\r\n\\pset pager_min_lines 0\r\n',        #set pagesizeコマンド
                 '/* SET PAGESIZE 0 */\r\n\\pset pager_min_lines 0\r\n',        #SET PAGESIZEコマンド
                 "/* set recsepchar ';' */\r\n\\pset recordsep ';'\r\n",        #set recsepcharコマンド
                 "/* SET RECSEPCHAR ';' */\r\n\\pset recordsep ';'\r\n",        #SET RECSEPCHARコマンド
                 '/* set timi on */\r\n\\timing on\r\n',                        #set timiコマンド
                 '/* SET TIMI OFF */\r\n\\timing OFF\r\n',                      #SET TIMIコマンド
                 '/* set timing off */\r\n\\timing off\r\n',                    #set timingコマンド
                 '/* SET TIMING ON */\r\n\\timing ON\r\n',                      #SET TIMINGコマンド
                 '/* set feedback off */\r\n',                                  #setコマンド - 変換せずコメント
                 '\\set ERR_CD  1\r\n',                                         #defコマンド - 数値セット
                 "\\set ERR_CD  '1'\r\n",                                       #DEFコマンド - 文字セット
                 '\\set ERR_CD  errcd\r\n',                                     #defineコマンド - 変数セット
                 '\\set ERR_CD\r\n',                                            #DEFINEコマンド - 定義のみ

                 'SELECT COALESCE(SEQ_NO,0) FROM TEST_TBL;\r\n',                #NVL関数
                 "SELECT COALESCE(SAM_STR,'') FROM TEST_TBL;\r\n",              #nvl関数
                 "SELECT COALESCE(SAM_STR,COALESCE(NVL_STR,'')) FROM TEST_TBL;\r\n",
                                                                                #NVL関数 - 二重ネスト

                 'SELECT CURRENT_TIMESTAMP /* FROM DUAL */;\r\n',               #sysdateシステム変数
                 "SELECT TO_CHAR(CURRENT_TIMESTAMP,'YYYYMMDDHH24MISS') /* FROM DUAL */;\r\n",
                                                                                #SYSDATEシステム変数
                 '\\set ERR_CD  :1\r\n',                                        #パラメータ変数 - セット
                 'SELECT * FROM TEST_TBL WHERE SEQ_NO = :1;\r\n',               #パラメータ変数 - 数値引用
                 "SELECT * FROM TEST_TBL WHERE SAM_STR = :'1';\r\n",            #パラメータ変数 - 文字引用
                 "SELECT :'1' || 'TEST' /* FROM DUAL */;\r\n",                  #パラメータ変数 - 文字引用（先頭）
                 "SELECT 'DROPTABLE' || :'1' || 'CASCADE' /* FROM DUAL */;\r\n",#パラメータ変数 - 文字引用（中）
                 "SELECT 'T' || :'1' || 'T' || :'2' || 'T' /* FROM DUAL */;\r\n",#パラメータ変数 - 文字引用（中2回）
                 "SELECT 'T' || :'1' || :'2' || 'T' /* FROM DUAL */;\r\n",      #パラメータ変数 - 文字引用（中2回連続）
                 "SELECT 'TEST' || :'1' /* FROM DUAL */;\r\n",                  #パラメータ変数 - 文字引用（最後）
                 '\\set ERR_CD  :errcd\r\n',                                    #バインド変数 - セット
                 'SELECT * FROM TEST_TBL WHERE SEQ_NO = :seqno;\r\n',
                                                                                #バインド変数 - 数値引用
                 "SELECT * FROM TEST_TBL WHERE SAM_STR = :'teststr';\r\n",
                                                                                #バインド変数 - 文字引用
                 "SELECT :'tblname' || ' TEST' /* FROM DUAL */;\r\n",           #バインド変数 - 文字引用（先頭）
                 "SELECT 'DROPTABLE' || :'tblname' || ' CASCADE' /* FROM DUAL */;\r\n",
                                                                                #バインド変数 - 文字引用（中1回）
                 "SELECT 'T' || :'tname' || ' T' || :'tname' || ' T' /* FROM DUAL */;\r\n",#バインド変数 - 文字引用（中2回）
                 "SELECT 'T' || :'tname' || :'tname' || ' T' /* FROM DUAL */;\r\n",#バインド変数 - 文字引用（中2回連続）
                 "SELECT 'TEST' || :'tname' /* FROM DUAL */;\r\n",              #バインド変数 - 文字引用（最後）

                 ' ',                                                           #スペース
                 '\t',                                                          #タブ
                 '\r\n',                                                        #Windows式改行
                 '\n'                                                           #Unix式改行
                ]
