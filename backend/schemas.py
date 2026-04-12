from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Any, Dict
import uuid

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FileBase(BaseModel):
    file_name: str
    status: str
    row_count: int
    column_count: int

class File(FileBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ColumnBase(BaseModel):
    column_name: str
    data_type: str
    null_count: int
    unique_count: int

class Column(ColumnBase):
    id: uuid.UUID
    file_id: uuid.UUID

    class Config:
        from_attributes = True

class Statistic(BaseModel):
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_dev: Optional[float] = None
    top_values: Optional[dict] = None

    class Config:
        from_attributes = True

class GraphDefinitionCreate(BaseModel):
    # When provided, the backend should update that graph instead of creating a new one.
    # Frontend uses string UUIDs, so keep it as str.
    id: Optional[str] = None
    graph_type: str
    # Some visuals (e.g. key influencers) may only set y_axis (Analyze); allow empty string.
    x_axis: Optional[str] = ""
    y_axis: Optional[str] = None
    aggregation: Optional[str] = "sum"
    options: Optional[Dict[str, Any]] = None

class GraphDefinition(BaseModel):
    id: uuid.UUID
    graph_type: str
    x_axis: str
    y_axis: Optional[str] = None
    aggregation: Optional[str] = None
    options: Optional[dict] = None

    class Config:
        from_attributes = True

class GraphDataRequest(BaseModel):
    graph_type: str
    x_axis: str
    y_axis: Optional[str] = None
    aggregation: Optional[str] = "sum"
    dimension_fields: Optional[List[str]] = None
    measure_fields: Optional[List[Dict[str, str]]] = None

class GraphDataResponse(BaseModel):
    labels: List[Any]
    values: List[Any]

class QueryRequest(BaseModel):
    prompt: str


class KeyInfluencersRequest(BaseModel):
    """Target column = what to explain (Analyze). Optional explain_by = single factor column; if omitted, scan eligible columns."""
    target_column: str
    explain_by: Optional[str] = None
    max_factors: int = 12
    max_cardinality: int = 35
