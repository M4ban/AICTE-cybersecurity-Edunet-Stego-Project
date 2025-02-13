import cv2
import os

def encrypt_message(image_path, output_path, message, password):
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not open or find the image.")
        return
    
    d = {chr(i): i for i in range(255)}
    
    n, m, z = 0, 0, 0

    # Store message length in the first pixel
    msg_length = len(message)
    img[0, 0] = [msg_length, 0, 0]  # Store length in Red channel
    
    for i, char in enumerate(message):
        n, m = divmod(i + 1, img.shape[1])  # Ensure within bounds
        img[n, m, z] = d[char]
        z = (z + 1) % 3
    
    cv2.imwrite(output_path, img)
    print(f"Message encrypted and saved as {output_path}")

    with open("password.txt", "w") as f:
        f.write(password)

if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()
    output_path = "mypic.png"  # Define output_path here
    message = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    
    encrypt_message(image_path, output_path, message, password)
    
    # Open the encrypted image (Windows)
    if os.path.exists(output_path):
        os.system(f"start {output_path}")  # Use 'xdg-open' for Linux or 'open' for macOS
    else:
        print("Error: Encrypted image file not found.")
        