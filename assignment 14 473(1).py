from PIL import Image
import numpy as np

# Constants for RGB channels
RED, GREEN, BLUE = 0, 1, 2

def message_to_binary(message):
    """Convert a string message into a binary representation."""
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")

def encode_image(img_path, message, output_path):
    """Encode a message into an image using LSB steganography."""
    try:
        # Load the image
        img = Image.open(img_path)
        img = img.convert('RGB')  # Ensure image is in RGB format
        
        # Convert the message to binary
        binary_message = message_to_binary(message) + '1111111111111110'  # Delimiter to indicate end of message
        data_index = 0
        
        # Convert image to numpy array for efficient processing
        img_array = np.array(img)
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                pixel = img_array[i, j]
                for k in (RED, GREEN, BLUE):
                    if data_index < len(binary_message):
                        # Modify the LSB of pixel component
                        img_array[i, j, k] = int(message_to_binary(pixel[k])[:-1] + binary_message[data_index], 2)
                        data_index += 1
        
        # Convert array back to image and save
        encoded_img = Image.fromarray(img_array)
        encoded_img.save(output_path)
        
        print("Message encoded and image saved to", output_path)
    except Exception as e:
        print("Error encoding message:", e)

# Adjust the paths according to your system
message = "Secret Message"
img_path = 'C:/Users/Administrator/Desktop/monalisa.bmp'  # Corrected path
output_path = 'C:/Users/Administrator/Desktop/monalisa_encoded.bmp'  # Output path

encode_image(img_path, message, output_path)
