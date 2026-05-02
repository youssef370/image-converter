from PIL import Image
from pathlib import Path

from .globals import SUPPORTED_FORMATS, ENCODERS, CACHE_NAME
from .validators import validate_file
from .cache import Cache, CacheEntry, compute_hash_key

cache = Cache(CACHE_NAME)

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
        dict: Operation status and path to output file
    """
    if not validate_file(file_path, SUPPORTED_FORMATS):
        return {"status": "invalid", "file": str(file_path), "reason": "File invalid"}
    
    key = compute_hash_key(file_path=file_path, quality=quality, output_format=output_format)
    
    if cache.lookup(key):
        return {"status": "skipped", "file": str(file_path), "reason": "Already in cache"}
    
    try:
        with Image.open(file_path) as img:
            output = ENCODERS[output_format](img, quality, output_dir)
            print("ALL CLEAR")
            cache_item = CacheEntry(
                    input_file=file_path,
                    output_format=output_format,
                    output_file=output,
                    quality=quality
                    )
            print(cache_item)
            cache.add(cache_item)
            return {"status": "ok", "file": output, "reason": "SUCCESS"}
    except Exception as e:
        return {"status": "failed", "file": str(file_path), "reason": e}


def convert_folder_content(
    *,
    folder_path: Path,
    quality: int,
    output_format: str,
    output_dir: Path,
    recursive: bool = False,
):
    """Converts image files within a folder.
    Args:
        folder_path: Path of the folder the content of which should be converted.
        quality: Compression quality inputted by user, if no input then depends on the output file format
    """
    files = folder_path.rglob("*") if recursive else folder_path.iterdir()
    for file in files:
        if not file.is_file():
            continue

        relative_path = file.relative_to(folder_path)
        
        if not output_dir:
            output_dir = Path("./converted")

        target_dir = output_dir / relative_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)

        status = convert_file(
            file_path=file,
            output_format=output_format,
            quality=quality,
            output_dir=target_dir,
        )
        print(f"STATUS: {status['status']}, FILE: {status['file']}, REASON: {status['reason']}")
