import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    immich_base_url: str
    immich_api_key: str
    immich_album_name: str
    photo_mode: str
    refresh_minutes: int


def load_config() -> Config:
    load_dotenv()

    required_vars = [
        "IMMICH_BASE_URL",
        "IMMICH_API_KEY",
        "IMMICH_ALBUM_NAME",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return Config(
        immich_base_url=os.getenv("IMMICH_BASE_URL", "").rstrip("/"),
        immich_api_key=os.getenv("IMMICH_API_KEY", ""),
        immich_album_name=os.getenv("IMMICH_ALBUM_NAME", ""),
        photo_mode=os.getenv("PHOTO_MODE", "random"),
        refresh_minutes=int(os.getenv("REFRESH_MINUTES", "60")),
    )
