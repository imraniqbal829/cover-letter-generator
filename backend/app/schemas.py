from pydantic import BaseModel

class GenerateRequest(BaseModel):
    cv_id: int
    job_description: str

class GenerateResponse(BaseModel):
    cover_letter: str

class UploadResponse(BaseModel):
    cv_id: int
    filename: str
    content_preview: str

class DownloadRequest(BaseModel):
    text: str
    file_type: str # 'pdf' or 'docx'