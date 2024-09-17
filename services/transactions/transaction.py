from types import NoneType
from typing import Dict, List, Union

from sqlalchemy import text
from database.database import get_async_session
from dtos.transactions.transaction import TransactionPayload
from utils.enums import TransactionMethodsEnum
import models as database_models


class Transaction:
    payload: List[TransactionPayload]
    session = None

    def __init__(self, payload: List[TransactionPayload]):
        self.payload = payload
        
    async def __get_session__(self):
        async for session in get_async_session():
            self.session = session

    async def extend(self, payload: List[TransactionPayload]):
        self.payload.extend(payload)
        await self.pre_run()

    async def pre_run(self):
        if self.session is None:
            await self.__get_session__()
        for action in self.payload:
            if action.method == TransactionMethodsEnum.INSERT:
                for model in action.models:
                    self.session.add(model)
                        
            elif action.method == TransactionMethodsEnum.DELETE:
                for model in action.models:
                    await self.session.delete(model)
                        
            elif action.method == TransactionMethodsEnum.UPDATE:
                for model in action.models:
                    params = list()
                    updateQuery: str = f"UPDATE {model.__tablename__} SET "
                    for key, value in model.__dict__.items():
                        if type(value) in [str, int]:
                            updateQuery += f"{key} = '{value}', "
                        elif type(value) == NoneType:
                            updateQuery += f"{key} = NULL, "
                        elif type(value) in [list]:
                            updateQuery += f"{key} = '{str(value).replace("'", '"')}'::jsonb, "
                    updateQuery = updateQuery[:-2] + f" WHERE id='{model.id}'"
                    await self.session.execute(text(updateQuery), params)

    async def run(self) -> None:
        if self.session is None:
            await self.pre_run()
        try:      
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
