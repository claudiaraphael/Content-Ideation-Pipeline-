from pydantic import BaseModel
from typing import Optional

# Data classes/Pydantic models for validation and serialization
# which means they define the structure of requests and responses

# Model for video download request to Instagram servers
class VideoDownloadRequest(BaseModel):
    url: str
    id: Optional[int] = None


# Model for video download response from Instagram servers
class VideoDownloadResponse(BaseModel):
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    video_file: Optional[bytes] = None
