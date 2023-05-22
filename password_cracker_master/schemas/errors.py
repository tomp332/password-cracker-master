from enum import Enum
from typing import Any

from fastapi import HTTPException


class FrameworkErrorCodesEnum(int, Enum):
    """
    Framework error codes
    """
    PASSWORD_FORMAT_ERROR = 1
    DIRLIST_FILE_ERROR = 2

class FrameworkError(HTTPException):
    """
    Framework error model
    """

    def __init__(self, message: Any, status_code: FrameworkErrorCodesEnum):
        self.message: Any = message
        self.status_code: FrameworkErrorCodesEnum = status_code
        self.http_code: int = 500
        self.parse_error()
        super().__init__(status_code=self.http_code, detail=self.message)

    def parse_error(self):
        """
        Parse error to HTTP status code
        """
        match self.status_code.value:
            case self.status_code.value if 1 <= self.status_code.value < 10:
                self.http_code = 400
            case self.status_code.value if 10 <= self.status_code.value < 20:
                self.http_code = 404
            case self.status_code.value if 20 <= self.status_code.value < 30:
                self.http_code = 500
