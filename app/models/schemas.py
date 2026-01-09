from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum


class EntityType(str, Enum):
    review = "review"
    rfa = "rfa"
    issue = "issue"


class GenerationMode(str, Enum):
    ai = "ai"


class ReviewFields(BaseModel):
    name: str
    start_date: str
    due_date: str
    workflow: str
    priority: str

    parent_review: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    checklist: Optional[List[str]] = None


class RFAFields(BaseModel):
    name: str
    request_date: str
    due_date: str
    workflow: str
    priority: str
    checklist: Optional[List[str]] = None


class IssueFields(BaseModel):
    name: str
    issue_type: str
    placement: str
    root_cause: str
    start_date: str
    due_date: str
    workflow: str

    location: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None


class GenerationRequest(BaseModel):
    entity_type: EntityType
    generation_mode: GenerationMode = GenerationMode.ai
    fields: Union[ReviewFields, RFAFields, IssueFields]


class GenerationResponse(BaseModel):
    success: bool
    generated_description: str
    generation_mode: GenerationMode
    editable: bool = True
    error: Optional[str] = None
