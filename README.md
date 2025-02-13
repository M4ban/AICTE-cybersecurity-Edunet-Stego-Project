# AICTE Cybersecurity Edunet Stego Project 2025  

## 🖼️ Data Hiding Using Steganography in Images  
Securely hide and retrieve text messages within images using advanced steganography techniques.  

## 🌟 Introduction  
This project implements image-based steganography, a powerful technique for securely hiding and retrieving text messages within an image. By subtly modifying pixel values, the hidden message remains invisible to the human eye, ensuring secure data transmission without raising suspicion. Perfect for applications in cybersecurity, confidential communication, and digital forensics.  

## ✨ Features  
- 🔒 **Lossless Data Embedding**: Uses the PNG format to prevent image distortion.  
- 🔑 **Passcode-Based Security**: Ensures only authorized users can decrypt the hidden message.  
- 🎨 **Dynamic Pixel Encoding**: Distributes data across image pixels for enhanced secrecy.  
- ⚡ **Quick & Efficient Retrieval**: Optimized decryption process for fast message extraction.  
- 🌐 **Cross-Platform Compatibility**: Runs on Windows, Linux, and macOS without special dependencies.  

## 🛠️ Installation  
### Prerequisites  
- Python 3.x  
- OpenCV (`cv2`)  
- NumPy  

### Install Dependencies  
Run the following command to install the required libraries:  

```sh
pip install opencv-python numpy
```

## 🚀 Usage  
### 🔐 Encryption (Hiding Data in an Image)  
Run the encryption script:  

```sh
python encrypt.py
```

#### Provide the following inputs:  
- **Image path**: Path to the image where the message will be embedded.  
- **Secret message**: The message you want to hide.  
- **Passcode**: A password to secure the message.  

**Example:**  
```plaintext
Enter image path: mypic.png
Enter secret message: Hello123
Enter a passcode: 1234
```
The encrypted image will be saved as `encryptedImage.png`.  

### 🔓 Decryption (Extracting Hidden Data)  
Run the decryption script:  

```sh
python decrypt.py
```

#### Provide the following inputs:  
- **Encrypted image path**: Path to the encrypted image (`encryptedImage.png`).  
- **Passcode**: The password used during encryption.  

**Example:**  
```plaintext
Enter encrypted image path: encryptedImage.png
Enter the original passcode: 1234
```
If the passcode matches, the hidden message will be displayed:  

```plaintext
Decrypted message: Hello123
```

## 📂 Example Workflow  
### 🔐 Encryption  
```plaintext
Enter image path: mypic.png
Enter secret message: Hello123
Enter a passcode: 1234
Message encrypted and saved as encryptedImage.png
```

### 🔓 Decryption  
```plaintext
Enter encrypted image path: encryptedImage.png
Enter the original passcode: 1234
Decrypted message: Hello123
```

## 🔮 Future Scope  
- 🔐 **Advanced Cryptographic Security**: Integrate AES/RSA encryption before embedding.  
- 📁 **Support for Other File Types**: Extend the tool to hide documents, audio, or images.  
- 🤖 **AI-Resistant Steganography**: Develop techniques to counteract AI-based detection.  
- 🎥 **Video-Based Steganography**: Expand the concept to hide data in video files.  
- ☁️ **Cloud-Based Secure Communication**: Build a web-based tool for secure communication.  
