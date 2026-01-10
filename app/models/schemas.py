from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum


# -----------------------------
# ENUMS (restrict allowed values)
# -----------------------------
class EntityType(str, Enum):
    review = "review"
    rfa = "rfa"
    issue = "issue"


class GenerationMode(str, Enum):
    ai = "ai"


# -----------------------------
# ENTITY SCHEMAS
# -----------------------------
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


# -----------------------------
# API REQUEST / RESPONSE MODELS
# -----------------------------
class GenerationRequest(BaseModel):
    """
    Incoming request from frontend.
    Depending on entity_type, fields will match ReviewFields, RFAFields, or IssueFields.
    """
    entity_type: EntityType
    generation_mode: GenerationMode = GenerationMode.ai
    fields: Union[ReviewFields, RFAFields, IssueFields]


class GenerationResponse(BaseModel):
    """
    Standard response returned by the generation endpoint.
    """
    success: bool
    generated_description: str
    generation_mode: GenerationMode
    editable: bool = True
    error: Optional[str] = None
