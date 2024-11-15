
import datetime
from typing import List, Optional
from dtos.answers.answer import AnswerContent
from pydantic import BaseModel, field_validator
from uuid import UUID
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum, AttemptTypeEnum
from utils.enums.question_type_enum import QuestionTypeEnum


class AttemptStatsField(BaseModel):
    question_id: UUID
    status: AttemptStatsStatusEnum
    content: Optional[List[AnswerContent]]
    
    def to_dict(self) -> dict:
        return {
            'question_id': str(self.question_id),
            'status': self.status.value,
            'content': [content.to_dict() for content in self.content]
        }


class AttemptStatsCreate(BaseModel):
    user_id: UUID
    task_id: UUID
    stats: List[AttemptStatsField]
    result: float
    type: AttemptTypeEnum
    
    def to_dict(self) -> dict:
        return {
            'user_id': str(self.user_id),
            'task_id': str(self.task_id),
            'stats': [stat.to_dict() for stat in self.stats],
            'result': self.result,
            'type': self.type.value
        }
    
    @field_validator('result')
    def validate_result(cls, val: float) -> float:
        if not (0 <= val <= 100):
            raise ValueError('Результат должен быть в диапазоне от 0 до 100')
        return val


class GetAttemptStatsDto(BaseModel):
    attempt_id: UUID
    
    
class GetResultingAttemptStatsDto(BaseModel):
    task_id: UUID
    user_id: UUID


class GetTaskStatsDto(BaseModel):
    task_ids: Optional[List[UUID]] = []
    get_all: Optional[bool] = True
    

class GetAttemptStatsDetailedDto(BaseModel):
    task_id: UUID
    attempt_id: UUID
    user_id: UUID


class AttemptStatsFieldExtended(BaseModel):
    question_id: UUID
    order: int
    status: AttemptStatsStatusEnum
    user_content: List[AnswerContent]
    source_content: List[AnswerContent]
    question_type: QuestionTypeEnum
    question_title: str
    
    def to_dict(self) -> dict:
        return {
            'question_id': str(self.question_id),
            'status': self.status.value,
            'user_content': [content.to_dict() for content in self.user_content],
            'source_content': [content.to_dict() for content in self.source_content]
        }
    
    @field_validator('question_title')
    def validate_question_title(cls, val: str) -> str:
        if not (1 <= len(val) <= 1000):
            raise ValueError('Длина текста вопроса может быть от 1 до 1000')
        return val


class AttemptStatsDetailedResponse(BaseModel):
    user_initials: str
    result: float
    stats: List[AttemptStatsFieldExtended]
    task_title: str


class GetResultingStatsDto(BaseModel):
    task_id: UUID


class GetAttemptStatsResponse(BaseModel):
    stats: List[AttemptStatsField]
    result: float
    created_at: datetime.datetime
