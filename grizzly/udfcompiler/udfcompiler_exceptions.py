# Exception class for defining compiler Errors that are used for Pandas fallback
class UDFCompilerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class UDFParseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)