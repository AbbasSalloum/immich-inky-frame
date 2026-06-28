from config import load_config
from utils.logger import setup_logger


def main() -> None:
    logger = setup_logger()
    logger.info("Starting Immich Inky Frame")

    config = load_config()

    logger.info("Config loaded successfully")
    logger.info(f"Immich URL: {config.immich_base_url}")
    logger.info(f"Album: {config.immich_album_name}")
    logger.info(f"Photo mode: {config.photo_mode}")
    logger.info(f"Refresh minutes: {config.refresh_minutes}")


if __name__ == "__main__":
    main()
