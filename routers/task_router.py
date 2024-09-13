from typing import List
from fastapi import APIRouter, Depends
from dtos.questions import Question
from dtos.tasks import GetTasksResponse, IsolatedTask, GetTasksByUserDto, GetTasksByTitleDto, \
    GetTaskByIdentifierDto, FullTaskResponse, DeleteTaskByIdDto, CreateTaskResponse, CreateTaskDto
from dtos.transactions.transaction import TransactionPayload
from repositories import TaskRepository
from services.authentication import fastapi_users
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from uuid import UUID
from models import UserModel, TaskModel, QuestionModel
from services.transactions import Transaction
from utils.enums import TransactionMethodsEnum

tasks_router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@tasks_router.post("/")
async def add_task(
        task_schema: CreateTaskDto,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    models_for_transaction = list()

    task_model: TaskModel = task_dto_to_model(task_schema, user_entity)
    models_for_transaction.append(task_model)

    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_model)
    models_for_transaction.extend(question_models)

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.INSERT,
            models=models_for_transaction
        )
    ]

    transaction: Transaction = Transaction(transaction_payload)
    await transaction.run()

    return CreateTaskResponse(ok=True, task_id=task_model.id)


@tasks_router.get("/")
async def get_tasks() -> GetTasksResponse:
    task_entities: List[TaskModel] = await TaskRepository.find_all()
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/user_id")
async def get_tasks_by_user(
    query_params: GetTasksByUserDto = Depends()
) -> GetTasksResponse:
    user_id = query_params.user_id
    task_entities: List[TaskModel] = await TaskRepository.find_by_user(user_id)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/task_title")
async def get_tasks_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTasksResponse:
    task_title = query_params.title
    task_entities: List[TaskModel] = await TaskRepository.find_by_title(task_title)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/identifier")
async def get_task_by_identifier(
    query_params: GetTaskByIdentifierDto = Depends()
) -> FullTaskResponse:
    identifier = query_params.identifier
    task_entity = await TaskRepository.find_by_identifier(identifier)
    validated_questions: List[Question] = \
        [Question.model_validate(question_model.__dict__) for question_model in task_entity.questions]
    result: FullTaskResponse = FullTaskResponse(
        task = IsolatedTask.model_validate(task_entity.__dict__),
        questions = validated_questions
    )
    return result


@tasks_router.delete("/")
async def delete_task_by_id(
        body: DeleteTaskByIdDto,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> UUID:
    if user_entity.is_superuser:
        await TaskRepository.delete_by_id(body.task_id)
    return body.task_id
