from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum, Boolean, Float, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from uuid import uuid4
from app.db.session import Base

class ProcessStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Chart(Base):
    __tablename__ = "charts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    original_filename = Column(String)
    gcs_uri = Column(String, nullable=False)
    content_type = Column(String)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String, nullable=False, default=ProcessStatus.PENDING.value)
    error_message = Column(Text)
    
    # Relationship with ExtractedData
    extracted_data = relationship("ExtractedData", back_populates="chart", cascade="all, delete-orphan")

class ExtractedData(Base):
    __tablename__ = "extracted_data"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chart_id = Column(String, ForeignKey("charts.id"), nullable=False, index=True)
    item_name = Column(String, nullable=False, index=True)
    item_value = Column(Text)
    extracted_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship with Chart
    chart = relationship("Chart", back_populates="extracted_data")
