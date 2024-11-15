from fastapi import HTTPException

class TeapotException(HTTPException):
    def __init__(self, message:str = 'blank'):
        super().__init__(status_code=418, detail=message)