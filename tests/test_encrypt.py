"""
tests/test_encrypt.py - Unit tests for the encrypt module.
"""

import os
import tempfile
import unittest

import numpy as np
import cv2

from encrypt import EncryptionError, encrypt_message


def _make_test_image(path: str, width: int = 100, height: int = 100) -> None:
    """Write a plain white PNG to *path*."""
    img = np.full((height, width, 3), 255, dtype=np.uint8)
    cv2.imwrite(path, img)


class TestEncryptMessage(unittest.TestCase):
    """Tests for :func:`encrypt.encrypt_message`."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp()
        self.image_path = os.path.join(self.tmp_dir, "cover.png")
        self.output_path = os.path.join(self.tmp_dir, "stego.png")
        self.password_file = os.path.join(self.tmp_dir, "password.txt")
        _make_test_image(self.image_path)

    # ------------------------------------------------------------------
    # Happy-path tests
    # ------------------------------------------------------------------

    def test_returns_output_path(self) -> None:
        result = encrypt_message(
            self.image_path, "Hello", "secret",
            output_path=self.output_path, password_file=self.password_file,
        )
        self.assertEqual(result, os.path.abspath(self.output_path))

    def test_output_image_exists(self) -> None:
        encrypt_message(
            self.image_path, "Hello", "secret",
            output_path=self.output_path, password_file=self.password_file,
        )
        self.assertTrue(os.path.isfile(self.output_path))

    def test_password_file_written(self) -> None:
        encrypt_message(
            self.image_path, "Hello", "my_password",
            output_path=self.output_path, password_file=self.password_file,
        )
        with open(self.password_file, "r") as fh:
            self.assertEqual(fh.read().strip(), "my_password")

    def test_max_length_message(self) -> None:
        """A 255-character message should be accepted."""
        message = "A" * 255
        result = encrypt_message(
            self.image_path, message, "pw",
            output_path=self.output_path, password_file=self.password_file,
        )
        self.assertTrue(os.path.isfile(result))

    # ------------------------------------------------------------------
    # Error-path tests
    # ------------------------------------------------------------------

    def test_missing_image_raises(self) -> None:
        with self.assertRaises(EncryptionError):
            encrypt_message(
                "/nonexistent/path.png", "Hi", "pw",
                output_path=self.output_path, password_file=self.password_file,
            )

    def test_empty_message_raises(self) -> None:
        with self.assertRaises(ValueError):
            encrypt_message(
                self.image_path, "", "pw",
                output_path=self.output_path, password_file=self.password_file,
            )

    def test_empty_password_raises(self) -> None:
        with self.assertRaises(ValueError):
            encrypt_message(
                self.image_path, "Hi", "",
                output_path=self.output_path, password_file=self.password_file,
            )

    def test_message_too_long_raises(self) -> None:
        with self.assertRaises(ValueError):
            encrypt_message(
                self.image_path, "A" * 256, "pw",
                output_path=self.output_path, password_file=self.password_file,
            )

    def test_unsupported_format_raises(self) -> None:
        jpg_path = os.path.join(self.tmp_dir, "cover.jpg")
        _make_test_image(jpg_path)
        with self.assertRaises(EncryptionError):
            encrypt_message(
                jpg_path, "Hi", "pw",
                output_path=self.output_path, password_file=self.password_file,
            )

    def test_empty_image_path_raises(self) -> None:
        with self.assertRaises(ValueError):
            encrypt_message(
                "", "Hi", "pw",
                output_path=self.output_path, password_file=self.password_file,
            )


if __name__ == "__main__":
    unittest.main()
