import cloudinary
import cloudinary.uploader
import os
from typing import Optional

# Load config from environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_file(file_path: str, folder: Optional[str] = None, resource_type: str = "auto") -> dict:
    """
    Upload a file to Cloudinary (image, video, pdf, etc.).
    :param file_path: Local file path
    :param folder: Optional Cloudinary folder
    :param resource_type: "image", "video", "raw", or "auto"
    """
    return cloudinary.uploader.upload(file_path, folder=folder, resource_type=resource_type)

def upload_file_bytes(file_bytes: bytes, filename: str, folder: Optional[str] = None, resource_type: str = "auto") -> dict:
    """
    Upload a file from memory (e.g. FastAPI UploadFile).
    """
    return cloudinary.uploader.upload(file_bytes, folder=folder, public_id=filename, resource_type=resource_type)

def get_file_url(public_id: str, resource_type: str = "auto") -> str:
    """
    Get a direct URL for the uploaded file.
    """
    from cloudinary.utils import cloudinary_url
    url, _ = cloudinary_url(public_id, resource_type=resource_type)
    return url

def delete_file(public_id: str, resource_type: str = "auto") -> dict:
    """
    Delete a file from Cloudinary by its public_id.
    """
    return cloudinary.uploader.destroy(public_id, resource_type=resource_type)
