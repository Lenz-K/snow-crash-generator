import qrcode
from PIL import Image

BLACK = 0
WHITE = 255
TEXT_ENCODING = 'UTF-8'

# Use these variables to adapt the generated image:
X_RESOLUTION = 1920
Y_RESOLUTION = 1080
BOX_SIZE = 8  # The width and height of one bit in the image
BACKGROUND = BLACK
IMAGE_FILE_NAME = 'snow_crash.png'
TEXT_INPUT_FILE_NAMES = ['snow-crash-generator.py', 'README.md']
DO_INCLUDE_QR_CODE = True
QR_CODE_CONTENTS = ['https://github.com/Lenz-K/snow-crash-generator']


def main():
    # The picture will be generated with one pixel per bit of data.
    # Later it will be scaled up to the specified BOX_SIZE.
    scaled_down_x_resolution = int(X_RESOLUTION / BOX_SIZE)
    scaled_down_y_resolution = int(Y_RESOLUTION / BOX_SIZE)
    # Create the array and fill it with the background color
    data = bytearray([BACKGROUND for _ in range(scaled_down_x_resolution * scaled_down_y_resolution)])

    # The offset in the array to write the next data to
    offset = 0
    # Iterate over the specified files
    for filename in TEXT_INPUT_FILE_NAMES:
        with open(filename, 'rt') as file:
            text = '\n'.join(file.readlines())
        # Get the binary data of the text file
        text_bytes = text.encode(TEXT_ENCODING)
        # Write the binary data into the array that will create the image
        data[offset:offset + len(text_bytes)] = text_bytes
        # Update the offset
        offset += len(text_bytes)

    # Create an image from the array
    img = Image.frombytes('1', (scaled_down_x_resolution, scaled_down_y_resolution), bytes(data))
    # Scale the image up to the desired resolution
    img = img.resize((X_RESOLUTION, Y_RESOLUTION))

    if DO_INCLUDE_QR_CODE:
        x = X_RESOLUTION
        for content in QR_CODE_CONTENTS:
            qr_img, qr_img_size = create_qr_code(content)
            # Paste the QR codes into the image starting in the lower right corner
            x -= qr_img_size
            img.paste(qr_img, (x, Y_RESOLUTION - qr_img_size))
    # Save the image
    img.save(IMAGE_FILE_NAME)


def create_qr_code(content):
    """
    Creates a QR code and returns it.
    The second return value is the width (also the height) of the QR code in pixels.
    """
    qr = qrcode.QRCode(border=1, box_size=BOX_SIZE, error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(content)
    qr.make()
    return qr.make_image(), len(qr.get_matrix()[0]) * BOX_SIZE


if __name__ == '__main__':
    main()
