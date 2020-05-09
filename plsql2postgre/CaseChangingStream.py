"""Provide the class to change the string's case.

    [class]CaseChangingStream - Change the string's case.
"""
class CaseChangingStream():
    """Change the string's case.

        [function]LA - Get the char from string by offset.
    """
    def __init__(self, stream, upper):
        """Init the properties of class.

            [argument]stream - Set the object string
            [argument]upper  - Change to uppercase if true, false to lowercase
        """
        self._stream = stream
        self._upper = upper

    def __getattr__(self, name):
        """Redirect every property or method call to string object."""
        return self._stream.__getattribute__(name)

    def LA(self, offset):
        """Get the char from string by offset."""
        char = self._stream.LA(offset)
        if char <= 0:
            return char
        return ord(chr(char).upper() if self._upper else chr(char).lower())
