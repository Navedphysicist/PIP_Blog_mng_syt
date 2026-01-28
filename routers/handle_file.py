from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import EmailStr, HttpUrl
import os
import shutil

router = APIRouter(
    prefix="/file",
    tags=['file']
)

FILES_DIR = "files"  # Directory where uploaded files are stored


@router.post("/upload")
async def uplaod_file(upload_file: UploadFile = File(...)):
    # Create files directory if it doesn't exist
    os.makedirs(FILES_DIR, exist_ok=True)

    # Extract filename to prevent directory traversal attacks
    filename = os.path.basename(upload_file.filename)
    path = os.path.join(FILES_DIR, filename)

    with open(path, "wb") as buffer:
        # Efficiently copy file content to disk
        shutil.copyfileobj(upload_file.file, buffer)

    await upload_file.close()  # Properly close the uploaded file handle

    return {
        "filename": filename,
        "message": "File Uploaded successfully"
    }


@router.get("/download")
def download_file(name: str):
    # Sanitize filename to prevent directory traversal attacks
    filename = os.path.basename(name)
    path = os.path.join(FILES_DIR, filename)

    return FileResponse(
        path,
        # Generic binary content type for file downloads
        media_type="application/octet-stream",
        filename=filename
    )


# import axios from "axios"

# const submitApplication = async () => {
#   const formData = new FormData()

#   formData.append("name", name)
#   formData.append("email", email)
#   formData.append("phone", phone)
#   formData.append("address", address)
#   formData.append("experience", experience)
#   formData.append("linkedin_url", linkedinUrl)
#   formData.append("cv", cvFile)

#   try {
#     const response = await axios.post(
#       "http://localhost:8000/apply",
#       formData
#     )

#     console.log(response.data)
#   } catch (error) {
#     console.error(error.response?.data || error.message)
#   }
# }


@router.post("/apply")
def apply(
    name: str = Form(...),  # Required form field for applicant name
    email: EmailStr = Form(...),  # Email validation using Pydantic EmailStr
    phone: str = Form(...),
    address: str = Form(...),
    experience: int = Form(...),  # Years of experience as integer
    # Optional LinkedIn URL with validation
    linkedin_url: HttpUrl | None = Form(None),
    cv: UploadFile = File(...)  # Required CV file upload
):
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "cv_filename": cv.filename,  # Return uploaded CV filename
        "cv_type": cv.content_type  # Return CV MIME type
    }
