TEST_INSTR =    [' ',                                               #スペース
                 '\t',                                              #タブ
                 '\r\n',                                            #Windows式改行
                 '\n',                                              #Unix式改行

                 '--\r\n',                                          #シングルラインコメント - ハイフン内容なし
                 'rem\r\n',                                         #シングルラインコメント - rem内容なし
                 'remark\r\n',                                      #シングルラインコメント - remark内容なし
                 'REM\r\n',                                         #シングルラインコメント - REM内容なし
                 'REMARK\r\n',                                      #シングルラインコメント - REMARK内容なし
                 '/**/\r\n',                                        #シングルラインコメント - マルチライン方式内容なし
                 '--これはコメントです。\r\n',                      #シングルラインコメント - ハイフンのスペース区切りなし
                 '---------------------\r\n',                       #シングルラインコメント - ハイフン続き
                 'rem------------------\r\n',                       #シングルラインコメント - remスペース区切りなし
                 'remark------------------\r\n',                    #シングルラインコメント - remarkスペース区切りなし
                 'REM------------------\r\n',                       #シングルラインコメント - REMスペース区切りなし
                 'REMARK------------------\r\n',                    #シングルラインコメント - REMARKスペース区切りなし
                 '/*------------------*/\r\n',                      #シングルラインコメント - マルチライン方式スペース区切りなし
                 '-- これはコメントです。\r\n',                     #シングルラインコメント - ハイフンのスペース区切りあり
                 'rem これはコメントです。\r\n',                    #シングルラインコメント - remスペース区切りあり
                 'remark これはコメントです。\r\n',                 #シングルラインコメント - remarkスペース区切りあり
                 'REM これはコメントです。\r\n',                    #シングルラインコメント - REMスペース区切りあり
                 'REMARK これはコメントです。\r\n',                 #シングルラインコメント - REMARKスペース区切りあり
                 '/* これはコメントです。 */\r\n',                  #シングルラインコメント - マルチライン方式スペース区切りあり
                 '-- SELECT NVL(1,2) FROM DUAL;\r\n',               #シングルラインコメント - ハイフン後擬似ステートメント無効
                 'rem  SELECT NVL(1,2) FROM DUAL;\r\n',             #シングルラインコメント - rem後擬似ステートメント無効
                 'remark  SELECT NVL(1,2) FROM DUAL;\r\n',          #シングルラインコメント - remark後擬似ステートメント無効
                 'REM  SELECT NVL(1,2) FROM DUAL;\r\n',             #シングルラインコメント - REM後擬似ステートメント無効
                 'REMARK  SELECT NVL(1,2) FROM DUAL;\r\n',          #シングルラインコメント - REMARK後擬似ステートメント無効
                 '/* コメント SELECT NVL(1,2) FROM DUAL; */\r\n',   #シングルラインコメント - マルチライン方式中擬似ステートメント無効
                 'SELECT NVL(1,2) FROM DUAL; -- コメント\r\n',      #シングルラインコメント - ハイフン前ステートメント有効
                 'SELECT NVL(1,2) FROM DUAL; /* コメント */\r\n',   #シングルラインコメント - マルチライン方式前ステートメント有効
                 '/* コメント */SELECT NVL(1,2) FROM DUAL;\r\n',    #シングルラインコメント - マルチライン方式後ステートメント有効
                 'SELECT/* コメント */NVL(1,2) FROM DUAL;\r\n',     #シングルラインコメント - マルチライン方式前後ステートメント有効
                 '/*\r\n*/\r\n',                                    #マルチラインコメント - 内容なし
                 '/*---------\r\n---------*/\r\n',                  #マルチラインコメント - スペース区切りなし
                 '/* コメント行１\r\nコメント行２。 */\r\n',        #マルチラインコメント - スペース区切りあり
                 '/* コメント\r\nSELECT NVL(1,2) FROM DUAL; */\r\n',#マルチラインコメント - 中擬似ステートメント無効
                 'SELECT NVL(1,2) FROM DUAL; /* コメント行１\r\nコメント行２ */\r\n',
                                                                    #マルチラインコメント - 前ステートメント有効
                 '/* コメント行１\r\nコメント行２ */ SELECT NVL(1,2) FROM DUAL;\r\n',
                                                                    #マルチラインコメント - 後ステートメント有効
                 'SELECT/* コメント行１\r\nコメント行２ */NVL(1,2) FROM DUAL;\r\n',
                                                                    #マルチラインコメント - 前後ステートメント有効

                 '/\r\n',                                           #SQL文即時実行コマンド
                 'exit\r\n',                                        #exitコマンド
                 'EXIT\r\n',                                        #EXITコマンド
                 'pro select NVL(1,2) FROM DUAL;\r\n',              #proメッセージ表示 - 後ステートメント無効
                 'prompt select NVL(1,2) FROM DUAL;\r\n',           #promptメッセージ表示 - 後ステートメント無効
                 'PRO select NVL(1,2) FROM DUAL;\r\n',              #PROメッセージ表示 - 後ステートメント無効
                 'PROMPT select NVL(1,2) FROM DUAL;\r\n',           #PROMPTメッセージ表示 - 後ステートメント無効
                 'show err\r\n',                                    #show errコマンド
                 'SHOW ERR\r\n',                                    #SHOW ERRコマンド
                 'show errors\r\n',                                 #show errorsコマンド
                 'SHOW ERRORS\r\n',                                 #SHOW ERRORSコマンド
                 'whenever sqlerror exit failure rollback\r\n',     #wheneverコマンド
                 'WHENEVER OSERROR CONTINUE NONE\r\n',              #WHENEVERコマンド
                 'set echo off\r\n',                                #set echoコマンド
                 'SET ECHO ON\r\n',                                 #SET ECHOコマンド
                 'set auto on\r\n',                                 #set autoコマンド
                 'SET AUTO OFF\r\n',                                #SET AUTOコマンド
                 'set autocommit off\r\n',                          #set autocommitコマンド
                 'SET AUTOCOMMIT ON\r\n',                           #SET AUTOCOMMITコマンド
                 'set colsep ""\r\n',                               #set colsepコマンド
                 "SET COLSEP ','\r\n",                              #SET COLSEPコマンド
                 'set lin 2000\r\n',                                #set linコマンド
                 'SET LIN 2000\r\n',                                #SET LINコマンド
                 'set linesize 2000\r\n',                           #set linesizeコマンド
                 'SET LINESIZE 2000\r\n',                           #SET LINESIZEコマンド
                 "set null ''\r\n",                                 #set nullコマンド
                 "SET NULL ''\r\n",                                 #SET NULLコマンド
                 'set pages 0\r\n',                                 #set pagesコマンド
                 'SET PAGES 0\r\n',                                 #SET PAGESコマンド
                 'set pagesize 0\r\n',                              #set pagesizeコマンド
                 'SET PAGESIZE 0\r\n',                              #SET PAGESIZEコマンド
                 "set recsepchar ';'\r\n",                          #set recsepcharコマンド
                 "SET RECSEPCHAR ';'\r\n",                          #SET RECSEPCHARコマンド
                 'set timi on\r\n',                                 #set timiコマンド
                 'SET TIMI OFF\r\n',                                #SET TIMIコマンド
                 'set timing off\r\n',                              #set timingコマンド
                 'SET TIMING ON\r\n',                               #SET TIMINGコマンド
                 'set feedback off\r\n'                             #setコマンド - 変換せずコメント
                ]
