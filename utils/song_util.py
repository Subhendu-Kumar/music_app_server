from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = 10
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/mp3", "audio/wav"}
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def validate_file(
    file: UploadFile, allowed_types: set, max_size_mb: int = MAX_FILE_SIZE_MB
):
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed types: {', '.join(allowed_types)}",
        )

    file.file.seek(0, 2)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > max_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size_mb:.2f}MB. Max allowed size is {max_size_mb}MB.",
        )
