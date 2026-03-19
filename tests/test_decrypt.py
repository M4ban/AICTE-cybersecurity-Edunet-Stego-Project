"""
tests/test_decrypt.py - Unit tests for the decrypt module.
"""

import os
import tempfile
import unittest

import numpy as np
import cv2

from encrypt import encrypt_message
from decrypt import AuthenticationError, DecryptionError, decrypt_message


def _make_test_image(path: str, width: int = 100, height: int = 100) -> None:
    """Write a plain white PNG to *path*."""
    img = np.full((height, width, 3), 255, dtype=np.uint8)
    cv2.imwrite(path, img)


class TestDecryptMessage(unittest.TestCase):
    """Tests for :func:`decrypt.decrypt_message`."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp()
        self.cover_path = os.path.join(self.tmp_dir, "cover.png")
        self.stego_path = os.path.join(self.tmp_dir, "stego.png")
        self.password_file = os.path.join(self.tmp_dir, "password.txt")
        _make_test_image(self.cover_path)

    def _encrypt(self, message: str, password: str) -> None:
        encrypt_message(
            self.cover_path, message, password,
            output_path=self.stego_path, password_file=self.password_file,
        )

    # ------------------------------------------------------------------
    # Happy-path tests
    # ------------------------------------------------------------------

    def test_round_trip_simple(self) -> None:
        self._encrypt("Hello", "secret")
        result = decrypt_message(self.stego_path, "secret", self.password_file)
        self.assertEqual(result, "Hello")

    def test_round_trip_full_ascii(self) -> None:
        message = "ABCXYZ abcxyz 0123!@#"
        self._encrypt(message, "pass123")
        result = decrypt_message(self.stego_path, "pass123", self.password_file)
        self.assertEqual(result, message)

    def test_round_trip_max_length(self) -> None:
        message = "Z" * 255
        self._encrypt(message, "pw")
        result = decrypt_message(self.stego_path, "pw", self.password_file)
        self.assertEqual(result, message)

    # ------------------------------------------------------------------
    # Error-path tests
    # ------------------------------------------------------------------

    def test_wrong_password_raises(self) -> None:
        self._encrypt("Secret", "correct")
        with self.assertRaises(AuthenticationError):
            decrypt_message(self.stego_path, "wrong", self.password_file)

    def test_missing_image_raises(self) -> None:
        with self.assertRaises(DecryptionError):
            decrypt_message("/no/such/file.png", "pw", self.password_file)

    def test_missing_password_file_raises(self) -> None:
        self._encrypt("Hi", "pw")
        with self.assertRaises(DecryptionError):
            decrypt_message(self.stego_path, "pw", "/no/such/password.txt")

    def test_empty_password_raises(self) -> None:
        self._encrypt("Hi", "pw")
        with self.assertRaises(ValueError):
            decrypt_message(self.stego_path, "", self.password_file)

    def test_empty_image_path_raises(self) -> None:
        with self.assertRaises(ValueError):
            decrypt_message("", "pw", self.password_file)

    def test_unsupported_format_raises(self) -> None:
        jpg_path = os.path.join(self.tmp_dir, "stego.jpg")
        _make_test_image(jpg_path)
        with self.assertRaises(DecryptionError):
            decrypt_message(jpg_path, "pw", self.password_file)


if __name__ == "__main__":
    unittest.main()
