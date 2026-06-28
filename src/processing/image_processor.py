from pathlib import Path
from PIL import Image, ImageOps, ImageFilter


INKY_WIDTH = 800
INKY_HEIGHT = 480


class ImageProcessor:
    def __init__(self, output_dir: str = "cache/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_for_inky(self, image_path: Path) -> Path:
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image).convert("RGB")

        width, height = image.size

        if width >= height:
            processed = self._process_landscape(image)
        else:
            processed = self._process_portrait(image)

        output_path = self.output_dir / "current.jpg"
        processed.save(output_path, quality=95)

        return output_path

    def _process_landscape(self, image: Image.Image) -> Image.Image:
        return ImageOps.fit(
            image,
            (INKY_WIDTH, INKY_HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

    def _process_portrait(self, image: Image.Image) -> Image.Image:
        background = ImageOps.fit(
            image,
            (INKY_WIDTH, INKY_HEIGHT),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

        background = background.filter(ImageFilter.GaussianBlur(radius=18))

        foreground = ImageOps.contain(
            image,
            (INKY_WIDTH, INKY_HEIGHT),
            method=Image.Resampling.LANCZOS,
        )

        x = (INKY_WIDTH - foreground.width) // 2
        y = (INKY_HEIGHT - foreground.height) // 2

        background.paste(foreground, (x, y))

        return background
