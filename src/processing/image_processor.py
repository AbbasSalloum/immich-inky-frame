from pathlib import Path
from PIL import Image, ImageOps


INKY_WIDTH = 800
INKY_HEIGHT = 480


class ImageProcessor:
    def __init__(self, output_dir: str = "cache/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_for_inky(self, image_path: Path) -> Path:
        image = Image.open(image_path).convert("RGB")

        processed = ImageOps.fit(
            image,
            (INKY_WIDTH, INKY_HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

        output_path = self.output_dir / "current.jpg"
        processed.save(output_path, quality=95)

        return output_path
