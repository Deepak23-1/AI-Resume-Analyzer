from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    extracted_text: str
    user_id: int


    class  Config:
        from_attributes = True