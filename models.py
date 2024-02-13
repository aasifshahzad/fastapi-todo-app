from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel, Enum
import enum

class CompletionStatus(enum.Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    PARTIAL_COMPLETE = "partial_complete"

class TaskOccurrence(enum.Enum):
    NON_OCCURRING = "non-occurring"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    
class TaskCategory(enum.Enum):
    NO_CATEGORY = "no_category"
    NAMAZ = "namaz"


class TaskBase(SQLModel):
    title: str = Field(index=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(),nullable=True))
    # updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True))
    

class Tasks(TaskBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    description: str | None = None
    category: TaskCategory = Field(sa_column=Column(Enum(TaskCategory)))
    occurrence: TaskOccurrence = Field(sa_column=Column(Enum(TaskOccurrence)))
    completion: CompletionStatus = Field(sa_column=Column(Enum(CompletionStatus)))
    


class TaskCreate(SQLModel):
    title: str | None = None
    description: str | None = None
    category: TaskCategory  | None = None
    occurrence: TaskOccurrence | None = None
    completion: CompletionStatus | None = None



class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completion: CompletionStatus | None = None
    occurrence: TaskOccurrence | None = None
    
class TaskResponse(TaskBase):
    description: str | None 
    category: TaskCategory | None 
    occurrence: TaskOccurrence | None
    completion: CompletionStatus | None


