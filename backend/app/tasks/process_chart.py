import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.services import gcs_service, gemini_service, db_service
from app.db.models import ProcessStatus
from app.core.config import settings
import traceback

async def run_extraction_task(chart_id: str, gcs_uri: str, db_url: str):
    """
    Background task to process a chart image
    
    Args:
        chart_id: ID of the chart to process
        gcs_uri: URI of the image in storage
        db_url: Database URL for creating a new session
    """
    # Convert URL to async format if needed
    if db_url.startswith('postgresql://') and not db_url.startswith('postgresql+asyncpg://'):
        db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://')
    elif db_url.startswith('sqlite://') and not db_url.startswith('sqlite+aiosqlite://'):
        db_url = db_url.replace('sqlite://', 'sqlite+aiosqlite://')
    
    # Create a new engine and session for this task
    engine = create_async_engine(db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    try:
        # Create a new session for this task
        async with async_session() as session:
            # Update status to processing
            await db_service.update_chart_status(
                session, 
                chart_id, 
                ProcessStatus.PROCESSING.value
            )
            
            # Get image from storage
            image_bytes = await gcs_service.get_file_from_gcs(gcs_uri)
            
            # Extract data using Gemini API
            extracted_data = await gemini_service.extract_chart_data(image_bytes)
            
            # Save extracted data to database
            await db_service.create_extracted_data_records(session, chart_id, extracted_data)
            
            # Update chart status to completed
            await db_service.update_chart_status(
                session, 
                chart_id, 
                ProcessStatus.COMPLETED.value
            )
            
    except Exception as e:
        print(f"Error processing chart {chart_id}: {str(e)}")
        print(traceback.format_exc())
        
        # Update chart status to failed with error message
        async with async_session() as session:
            await db_service.update_chart_status(
                session, 
                chart_id, 
                ProcessStatus.FAILED.value, 
                str(e)
            )
