from PIL import Image
from pathlib import Path

from .globals import SUPPORTED_FORMATS, ENCODERS
from .validators import validate_file


def convert_file(
    *, file_path: Path, output_format: str, quality: int, output_dir: Path | None
):
    """Create the output directory and execute the encoding function based user's format input
    Args:
        file_path: Path of the file to convert
        format: Format to which the input file should be converted
        quality: Compression quality inputted by user, if no input then depends on the output file format
        output_dir (optional): Destination directory where output file will be stored
    Returns:
        str: Path to the output file
    """
    if not validate_file(file_path, SUPPORTED_FORMATS):
        return {"status": "invalid", "file": str(file_path)}

    if not output_dir:
        output_dir = file_path.parent / "converted"

    output_dir.mkdir(parents=True, exist_ok=True)

    ext = output_format
    try:
        with Image.open(file_path) as img:
            output = ENCODERS[ext](img, quality, output_dir)
            return {"status": "ok", "file": output}
    except Exception:
        print("Cannot open image")
        return {"status": "failed", "file": str(file_path)}


def convert_folder_content(
    *, folder_path: Path, quality: int, output_format: str, output_dir: Path
):
    """Converts image files within a folder.
    Args:
        folder_path: Path of the folder the content of which should be converted.
        quality: Compression quality inputted by user, if no input then depends on the output file format
    """
    for file in folder_path.iterdir():
        if file.is_file():
            status = convert_file(
                file_path=file,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir,
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")
