from .encoders import encode_jpeg, encode_avif, encode_png, encode_webp

FORMATS = {
    "jpeg": {
        "encoder": encode_jpeg,
        "quality": 75,
    },
    "avif": {
        "encoder": encode_avif,
        "quality": 85,
    },
    "webp": {
        "encoder": encode_webp,
        "quality": 80,
    },
    "png": {
        "encoder": encode_png,
        "quality": 75,
    },
}

SUPPORTED_FORMATS = set(FORMATS.keys())

ENCODERS = {k: v["encoder"] for k, v in FORMATS.items()}

DEFAULT_QUALITIES = {k: v["quality"] for k, v in FORMATS.items()}
