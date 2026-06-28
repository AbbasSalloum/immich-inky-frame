import random
from pathlib import Path


class PhotoDownloader:
    def __init__(self, client, cache_dir: str = "cache/photos"):
        self.client = client
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cached_photos(self) -> list[Path]:
        return sorted(
            [
                path for path in self.cache_dir.iterdir()
                if path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
            ]
        )

    def fill_cache(self, image_assets: list[dict], target_size: int, logger) -> list[Path]:
        cached = self.get_cached_photos()

        if len(cached) >= target_size:
            logger.info(f"Cache already has {len(cached)} photos")
            return cached

        needed = target_size - len(cached)
        logger.info(f"Cache needs {needed} more photos")

        random.shuffle(image_assets)

        downloaded = 0

        for asset in image_assets:
            if downloaded >= needed:
                break

            asset_id = asset.get("id")
            filename = asset.get("originalFileName") or f"{asset_id}.jpg"

            if not asset_id:
                continue

            safe_filename = f"{asset_id}_{filename}".replace("/", "_")
            output_path = self.cache_dir / safe_filename

            if output_path.exists():
                continue

            logger.info(f"Downloading {filename}")

            try:
                image_bytes = self.client.download_asset(asset_id)
                output_path.write_bytes(image_bytes)
                downloaded += 1
                logger.info(f"Saved {output_path}")
            except Exception as error:
                logger.error(f"Failed to download {filename}: {error}")

        return self.get_cached_photos()

    def pick_random_cached_photo(self) -> Path | None:
        cached = self.get_cached_photos()

        if not cached:
            return None

        return random.choice(cached)
