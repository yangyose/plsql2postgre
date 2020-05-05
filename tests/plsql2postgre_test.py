""" Automatic acceptance test for plsql2postgre by pytest framework.

    [class]LoadData - Get test datas from test cases.
    [class]TestRun  - Run test using test datas.
"""
import  pytest
import  xlrd
from    antlr4                              import InputStream
from    plsql2postgre.PlSql2Postgre         import PlSql2Postgre, DEFAULT_ENCODING

class LoadData:
    """ Get test datas from test cases.

        [property]test_case  - Set the excel file's name containing unit test cases.
        [property]input_col  - Set the input data's column number in excel file.
        [property]output_col - Set the expected result's column number in excel file.
        [property]unit_data  - Return the matching list of input data and expected results.
    """
    test_case = 'PlSql2PostgreTestCase.xlsx'
    input_col = 5
    output_col = 6

    def __init__(self):
        """ Get excel's worksheet object for read

        """
        self.__worksheet = xlrd.open_workbook(self.test_case).sheet_by_index(0)

    @property
    def unit_data(self):
        """ Get and return the matching list of input data and expected results
            from excel file as a property.

        """
        # Set default test datas.
        test_instr = ['\t', '\r\n']
        test_outstr = ['\t', '\r\n']
        # Get input datas and expected results from excel file.
        test_instr.extend(self.__worksheet.col_values(self.input_col, 1))
        test_outstr.extend(self.__worksheet.col_values(self.output_col, 1))
        # Return the matching list of input data and expected results.
        return [(test_instr[i], test_outstr[i]) for i in range(len(test_instr))]

    @property
    def inte_data(self):
        """ Get and return the integration sql script data and expected results.
            *** uncompleted ***

        """
        return []

class TestRun:
    """ Run test using test datas.

        [method]test_unit - Run test using unit datas getting from LoadData class.
    """
    @staticmethod
    def __test_run(origin, result):
        """ Run test iterative using test datas.

            [argument]origin - Set input data string.
            [argument]result - Set expected result string.
        """
        # Preprocess the input data.
        input_stream = InputStream(origin)
        # Run the real test object.
        converter = PlSql2Postgre(input_stream)
        # Determine the result.
        assert converter.run().decode(DEFAULT_ENCODING) == result

    @pytest.mark.parametrize('instr, outstr', LoadData().unit_data)
    def test_unit(self, instr, outstr):
        """ Run test iterative using unit test datas.

            [argument]instr  - Set input data string.
            [argument]outstr - Set expected result string.
        """
        self.__test_run(instr, outstr)

    @pytest.mark.parametrize('instr, outstr', LoadData().inte_data)
    def test_integration(self, instr, outstr):
        """ Run test iterative using integration test datas.
            *** uncompleted ***

            [argument]instr  - Set input data string.
            [argument]outstr - Set expected result string.
        """
        self.__test_run(instr, outstr)
