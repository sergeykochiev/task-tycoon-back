import os
import json
from typing import List, Optional
from pydantic import BaseModel, model_validator, computed_field, field_validator
from uuid import UUID
from dtos.questions.question import CreateQuestion, Question


class JsonValidatable:
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CreateTaskDto(BaseModel, JsonValidatable):
    title: str
    description_full: Optional[str] = None
    description_short: Optional[str] = None
    questions: List[CreateQuestion]


class CreateTaskResponse(BaseModel):
    task_id: UUID


class GetTaskTitle(BaseModel):
    id: UUID
    title: str


class IsolatedTask(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    identifier: int
    description_full: Optional[str]
    description_short: Optional[str]
    file_path: Optional[str] = None

    @computed_field
    @property
    def file_url(self) -> Optional[str]:
        if self.file_path is None:
            return None
        return f"http://127.0.0.1:8000/api/v1/tasks/download/?task_id={self.id}"
    
    @field_validator("file_path")
    def remove_dir(cls, v) -> Optional[str]:
        if v is None:
            return None
        return os.path.basename(v)


class GetWithoutQuestions(BaseModel):
    task: IsolatedTask
    mode: str

class FullTaskResponse(BaseModel):
    task: IsolatedTask
    questions: Optional[List[Question]]


class GetTasksResponse(BaseModel):
    tasks: List[IsolatedTask]


class GetTasksByUserDto(BaseModel):
    user_id: UUID


class GetTasksByTitleDto(BaseModel):
    title: str


class GetTaskByIdWithoutQuestions(BaseModel):
    id: UUID


class GetTaskByIdDto(BaseModel):
    id: UUID


class DeleteTaskByIdDto(BaseModel):
    task_id: UUID


class PatchTaskDto(BaseModel, JsonValidatable):
    task_id: UUID
    title: Optional[str] = None
    description_full: Optional[str] = None
    description_short: Optional[str] = None
    questions: Optional[List[CreateQuestion]] = []


class PatchTaskResponse(BaseModel):
    task_id: UUID


class UploadFileDto(BaseModel):
    task_id: UUID

class DownloadFileDto(BaseModel):
    task_id: UUID
