import base64
import json
import requests
from typing import Dict, List, Any, Optional
from app.core.config import settings
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel, Part
import vertexai

# Initialize Vertex AI
try:
    vertexai.init(project="your-project-id")
except:
    # Will be properly initialized in production
    pass

async def extract_chart_data(image_bytes: bytes) -> List[Dict[str, str]]:
    """
    Extract structured data from a medical chart image using Gemini API
    
    Args:
        image_bytes: Binary image data
        
    Returns:
        List of dictionaries with item_name and item_value pairs
    """
    try:
        # For REST API approach
        if settings.GEMINI_API_KEY:
            return await _extract_with_rest_api(image_bytes)
        # For Vertex AI SDK approach    
        else:
            return await _extract_with_vertex_ai(image_bytes)
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise e

async def _extract_with_rest_api(image_bytes: bytes) -> List[Dict[str, str]]:
    """
    Use Gemini REST API for extraction (API Key approach)
    """
    # Convert image to base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    # API endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-vision:generateContent"
    
    # Request payload
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "以下のカルテ画像から、次の項目を抽出してください：\n\n1. 主訴\n2. 現病歴\n3. 既往歴\n4. 家族歴\n5. 身体所見\n6. 検査所見\n7. 診断\n8. 治療計画\n\n抽出結果を以下のJSON形式で返してください。項目が見つからない場合は空文字列を返してください。\n{\"主訴\": \"\", \"現病歴\": \"\", \"既往歴\": \"\", \"家族歴\": \"\", \"身体所見\": \"\", \"検査所見\": \"\", \"診断\": \"\", \"治療計画\": \"\"}\n\n可読性を重視し、JSONデータのみを返してください。"
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ],
        "generation_config": {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 8192
        }
    }
    
    # Send request
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": settings.GEMINI_API_KEY
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    # Parse response
    response_data = response.json()
    
    # Extract text from response
    text = response_data["candidates"][0]["content"]["parts"][0]["text"]
    
    # Parse JSON from response text (the model might return additional text)
    try:
        # Try to find JSON in the response
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            json_text = text[json_start:json_end]
            data = json.loads(json_text)
        else:
            raise ValueError("No JSON found in response")
        
        # Convert to expected output format
        result = []
        for key, value in data.items():
            result.append({"item_name": key, "item_value": value})
        
        return result
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from response: {text}")
        raise e

async def _extract_with_vertex_ai(image_bytes: bytes) -> List[Dict[str, str]]:
    """
    Use Vertex AI for extraction (GCP Service Account approach)
    """
    # Convert image to bytes (already in bytes)
    
    try:
        # Initialize Gemini model
        model = GenerativeModel("gemini-2.5-pro-vision")
        
        # Create image part
        image_part = Part.from_data(mime_type="image/jpeg", data=image_bytes)
        
        # Create prompt text
        prompt = "以下のカルテ画像から、次の項目を抽出してください：\n\n1. 主訴\n2. 現病歴\n3. 既往歴\n4. 家族歴\n5. 身体所見\n6. 検査所見\n7. 診断\n8. 治療計画\n\n抽出結果を以下のJSON形式で返してください。項目が見つからない場合は空文字列を返してください。\n{\"主訴\": \"\", \"現病歴\": \"\", \"既往歴\": \"\", \"家族歴\": \"\", \"身体所見\": \"\", \"検査所見\": \"\", \"診断\": \"\", \"治療計画\": \"\"}\n\n可読性を重視し、JSONデータのみを返してください。"
        
        # Generate content
        response = model.generate_content([prompt, image_part], generation_config={
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 8192
        })
        
        # Extract text from response
        text = response.text
        
        # Parse JSON from response text
        try:
            # Try to find JSON in the response
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_text = text[json_start:json_end]
                data = json.loads(json_text)
            else:
                raise ValueError("No JSON found in response")
            
            # Convert to expected output format
            result = []
            for key, value in data.items():
                result.append({"item_name": key, "item_value": value})
            
            return result
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from response: {text}")
            raise e
        
    except Exception as e:
        print(f"Vertex AI error: {e}")
        raise e
