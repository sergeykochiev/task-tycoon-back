from dtos.users.user_create import CreateUser
from database.database import new_session
from models.UserModel import UserModel
from uuid import UUID

class UserRepository:
    @classmethod
    async def add_one(cls, data: CreateUser) -> UUID:
        async with new_session() as session:
            user_dict = data.model_dump()

            user = UserModel(**user_dict)

            session.add(user)
            await session.flush()
            await session.commit()
            return user.UUID
