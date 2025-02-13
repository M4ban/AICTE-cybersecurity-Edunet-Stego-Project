import cv2
import os

def decrypt_message(image_path):
    if not os.path.exists(image_path):
        print("Error: Encrypted image file not found.")
        return

    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not open or find the image.")
        return

    c = {i: chr(i) for i in range(255)}

    try:
        with open("password.txt", "r") as f:
            stored_password = f.read().strip()
    except FileNotFoundError:
        print("Error: Password file not found.")
        return

    entered_password = input("Enter passcode for decryption: ").strip()

    if entered_password != stored_password:
        print("YOU ARE NOT AUTHORIZED!")
        return

    # Retrieve message length from the first pixel
    msg_length = img[0, 0, 0]  # Read from Red channel
    
    n, m, z = 0, 0, 0
    message = ""

    for i in range(msg_length):  # Read only stored characters
        n, m = divmod(i + 1, img.shape[1])
        message += c[img[n, m, z]]
        z = (z + 1) % 3

    print("Decrypted message:", message)

if __name__ == "__main__":
    image_path = input("Enter encrypted image path: ").strip()
    decrypt_message(image_path)
