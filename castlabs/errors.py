class CPGenericException(Exception):
    def __init__(self, data: dict):
        super().__init__(data["message"])
        self.data = data


class CPAuthorizationException(CPGenericException):
    pass


class CPMalformedHttpRequestException(CPGenericException):
    pass
