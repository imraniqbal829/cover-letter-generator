from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

# --- UPDATED IMPORTS ---
# Import from the specific service modules instead of a single services file.
from .services import cv_parser_service, llm_service, document_generator_service

router = APIRouter()

@router.post("/upload-cv/", response_model=schemas.UploadResponse)
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    1. Receives a CV file.
    2. Delegates parsing to the cv_parser_service.
    3. Saves the content to the database via CRUD layer.
    4. Returns the new CV's ID and a content preview.
    """
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or DOCX.")

    try:
        file_contents = await file.read()
        # --- UPDATED CALL ---
        parsed_text = cv_parser_service.parse_cv(file.filename, file_contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Could not parse the uploaded file.")

    cv = crud.create_cv(db=db, filename=file.filename, content=parsed_text)
    return {
        "cv_id": cv.id,
        "filename": cv.filename,
        "content_preview": parsed_text[:250] + "..." if len(parsed_text) > 250 else parsed_text
    }

@router.post("/generate/", response_model=schemas.GenerateResponse)
def generate_cover_letter(request: schemas.GenerateRequest, db: Session = Depends(get_db)):
    """
    1. Takes a cv_id and job_description.
    2. Fetches CV content from the DB via CRUD layer.
    3. Delegates cover letter generation to the llm_service.
    4. Returns the generated text.
    """
    cv = crud.get_cv(db, cv_id=request.cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    try:
        # --- UPDATED CALL ---
        letter_text = llm_service.generate_cover_letter(
            cv_content=cv.content,
            job_description=request.job_description
        )
        return {"cover_letter": letter_text}
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while generating the letter.")

@router.post("/download/")
async def download_file(request: schemas.DownloadRequest):
    """
    1. Takes generated text and a file type.
    2. Delegates file creation to the document_generator_service.
    3. Streams the file back to the user.
    """
    if request.file_type not in ['pdf', 'docx']:
        raise HTTPException(status_code=400, detail="Invalid file type specified. Use 'pdf' or 'docx'.")

    try:
        if request.file_type == 'docx':
            # --- UPDATED CALL ---
            file_stream = document_generator_service.create_docx_file(request.text)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = "CoverLetter.docx"
        else: # 'pdf'
            # --- UPDATED CALL ---
            file_stream = document_generator_service.create_pdf_file(request.text)
            media_type = "application/pdf"
            filename = "CoverLetter.pdf"

        return StreamingResponse(
            file_stream,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create the downloadable file.")
