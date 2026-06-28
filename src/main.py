from config import load_config
from immich.client import ImmichClient
from immich.downloader import PhotoDownloader
from utils.logger import setup_logger
from processing.image_processor import ImageProcessor

def main() -> None:
    logger = setup_logger()
    logger.info("Starting Immich Inky Frame")

    config = load_config()

    client = ImmichClient(
        base_url=config.immich_base_url,
        api_key=config.immich_api_key,
    )

    logger.info("Connecting to Immich...")

    album = client.find_album_by_name(config.immich_album_name)

    if not album:
        logger.error(f"Album not found: {config.immich_album_name}")
        return

    album_id = album["id"]
    logger.info(f"Found album: {album.get('albumName')}")

    assets = client.get_album_assets(album_id)

    image_assets = [
        asset for asset in assets
        if asset.get("type") == "IMAGE"
    ]

    logger.info(f"Image assets in album: {len(image_assets)}")

    downloader = PhotoDownloader(client)
    cached_photos = downloader.fill_cache(
        image_assets=image_assets,
        target_size=config.cache_target_size,
        logger=logger,
    )

    selected_photo = downloader.pick_random_cached_photo()

    if not selected_photo:
        logger.error("No cached photos available")
        return

    logger.info(f"Selected cached photo: {selected_photo}")
    processor = ImageProcessor()
    processed_photo = processor.process_for_inky(selected_photo)

    logger.info(f"Processed photo saved to: {processed_photo}")


if __name__ == "__main__":
    main()
