"""
encrypt.py - Steganography encryption module.

Hides a text message inside a PNG/BMP/TIFF image by encoding each character
into successive pixel colour channels.  The message length is stored in the
Red channel of pixel (0, 0) so the decoder knows exactly how many bytes to
read back.
"""

import logging
import os

import cv2

from config import DEFAULT_OUTPUT_IMAGE, MAX_MESSAGE_LENGTH, PASSWORD_FILE, SUPPORTED_IMAGE_FORMATS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class EncryptionError(Exception):
    """Raised when the encryption process cannot be completed."""


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------


def encrypt_message(
    image_path: str,
    message: str,
    password: str,
    output_path: str = DEFAULT_OUTPUT_IMAGE,
    password_file: str = PASSWORD_FILE,
) -> str:
    """Encrypt *message* into *image_path* and save the result to *output_path*.

    The function embeds each character of the message into the pixel data of
    the cover image.  A simple passcode is stored in *password_file* so that
    the companion :func:`decrypt.decrypt_message` can validate access.

    Parameters
    ----------
    image_path:
        Path to the source (cover) image.  Must be a lossless format such as
        PNG, BMP or TIFF so that pixel values are preserved exactly.
    message:
        Plaintext message to hide.  Maximum length is
        :data:`config.MAX_MESSAGE_LENGTH` characters.
    password:
        Passcode required to decrypt the message later.
    output_path:
        Destination path for the stego image.  Defaults to
        :data:`config.DEFAULT_OUTPUT_IMAGE`.
    password_file:
        Path where the password is persisted.  Defaults to
        :data:`config.PASSWORD_FILE`.

    Returns
    -------
    str
        Absolute path to the saved stego image.

    Raises
    ------
    EncryptionError
        If the image cannot be read, the message is too long, the message
        contains unsupported characters, or the output cannot be written.
    ValueError
        If any argument fails basic validation.
    """
    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------
    if not image_path or not isinstance(image_path, str):
        raise ValueError("image_path must be a non-empty string.")
    if not os.path.isfile(image_path):
        raise EncryptionError(f"Image file not found: {image_path}")
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in SUPPORTED_IMAGE_FORMATS:
        raise EncryptionError(
            f"Unsupported image format '{ext}'. "
            f"Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        )
    if not message:
        raise ValueError("message must not be empty.")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Message too long ({len(message)} chars). "
            f"Maximum allowed: {MAX_MESSAGE_LENGTH} characters."
        )
    if not password:
        raise ValueError("password must not be empty.")

    # Validate that all characters are encodable (ASCII 0-254)
    char_to_int = {chr(i): i for i in range(255)}
    for idx, char in enumerate(message):
        if char not in char_to_int:
            raise ValueError(
                f"Unsupported character {char!r} at position {idx}. "
                "Only ASCII characters (0–254) are supported."
            )

    # ------------------------------------------------------------------
    # Load image
    # ------------------------------------------------------------------
    img = cv2.imread(image_path)
    if img is None:
        raise EncryptionError(f"OpenCV could not read image: {image_path}")

    height, width, _ = img.shape
    max_capacity = height * width - 1  # first pixel is reserved for length
    if len(message) > max_capacity:
        raise EncryptionError(
            f"Image is too small to hold the message. "
            f"Capacity: {max_capacity} chars, message length: {len(message)}."
        )

    # ------------------------------------------------------------------
    # Encode message
    # ------------------------------------------------------------------
    # Store message length in the Red channel of pixel (0, 0)
    img[0, 0] = [len(message), 0, 0]

    z = 0
    for i, char in enumerate(message):
        n, m = divmod(i + 1, width)
        img[n, m, z] = char_to_int[char]
        z = (z + 1) % 3

    # ------------------------------------------------------------------
    # Write output image
    # ------------------------------------------------------------------
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)

    if not cv2.imwrite(output_path, img):
        raise EncryptionError(f"Failed to write stego image to: {output_path}")

    # ------------------------------------------------------------------
    # Persist password
    # ------------------------------------------------------------------
    password_dir = os.path.dirname(os.path.abspath(password_file))
    os.makedirs(password_dir, exist_ok=True)
    with open(password_file, "w", encoding="utf-8") as fh:
        fh.write(password)

    logger.info("Message encrypted and saved as %s", output_path)
    return os.path.abspath(output_path)


# ---------------------------------------------------------------------------
# Script entry-point (kept for backwards compatibility)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    _image_path = input("Enter image path: ").strip()
    _message = input("Enter secret message: ").strip()
    _password = input("Enter a passcode: ").strip()

    try:
        _output = encrypt_message(_image_path, _message, _password)
        print(f"Message encrypted and saved as {_output}")
    except (EncryptionError, ValueError) as exc:
        print(f"Encryption failed: {exc}")
