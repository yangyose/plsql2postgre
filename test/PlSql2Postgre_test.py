import sys
import xlrd

sys.path.append('..')
from antlr4                 import InputStream
from PlSql2Postgre          import PlSql2Postgre, DEFAULT_ENCODING

class TestRun():
    TEST_CASE = 'PlSql2PostgreTestCase.xlsx'
    INPUT_COL = 5
    OUTPUT_COL = 6

    def setup_class(self):
        self.test_instr = ['\t', '\r\n']
        self.test_outstr = ['\t', '\r\n']

        worksheet = xlrd.open_workbook(self.TEST_CASE).sheet_by_index(0)
        self.test_instr.extend(worksheet.col_values(self.INPUT_COL, 1))
        self.test_outstr.extend(worksheet.col_values(self.OUTPUT_COL, 1))

    def test_run(self):
        str_len = len(self.test_instr)
        for i in range(str_len):
            input_stream = InputStream(self.test_instr[i])
            converter = PlSql2Postgre(input_stream)
            assert converter.run().decode(DEFAULT_ENCODING) == self.test_outstr[i]
