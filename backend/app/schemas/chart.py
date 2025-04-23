from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ProcessStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ChartCreateResponse(BaseModel):
    chart_id: str
    status: str = ProcessStatus.PENDING.value
    message: str

class ChartStatusResponse(BaseModel):
    chart_id: str
    status: str
    error_message: Optional[str] = None
    
class ExtractedDataItem(BaseModel):
    item_name: str
    item_value: Optional[str] = None

class ExtractedDataCreate(ExtractedDataItem):
    chart_id: str

class ChartResultResponse(BaseModel):
    chart_id: str
    original_filename: Optional[str] = None
    gcs_uri: Optional[str] = None
    status: str
    extracted_data: Optional[List[ExtractedDataItem]] = None
    message: Optional[str] = None
    error_message: Optional[str] = None

# For internal use
class ChartCreate(BaseModel):
    id: str
    original_filename: str
    gcs_uri: str
    content_type: str
    status: str = ProcessStatus.PENDING.value
