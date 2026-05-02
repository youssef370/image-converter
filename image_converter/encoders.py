from .utils import build_output_path

from pathlib import Path
from PIL import Image

def encode_avif(img: Image, quality: int, output_dir: Path):
    """Encode image file to AVIF
    Args:
        img: Image object to convert to AVIF
        quality: Compression quality inputted by user, if no input then quality=85
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    output = build_output_path(path=output_dir, name=img.filename, output_format="avif")
    img.save(output, format="AVIF", quality=max(30, int(quality * 0.7)))

    return output


def encode_webp(img: Image, quality: int, output_dir: Path):
    """Encode image file to WEBP
    Args:
        img: Image object to convert to WEBP
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    output = build_output_path(path=output_dir, name=img.filename, output_format="webp")
    img.convert("RGB").save(output, format="WEBP", quality=quality, method=6)

    return output


def encode_jpeg(img: Image, quality: int, output_dir: Path):
    """Encode image file to JPEG
    Args:
        img: Image object to convert to JPEG
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    output = build_output_path(path=output_dir, name=img.filename, output_format="jpeg")
    img.convert("RGB").save(
        output,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
    )

    return output


def encode_png(img: Image, quality: int, output_dir: Path):
    """Encode image file to PNG
    Args:
        img: Image object to convert to JPEG
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    compression = round((quality / 100) * 9)
    output = build_output_path(path=output_dir, name=img.filename, output_format="jpeg")
    img.convert("RGBA").save(output, format="PNG", compress_level=compression)

    return output
