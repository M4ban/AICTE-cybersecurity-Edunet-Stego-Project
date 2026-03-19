# AICTE Cybersecurity Edunet Stego Project 2025

## 🖼️ Data Hiding Using Steganography in Images

Securely hide and retrieve text messages within images using pixel-level steganography.

---

## 🌟 Introduction

This project implements **image-based steganography** – a technique for securely hiding text messages within the pixel data of a cover image.  By subtly modifying individual pixel colour channels the hidden message remains invisible to the human eye, enabling covert data transmission without raising suspicion.

> **Use-cases**: cybersecurity research, confidential communication, digital forensics, and academic demonstration.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🔒 **Lossless embedding** | Uses PNG/BMP/TIFF to preserve pixel values exactly |
| 🔑 **Passcode protection** | Only authorised users can decrypt the hidden message |
| 🎨 **Dynamic pixel encoding** | Characters distributed across R/G/B channels |
| ⚡ **Fast retrieval** | O(n) decode – proportional only to message length |
| 🌐 **Cross-platform** | Works on Windows, Linux, and macOS |
| 🛡️ **Input validation** | Explicit errors for bad paths, oversized messages, unsupported formats |
| 🖥️ **CLI interface** | `main.py` provides a full argparse-based command-line tool |

---

## 📂 Project Structure

```
AICTE-cybersecurity-Edunet-Stego-Project/
├── config.py          # Centralised configuration (paths, limits, formats)
├── encrypt.py         # Encryption module + backwards-compatible __main__
├── decrypt.py         # Decryption module + backwards-compatible __main__
├── main.py            # Unified CLI (argparse + logging)
├── requirements.txt   # Python dependencies
├── .gitignore
├── mypic.png          # Sample cover image
├── tests/
│   ├── __init__.py
│   ├── test_encrypt.py
│   └── test_decrypt.py
└── README.md
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or newer
- pip

### Steps

```sh
# 1. Clone the repository
git clone https://github.com/M4ban/AICTE-cybersecurity-Edunet-Stego-Project.git
cd AICTE-cybersecurity-Edunet-Stego-Project

# 2. (Optional but recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Option A – Unified CLI (`main.py`)

#### 🔐 Encrypt a message

```sh
python main.py encrypt --image mypic.png --output encryptedImage.png
```

You will be prompted for:
- **Secret message** – the text to hide (max 255 characters)
- **Passcode** – password required to decrypt later

#### 🔓 Decrypt a message

```sh
python main.py decrypt --image encryptedImage.png
```

You will be prompted for the **Passcode**.

#### All CLI options

```
usage: stego [-h] [-v] COMMAND ...

positional arguments:
  COMMAND
    encrypt   Hide a message inside an image.
    decrypt   Extract a hidden message from a stego image.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose (DEBUG) logging.
```

---

### Option B – Individual scripts (backwards-compatible)

```sh
# Encrypt
python encrypt.py

# Decrypt
python decrypt.py
```

---

## 📂 Example Workflow

### 🔐 Encryption

```
$ python main.py encrypt --image mypic.png --output encryptedImage.png
Enter secret message: Hello123
Enter a passcode: 1234
Message encrypted and saved as: /path/to/encryptedImage.png
```

### 🔓 Decryption

```
$ python main.py decrypt --image encryptedImage.png
Enter passcode for decryption: 1234
Decrypted message: Hello123
```

---

## 🧪 Running Tests

```sh
python -m pytest tests/ -v
```

---

## 🔐 Security Considerations

| Consideration | Status |
|---|---|
| `password.txt` committed to version control | ❌ Excluded by `.gitignore` |
| Hardcoded file paths | ✅ Removed – all paths configurable via `config.py` or CLI flags |
| Message integrity | ⚠️ No cryptographic integrity check; the passcode only restricts access |
| Password storage | ⚠️ Stored in plaintext – suitable for demonstration only |
| OS command injection | ✅ Removed `os.system("start …")` call |

> **Note**: This project is designed for educational purposes.  For production use, consider encrypting the message with AES before embedding it, and replacing the plaintext password file with a proper key-derivation scheme.

---

## 🔮 Future Scope

- 🔐 **AES/RSA encryption** – encrypt message before embedding for double protection
- 📁 **Multi-format support** – hide documents or other binary data
- 🤖 **AI-resistant steganography** – techniques to evade steganalysis tools
- 🎥 **Video steganography** – extend the concept to video files
- ☁️ **Web interface** – browser-based tool for easier access

---

## 📄 License

This project was developed as part of the AICTE Cybersecurity Edunet programme 2025.

