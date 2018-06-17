class Error(Exception):
    """
    Pyzub's base exception
    """
    pass


class InvalidTimeString(Error):
    """
    Raised when parser fail on bad formated time strings
    """
    pass
