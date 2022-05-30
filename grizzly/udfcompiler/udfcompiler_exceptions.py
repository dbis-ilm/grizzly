# Exception class for defining compiler Errors that are used for Pandas fallback
class UDFCompilerException(Exception):
    def __init__(self, message, compileerror=None, funccall=None):
        self.message = message
        self.compileerror = compileerror
        self.funccall = funccall
        super().__init__(message)