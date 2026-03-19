"""
config.py - Centralised configuration for the Stego Project.

All hardcoded values are defined here so they can be changed in one place.
"""

import os

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

# Directory that contains this file (project root)
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

# Default file used to persist the encryption password
PASSWORD_FILE: str = os.path.join(BASE_DIR, "password.txt")

# Default output image produced by the encryption step
DEFAULT_OUTPUT_IMAGE: str = os.path.join(BASE_DIR, "encryptedImage.png")

# ---------------------------------------------------------------------------
# Supported image formats
# ---------------------------------------------------------------------------

SUPPORTED_IMAGE_FORMATS: tuple[str, ...] = (".png", ".bmp", ".tiff", ".tif")

# ---------------------------------------------------------------------------
# Encoding limits
# ---------------------------------------------------------------------------

# Maximum number of characters that can be hidden in a single image.
# The first pixel (index 0,0) stores the message length in the Red channel
# (uint8), so the practical upper limit is 255 characters.
MAX_MESSAGE_LENGTH: int = 255
