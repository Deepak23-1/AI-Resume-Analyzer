from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session


from app.utils.pdf_reader import extract_text_from_pdf
from app.database.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse, JobDescriptionRequest
from app.utils.gemini import analyze_resume, compare_resume_job


import os
import json
import shutil

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)



@router.post("/upload")
async def upload_resume(
    file: UploadFile=File(...),
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    if file.content_type !="application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)    


    resume = Resume(
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text,
        user_id=current_user.id
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
        "user_id": resume.user_id
    } 


@router.get(
        "/history",
        response_model=list[ResumeResponse]
)
def get_resume_history(
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):    

    resumes = (
        db.query(Resume).filter(Resume.user_id==current_user.id).all()
    )

    return resumes   


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse
)    
def get_resume(
    resume_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    resume = (
        db.query(Resume).filter(Resume.id==resume_id, Resume.user_id==current_user.id).first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail= "Resume not found"
        )
    
    return resume


@router.post("/analyze/{resume_id}")
def analyze_resume_api(
    resume_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user),
):
    resume = (
        db.query(Resume).filter(Resume.id==resume_id, Resume.user_id==current_user.id).first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # Return existing analysis if already available
    if resume.analysis:
        return {
            "resume_id": resume.id,
            "filename": resume.filename,
            "analysis": resume.analysis,
            "status": resume.analysis_status,
            "source": "database"
        }

    # Update status before starting analysis
    resume.analysis_status = "processing"
    db.commit()

    try:
        # Generate analysis using Gemini
        analysis = analyze_resume(resume.extracted_text)

        # Save analysis directly (JSONB column)
        resume.analysis = analysis
        resume.analysis_status = "completed"

        db.commit()
        db.refresh(resume)

        return {
            "resume_id": resume.id,
            "filename": resume.filename,
            "analysis": resume.analysis,
            "status": resume.analysis_status,
            "source": "gemini"
        }

    except Exception as e:
        resume.analysis_status = "failed"
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@router.post("/match/{resume_id}")
def match_resume(
    resume_id: int,
    request: JobDescriptionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    analysis = compare_resume_job(
        resume.extracted_text,
        request.job_description
    )

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "analysis": analysis
    }    