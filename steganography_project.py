# stego_tool.py - Combined Encode + Decode Script
from PIL import Image

def to_bin(data):
    return ''.join(format(ord(i), '08b') for i in data)

def to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        message += chr(int(c, 2))
        if message.endswith('###'):
            break
    return message[:-3]

def encode(img_path, message, output_path):
    img = Image.open(img_path)
    binary = to_bin(message + '###')
    pixels = list(img.getdata())

    new_pixels = []
    idx = 0

    for pixel in pixels:
        r, g, b = pixel[:3]
        if idx < len(binary):
            r = (r & ~1) | int(binary[idx])
            idx += 1
        if idx < len(binary):
            g = (g & ~1) | int(binary[idx])
            idx += 1
        if idx < len(binary):
            b = (b & ~1) | int(binary[idx])
            idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print("\n✅ Message hidden successfully in", output_path)

def decode(img_path):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary = ''

    for pixel in pixels:
        for color in pixel:
            binary += str(color & 1)

    message = to_text(binary)
    print("\n🔍 Hidden message:\n", message)

def main():
    print("""
    ===============================
      Steganography Tool
      Made by: Rishabh (2nd Yr)
    ===============================
    1. Hide Message in Image
    2. Reveal Message from Image
    3. Exit
    """)

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        img = input("Enter input image filename: ")
        msg = input("Enter the message to hide: ")
        out = input("Enter output image filename: ")
        encode(img, msg, out)
    elif choice == '2':
        img = input("Enter image filename to decode: ")
        decode(img)
    elif choice == '3':
        print("👋 Exiting...")
    else:
        print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()
