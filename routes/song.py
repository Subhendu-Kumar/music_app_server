from uuid import uuid4
import cloudinary.uploader
from utils.cloudinary_util import *
from utils.database_util import get_db
from utils.jwt_util import verify_token
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status

# from utils.song_util import validate_file, ALLOWED_AUDIO_TYPES, ALLOWED_IMAGE_TYPES

router = APIRouter(prefix="/song", tags=["Songs"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access"
            )
        # validate_file(song, ALLOWED_AUDIO_TYPES)
        # validate_file(thumbnail, ALLOWED_IMAGE_TYPES)
        if not artist or not song_name or not hex_color:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields.",
            )
        existing_song = await db.song.find_first(
            where={"song_name": song_name, "userId": userId}
        )
        if existing_song:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A song with this name already exists for the user.",
            )
        song_id = str(uuid4())
        song_res = cloudinary.uploader.upload(
            song.file, resource_type="auto", folder=f"songs/{song_id}"
        )
        if not song_res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="song upload failed",
            )
        thumbnail_res = cloudinary.uploader.upload(
            thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
        )
        if not song_res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="thumbnail upload failed",
            )
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_all_songs(db=Depends(get_db), user_data: dict = Depends(verify_token)):
    try:
        songs = await db.song.find_many(order={"createdAt": "desc"})
        if not songs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No songs found"
            )
        return songs
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/fav", status_code=status.HTTP_200_OK)
async def get_favorite_songs_only(
    db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        if not userId:
            raise HTTPException(status_code=400, detail="Invalid access")
        favorites = await db.favorite.find_many(
            where={"userId": userId},
            include={"song": True},
            order={"createdAt": "desc"},
        )

        # Extract just the songs
        songs = [favorite.song for favorite in favorites]
        return songs

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching favorite songs: {str(e)}",
        )


@router.post("/fav", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    song_id: str, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        if not userId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access"
            )

        # Check if song exists
        song = await db.song.find_unique(where={"id": song_id})
        if not song:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Song not found"
            )

        # Check if already favorited
        existing_favorite = await db.favorite.find_unique(
            where={
                "userId_songId": {
                    "userId": userId,
                    "songId": song_id,
                }
            }
        )

        if existing_favorite:
            # Delete favorite
            await db.favorite.delete(
                where={"userId_songId": {"userId": userId, "songId": song_id}}
            )
            return {"message": False}
        else:
            # Create favorite
            await db.favorite.create(
                data={"userId": userId, "songId": song_id},
                include={"song": True},
            )
            return {"message": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding favorite: {str(e)}",
        )


@router.delete("/fav/{song_id}", status_code=status.HTTP_200_OK)
async def remove_favorite(
    song_id: str, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        if not userId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access"
            )
        # Check if favorite exists
        favorite = await db.favorite.find_unique(
            where={"userId_songId": {"userId": userId, "songId": song_id}}
        )

        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found"
            )

        # Delete favorite
        await db.favorite.delete(
            where={"userId_songId": {"userId": userId, "songId": song_id}}
        )

        return {"message": "Song removed from favorites"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing favorite: {str(e)}",
        )
