from dataclasses import dataclass

from fastapi import HTTPException


# @dataclass
class ExceptionBase(HTTPException):
    detail: str
    status_code: int

    def __str__(self):
        return self.detail
