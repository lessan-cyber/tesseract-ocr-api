from fastapi import FastAPI, UploadFile, HTTPException
from ocr_processor import OCRResponse
from PIL import Image
import pytesseract
import pdf2image
import io
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class OCRResponse(BaseModel):
    filename: str
    pages: list[dict]


@app.get("/")
async def root():
    return {"message": "Welcome to the OCR API"}


@app.post("/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile, lang: str = "fra"):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf","image/jpg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Validate language
    available_langs = pytesseract.get_languages(config='')
    if not all(language in available_langs for language in lang.split('+')):
        raise HTTPException(status_code=400, detail=f"Unsupported language(s). Available: {available_langs}")

    try:
        # Read file content
        content = await file.read()

        # Handle PDF or image
        if file.content_type == "application/pdf":
            images = pdf2image.convert_from_bytes(content)
        else:
            images = [Image.open(io.BytesIO(content))]

        # Extract text with specified language
        result = []
        for img in images:
            text = pytesseract.image_to_string(img, lang=lang)
            result.append({"page": len(result) + 1, "text": text.strip()})

        return {"filename": file.filename, "pages": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")



