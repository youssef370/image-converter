#!/usr/bin/env python3


from pathlib import Path

def get_file_extension(file_path: Path) -> str:
    ext = file_path.suffix.lstrip(".").lower()
    if ext == "jpg":
        ext = "jpeg"

    return ext

def build_output_path(*, path: Path | None, name: str, output_format: str):
    if not path:
        path = Path("./converted")
    path.mkdir(parents=True, exist_ok=True)
    
    return Path(f"{path}/{get_output_name(input_name=name, output_format=output_format)}")
    

def get_output_name(*, input_name: str | None, output_format: str):
    name = Path(input_name).stem if input_name else "output"

    return f"{name}.{output_format}"


if __name__ == "__main__":
    print(build_output_path(path=None,name="lorem", output_format="jpeg"))
