"""
main.py - Command-line interface for the Stego Project.

Usage examples
--------------
Encrypt a message::

    python main.py encrypt --image mypic.png --output encryptedImage.png

Decrypt a message::

    python main.py decrypt --image encryptedImage.png
"""

import argparse
import logging
import sys

from config import DEFAULT_OUTPUT_IMAGE, PASSWORD_FILE
from decrypt import AuthenticationError, DecryptionError, decrypt_message
from encrypt import EncryptionError, encrypt_message


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def _configure_logging(verbose: bool) -> None:
    """Configure the root logger.

    Parameters
    ----------
    verbose:
        When *True* the log level is set to DEBUG; otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------


def _handle_encrypt(args: argparse.Namespace) -> int:
    """Handle the *encrypt* sub-command.

    Prompts for the secret message and passcode, then delegates to
    :func:`encrypt.encrypt_message`.

    Returns
    -------
    int
        Exit code (0 = success, 1 = failure).
    """
    message = input("Enter secret message: ").strip()
    password = input("Enter a passcode: ").strip()

    try:
        output = encrypt_message(
            image_path=args.image,
            message=message,
            password=password,
            output_path=args.output,
            password_file=args.password_file,
        )
        print(f"Message encrypted and saved as: {output}")
        return 0
    except (EncryptionError, ValueError) as exc:
        logging.error("Encryption failed: %s", exc)
        return 1


def _handle_decrypt(args: argparse.Namespace) -> int:
    """Handle the *decrypt* sub-command.

    Prompts for the passcode and delegates to
    :func:`decrypt.decrypt_message`.

    Returns
    -------
    int
        Exit code (0 = success, 1 = failure).
    """
    password = input("Enter passcode for decryption: ").strip()

    try:
        message = decrypt_message(
            image_path=args.image,
            password=password,
            password_file=args.password_file,
        )
        print(f"Decrypted message: {message}")
        return 0
    except AuthenticationError:
        print("YOU ARE NOT AUTHORIZED!")
        return 1
    except (DecryptionError, ValueError) as exc:
        logging.error("Decryption failed: %s", exc)
        return 1


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="stego",
        description="Image-based steganography tool – hide and retrieve text messages in images.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG) logging.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # -- encrypt sub-command -------------------------------------------------
    enc_parser = subparsers.add_parser(
        "encrypt",
        help="Hide a message inside an image.",
        description="Embed a secret message into a cover image using steganography.",
    )
    enc_parser.add_argument(
        "--image", "-i",
        required=True,
        metavar="PATH",
        help="Path to the cover (source) image.",
    )
    enc_parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT_IMAGE,
        metavar="PATH",
        help=f"Path for the output stego image (default: {DEFAULT_OUTPUT_IMAGE}).",
    )
    enc_parser.add_argument(
        "--password-file",
        default=PASSWORD_FILE,
        metavar="PATH",
        help=f"File where the passcode is stored (default: {PASSWORD_FILE}).",
    )
    enc_parser.set_defaults(func=_handle_encrypt)

    # -- decrypt sub-command -------------------------------------------------
    dec_parser = subparsers.add_parser(
        "decrypt",
        help="Extract a hidden message from a stego image.",
        description="Read back a secret message that was embedded in a stego image.",
    )
    dec_parser.add_argument(
        "--image", "-i",
        required=True,
        metavar="PATH",
        help="Path to the stego (encrypted) image.",
    )
    dec_parser.add_argument(
        "--password-file",
        default=PASSWORD_FILE,
        metavar="PATH",
        help=f"File containing the stored passcode (default: {PASSWORD_FILE}).",
    )
    dec_parser.set_defaults(func=_handle_decrypt)

    return parser


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Parse *argv* and dispatch to the appropriate handler.

    Parameters
    ----------
    argv:
        Command-line arguments.  Defaults to :data:`sys.argv` when *None*.

    Returns
    -------
    int
        Exit code.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
