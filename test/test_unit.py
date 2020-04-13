import sys

sys.path.append('..')
from antlr4                 import InputStream
from PlSql2Postgre          import PlSql2Postgre, DEFAULT_ENCODING

from test_input             import TEST_INSTR
from test_output            import TEST_OUTSTR

class TestRun():
    def test_run(self):
        str_len = len(TEST_INSTR)
        for i in range(str_len):
            input_stream = InputStream(TEST_INSTR[i])
            converter = PlSql2Postgre(input_stream)
            assert converter.run().decode(DEFAULT_ENCODING) == TEST_OUTSTR[i]
