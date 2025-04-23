from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.db.models import Chart, ExtractedData, ProcessStatus
from app.schemas.chart import ChartCreate, ExtractedDataCreate

async def create_chart_record(db: AsyncSession, chart_id: str, filename: str, gcs_uri: str, content_type: str) -> Chart:
    """
    Create a new chart record in the database
    
    Args:
        db: Database session
        chart_id: Unique identifier for the chart
        filename: Original filename
        gcs_uri: GCS or MinIO URI for the image
        content_type: MIME type of the image
        
    Returns:
        Created Chart record
    """
    chart = Chart(
        id=chart_id,
        original_filename=filename,
        gcs_uri=gcs_uri,
        content_type=content_type,
        status=ProcessStatus.PENDING.value
    )
    
    db.add(chart)
    await db.commit()
    await db.refresh(chart)
    return chart

async def update_chart_status(db: AsyncSession, chart_id: str, status: str, error_message: Optional[str] = None) -> Chart:
    """
    Update the status of a chart record
    
    Args:
        db: Database session
        chart_id: Chart ID to update
        status: New status value
        error_message: Optional error message (for failed status)
        
    Returns:
        Updated Chart record
    """
    stmt = (
        update(Chart)
        .where(Chart.id == chart_id)
        .values(status=status, error_message=error_message if error_message else None)
        .returning(Chart)
    )
    result = await db.execute(stmt)
    chart = result.scalar_one_or_none()
    
    await db.commit()
    return chart

async def get_chart_by_id(db: AsyncSession, chart_id: str) -> Optional[Chart]:
    """
    Get a chart record by its ID
    
    Args:
        db: Database session
        chart_id: Chart ID to retrieve
        
    Returns:
        Chart record or None if not found
    """
    stmt = select(Chart).where(Chart.id == chart_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_chart_with_extracted_data(db: AsyncSession, chart_id: str) -> Optional[Chart]:
    """
    Get a chart record with its extracted data by chart ID
    
    Args:
        db: Database session
        chart_id: Chart ID to retrieve
        
    Returns:
        Chart record with extracted_data loaded or None if not found
    """
    stmt = (
        select(Chart)
        .where(Chart.id == chart_id)
        .options(sqlalchemy.orm.selectinload(Chart.extracted_data))
    )
    
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_extracted_data_records(db: AsyncSession, chart_id: str, data_items: List[Dict[str, str]]) -> List[ExtractedData]:
    """
    Create multiple extracted data records for a chart
    
    Args:
        db: Database session
        chart_id: ID of the chart these items belong to
        data_items: List of dictionaries with item_name and item_value pairs
        
    Returns:
        List of created ExtractedData records
    """
    # Create ExtractedData objects
    extracted_data_records = [
        ExtractedData(
            chart_id=chart_id,
            item_name=item["item_name"],
            item_value=item["item_value"]
        )
        for item in data_items
    ]
    
    # Add all records to the session
    db.add_all(extracted_data_records)
    await db.commit()
    
    # Refresh all records to get their IDs
    for record in extracted_data_records:
        await db.refresh(record)
    
    return extracted_data_records
