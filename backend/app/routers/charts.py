from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
import csv
from io import StringIO

from app.core.auth import verify_api_key
from app.db.session import get_db
from app.db.models import ProcessStatus
import app.services.db_service as db_service
import app.services.gcs_service as gcs_service
import app.services.gemini_service as gemini_service
from app.schemas.chart import ChartCreateResponse, ChartStatusResponse, ChartResultResponse, ExtractedDataItem
from app.core.config import settings
from app.tasks.process_chart import run_extraction_task

router = APIRouter(
    prefix="/charts",
    tags=["Charts"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("", response_model=ChartCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_chart(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a medical chart image and start the processing"""
    # Validate file type
    if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Use JPEG or PNG."
        )
    
    # Validate file size (read into memory to check size)
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"File size exceeds limit ({settings.MAX_FILE_SIZE // 1024 // 1024}MB)."
        )
    
    # Reset file position after reading
    await file.seek(0)
    
    # Generate a unique ID for this chart
    chart_id = str(uuid.uuid4())
    
    try:
        # Upload the file to GCS/MinIO
        gcs_uri = await gcs_service.upload_file_to_gcs(file, chart_id, file.content_type)
        
        # Create a record in the database
        chart = await db_service.create_chart_record(db, chart_id, file.filename, gcs_uri, file.content_type)
        
        # Add background task for processing
        background_tasks.add_task(run_extraction_task, chart_id, gcs_uri, str(db.bind.url))
        
        return ChartCreateResponse(
            chart_id=chart_id,
            status=chart.status,
            message="Chart processing started."
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process upload: {str(e)}"
        )

@router.get("/{chart_id}/status", response_model=ChartStatusResponse)
async def get_chart_status(
    chart_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """Get the processing status of a chart"""
    chart = await db_service.get_chart_by_id(db, chart_id)
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    return ChartStatusResponse(
        chart_id=chart_id,
        status=chart.status,
        error_message=chart.error_message
    )

@router.get("/{chart_id}", response_model=ChartResultResponse)
async def get_chart_result(
    chart_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """Get the processing result of a chart"""
    chart = await db_service.get_chart_with_extracted_data(db, chart_id)
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    # For completed status, return extracted data
    if chart.status == ProcessStatus.COMPLETED.value:
        extracted_data = [
            ExtractedDataItem(
                item_name=data.item_name,
                item_value=data.item_value
            )
            for data in chart.extracted_data
        ]
        
        return ChartResultResponse(
            chart_id=chart_id,
            original_filename=chart.original_filename,
            gcs_uri=chart.gcs_uri,
            status=chart.status,
            extracted_data=extracted_data
        )
    
    # For non-completed status, return status information
    return ChartResultResponse(
        chart_id=chart_id,
        status=chart.status,
        message="Processing not completed or failed.",
        error_message=chart.error_message
    )

@router.get("/{chart_id}/csv")
async def download_csv(
    chart_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """Download the extracted data as a CSV file"""
    chart = await db_service.get_chart_with_extracted_data(db, chart_id)
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    # Check if processing is complete
    if chart.status != ProcessStatus.COMPLETED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chart processing not completed"
        )
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["項目名", "内容"])
    
    # Write data rows
    for data in chart.extracted_data:
        writer.writerow([data.item_name, data.item_value])
    
    # Prepare response with CSV content
    response = Response(content=output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=chart_{chart_id}.csv"
    response.headers["Content-Type"] = "text/csv"
    
    return response
