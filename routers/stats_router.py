from fastapi import APIRouter, Depends
from repositories import AttemptStatsRepository, TaskRepository
from services.authentication import fastapi_users
from dtos.attempt_stats.attempt_stats import GetAttemptStatsDto, GetAttemptStatsResponse
from models import UserModel
from services.permissions import Permissions
from utils.custom_errors import NoPermissionException, NotFoundException
from utils.enums import PermissionsEnum


stats_router: APIRouter = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@stats_router.get('/attempt')
async def get_attempt_stats(
    query_params: GetAttemptStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetAttemptStatsResponse:
    attempt_stats_entity = await AttemptStatsRepository.find_one_by_id(query_params.attempt_id)
    if not attempt_stats_entity:
        raise NotFoundException(f'Не найдена попытка с id={query_params.attempt_id}')
    if user.is_superuser:
        return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)
    task_entity = await TaskRepository.find_by_id(attempt_stats_entity.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={attempt_stats_entity.task_id}')
    if task_entity.user_id != user.id:
        raise NoPermissionException(f'У вас нет прав на просмотр данной статистики')
    return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)

