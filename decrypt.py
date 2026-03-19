"""
decrypt.py - Steganography decryption module.

Extracts a hidden text message from a stego image that was produced by
:mod:`encrypt`.  Access is protected by a passcode stored in a password file
alongside the stego image.
"""

import logging
import os

import cv2

from config import PASSWORD_FILE, SUPPORTED_IMAGE_FORMATS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class DecryptionError(Exception):
    """Raised when the decryption process cannot be completed."""


class AuthenticationError(DecryptionError):
    """Raised when the provided passcode does not match the stored one."""


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------


def decrypt_message(
    image_path: str,
    password: str,
    password_file: str = PASSWORD_FILE,
) -> str:
    """Extract and return the hidden message from *image_path*.

    Parameters
    ----------
    image_path:
        Path to the stego image created by :func:`encrypt.encrypt_message`.
    password:
        Passcode to authenticate the decryption request.
    password_file:
        Path to the file containing the stored password.  Defaults to
        :data:`config.PASSWORD_FILE`.

    Returns
    -------
    str
        The plaintext message that was hidden in the image.

    Raises
    ------
    DecryptionError
        If the image file cannot be read or the password file is missing.
    AuthenticationError
        If *password* does not match the stored passcode.
    ValueError
        If any argument fails basic validation.
    """
    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------
    if not image_path or not isinstance(image_path, str):
        raise ValueError("image_path must be a non-empty string.")
    if not os.path.isfile(image_path):
        raise DecryptionError(f"Encrypted image file not found: {image_path}")
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in SUPPORTED_IMAGE_FORMATS:
        raise DecryptionError(
            f"Unsupported image format '{ext}'. "
            f"Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        )
    if not password:
        raise ValueError("password must not be empty.")

    # ------------------------------------------------------------------
    # Load image
    # ------------------------------------------------------------------
    img = cv2.imread(image_path)
    if img is None:
        raise DecryptionError(f"OpenCV could not read image: {image_path}")

    # ------------------------------------------------------------------
    # Authenticate
    # ------------------------------------------------------------------
    if not os.path.isfile(password_file):
        raise DecryptionError(
            f"Password file not found: {password_file}. "
            "Ensure you have run encryption first."
        )
    with open(password_file, "r", encoding="utf-8") as fh:
        stored_password = fh.read().strip()

    if password != stored_password:
        raise AuthenticationError("Incorrect passcode – access denied.")

    # ------------------------------------------------------------------
    # Decode message
    # ------------------------------------------------------------------
    int_to_char = {i: chr(i) for i in range(255)}

    msg_length = int(img[0, 0, 0])  # length stored in Red channel of (0,0)
    width = img.shape[1]

    message_chars: list[str] = []
    z = 0
    for i in range(msg_length):
        n, m = divmod(i + 1, width)
        message_chars.append(int_to_char[int(img[n, m, z])])
        z = (z + 1) % 3

    message = "".join(message_chars)
    logger.info("Message successfully decrypted from %s", image_path)
    return message


# ---------------------------------------------------------------------------
# Script entry-point (kept for backwards compatibility)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    _image_path = input("Enter encrypted image path: ").strip()
    _password = input("Enter passcode for decryption: ").strip()

    try:
        _message = decrypt_message(_image_path, _password)
        print(f"Decrypted message: {_message}")
    except AuthenticationError:
        print("YOU ARE NOT AUTHORIZED!")
    except (DecryptionError, ValueError) as exc:
        print(f"Decryption failed: {exc}")

