import os
import uuid
import aiofiles
from typing import Dict
from fastapi import UploadFile

VIDEO_STORAGE = "videos"
os.makedirs(VIDEO_STORAGE, exist_ok=True)

upload_status: Dict[str, str] = {}

async def initiate_video_upload(background_tasks, file: UploadFile):
    unique_id = str(uuid.uuid4())
    upload_status[unique_id] = "in progress"
    background_tasks.add_task(save_video, unique_id, file)
    return {"unique_id": unique_id}

async def save_video(unique_id: str, file: UploadFile):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    try:
        async with aiofiles.open(video_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        upload_status[unique_id] = "completed"
    except Exception:
        upload_status[unique_id] = "failed"

def get_upload_status(unique_id: str):
    return upload_status.get(unique_id)

def get_video_path(unique_id: str):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    if os.path.exists(video_path):
        return video_path
    return None

def delete_video_file(unique_id: str):
    video_path = os.path.join(VIDEO_STORAGE, f"{unique_id}.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
        upload_status.pop(unique_id, None)
        return True
    return False
