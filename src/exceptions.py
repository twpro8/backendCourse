from datetime import date

from fastapi.exceptions import HTTPException


class MomoaException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MomoaException):
    detail = "Object not found"


class NoAvailableRoomsException(MomoaException):
    detail = "No rooms left"


class ObjectAlreadyExistsException(MomoaException):
    detail = "Object already exists"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class MomoaHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Hotel not found"


class UserAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "User already exists"


class UserDoesNotExistHTTPException(MomoaHTTPException):
    status_code = 401
    detail = "User does not exist"


class IncorrectPasswordHTTPException(MomoaHTTPException):
    status_code = 401
    detail = "Incorrect password"


class RoomNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Room not found"


class NoAvailableRoomsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "No rooms left"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422,
            detail='"Check-out" date must be later than the "check-in" date.',
        )
