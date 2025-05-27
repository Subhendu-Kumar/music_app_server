from uuid import uuid4
import cloudinary.uploader
from utils.cloudinary_util import *
from utils.database_util import get_db
from utils.jwt_util import verify_token
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from utils.song_util import validate_file, ALLOWED_AUDIO_TYPES, ALLOWED_IMAGE_TYPES

router = APIRouter(prefix="/song", tags=["Songs"])


@router.post("/upload", status_code=201)
async def song_upload(
    db=Depends(get_db),
    artist: str = Form(...),
    song_name: str = Form(...),
    hex_color: str = Form(...),
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    user_data: dict = Depends(verify_token),
):
    try:
        userId = user_data.get("user")["id"]
        if not userId:
            raise HTTPException(status_code=400, detail="Invalid access")
        # validate_file(song, ALLOWED_AUDIO_TYPES)
        # validate_file(thumbnail, ALLOWED_IMAGE_TYPES)
        if not artist or not song_name or not hex_color:
            raise HTTPException(status_code=400, detail="Missing required fields.")
        existing_song = await db.song.find_first(
            where={"song_name": song_name, "userId": userId}
        )
        if existing_song:
            raise HTTPException(
                status_code=409,
                detail="A song with this name already exists for the user.",
            )
        song_id = str(uuid4())
        song_res = cloudinary.uploader.upload(
            song.file, resource_type="auto", folder=f"songs/{song_id}"
        )
        if not song_res:
            raise HTTPException(status_code=500, detail="song upload failed")
        thumbnail_res = cloudinary.uploader.upload(
            thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
        )
        if not song_res:
            raise HTTPException(status_code=500, detail="thumbnail upload failed")
        song_url = song_res.get("secure_url")
        thumbnail_url = thumbnail_res.get("secure_url")
        new_song = await db.song.create(
            data={
                "id": song_id,
                "song": song_url,
                "thumbnail": thumbnail_url,
                "artist": artist,
                "song_name": song_name,
                "hex_color": hex_color,
                "userId": userId,
            }
        )
        return {"message": "Song uploaded successfully", "song": new_song}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
