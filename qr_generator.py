import qrcode
import argparse
from PIL import Image, ImageDraw, ImageFont


def generate_qr_code(qr_data,
                     appearance_text=None,
                     logo_path=None,
                     version=1,
                     save_path="qr.png",
                     error_correction=qrcode.constants.ERROR_CORRECT_H,
                     box_size=10,
                     border=2,
                     border_corner_radius=0,
                     inner_border_size=0,
                     outer_border_size=0,
                     logo_size=(48, 48),
                     ):
    """
    Generate a QR code with a centered space for a logo overlay.

    :param outer_border_size: outer border size of the qr code with logo and text
    :param inner_border_size: inner border size of the qr code with logo
    :param border_corner_radius: radius of the border corners.
    :param qr_data: The data (URL, text, etc.) to encode in the QR code.
    :param appearance_text: The text to be displayed in the QR code. If None, the QR code will not have a text displayed.
    :param logo_path: Path to the logo image. If None, the QR code will not have a logo.
    :param version: Version of the QR code (controls the size).
    :param error_correction: Error correction level (higher for larger logos).
    :param box_size: Size of each box in the QR code grid.
    :param border: Width of the border (in boxes).
    :param logo_size: The fixed size of the logo (width, height).
    :param save_path: The file path where the QR code will be saved.
    :return: None
    """

    qr, qr_img = _create_basic_qr_img(border, box_size, qr_data, error_correction, version)

    if logo_path is not None:
        qr_img = _add_logo_to_qr_img(logo_path, qr, qr_img, logo_size, box_size)

    qr_img = _create_black_rounded_corners_on_white_bg_for_qr_img(qr_img, border_corner_radius, inner_border_size)

    if appearance_text is not None:
        qr_img = _add_rounded_border_and_text(qr_img, appearance_text, border_corner_radius, outer_border_size)

    # Save the generated QR code
    qr_img.save(save_path)
    print(f"QR code saved to {save_path}")


def _create_basic_qr_img(border, box_size, qr_data, error_correction, version):
    # Create the QR code object
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border
    )
    # Add the data to the QR code
    qr.add_data(qr_data)
    qr.make(fit=True)
    # Create an image from the QR code
    qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')
    return qr, qr_img


def _add_logo_to_qr_img(logo_path, qr, qr_img, logo_size, box_size):
    if logo_path:
        # Open the logo image
        logo = Image.open(logo_path)

        # Resize the logo to the specified fixed size (48x48)
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

        # Calculate the position to center the logo on the QR code
        qr_width, qr_height = qr_img.size
        logo_width, logo_height = logo_size

        # Calculate position to center the logo
        logo_position = (
            (qr_width - logo_width) // 2,
            (qr_height - logo_height) // 2
        )

        # Get QR code matrix
        qr_matrix = qr.get_matrix()
        matrix_size = len(qr_matrix)

        # Adjust the QR code's matrix to create enough white space in the center
        qr_matrix = qr.get_matrix()
        quiet_zone_size = 15  # You can adjust this ratio as necessary

        # Clear the center of the QR matrix to avoid overlapping the logo
        for row in range(quiet_zone_size, matrix_size - quiet_zone_size):
            for col in range(quiet_zone_size, matrix_size - quiet_zone_size):
                qr_matrix[row][col] = 0

        # Create a new image from the modified matrix
        new_qr_img = Image.new("RGB", qr_img.size, "white")
        for y in range(len(qr_matrix)):
            for x in range(len(qr_matrix[y])):
                if qr_matrix[y][x]:
                    box = (x * box_size, y * box_size,
                           (x + 1) * box_size, (y + 1) * box_size)
                    new_qr_img.paste("black", box)

        # Paste the logo onto the QR code with enough clear space
        new_qr_img.paste(logo, logo_position, mask=logo)
        return new_qr_img
    return qr_img


def _create_black_rounded_corners_on_white_bg_for_qr_img(qr_img, corner_radius, border_size):
    # Get QR code size and add padding for text and border
    qr_width, qr_height = qr_img.size
    new_width = qr_width + 2 * border_size
    new_height = qr_height + 2 * border_size

    # Create a new image with black background
    new_img = Image.new("RGB", (new_width, new_height), "black")

    # Create a mask for rounded corners
    mask = Image.new("L", (new_width, new_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, new_width, new_height], corner_radius, fill=255)

    # Create a white background image
    white_bg = Image.new("RGB", (new_width, new_height), "white")

    # Paste the white background onto the new image using the mask
    new_img.paste(white_bg, (0, 0), mask)

    # Paste the QR code onto the new image
    new_img.paste(qr_img, (border_size, border_size))
    return new_img


def _create_white_rounded_corners_on_black_bg_for_qr_img(qr_img, new_width, new_height, border_size, corner_radius):
    # Create a new image with black background
    new_img = Image.new("RGB", (new_width, new_height), "black")

    # Create a mask for rounded corners
    mask = Image.new("L", (new_width, new_height), "white")
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, new_width, new_height], corner_radius, fill=0)

    # Create a white background image
    white_bg = Image.new("RGB", (new_width, new_height), "white")

    # Paste the white background onto the new image using the mask
    new_img.paste(white_bg, (0, 0), mask)

    # Paste the QR code onto the new image
    new_img.paste(qr_img, (border_size, border_size))
    return new_img


def _add_rounded_border_and_text(qr_img, appearance_text, border_corner_radius, border_size):
    # Get QR code size and add padding for text and border
    qr_width, qr_height = qr_img.size
    text_padding = 70  # Increased to accommodate larger font
    new_width = qr_width + 2 * border_size
    new_height = qr_height + 2 * border_size + text_padding

    new_img = _create_white_rounded_corners_on_black_bg_for_qr_img(qr_img, new_width, new_height, border_size,
                                                                   border_corner_radius)

    # Add text (URL) below the QR code
    draw = ImageDraw.Draw(new_img)
    font_size = 25  # Adjust this value to change the font size
    try:
        font = ImageFont.truetype("Verdana.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("Helvetica.ttf", font_size)
            except IOError:
                font = ImageFont.load_default().font_variant(size=font_size)

    # Define the position and add the text
    text_bbox = font.getbbox(appearance_text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = ((new_width - text_width) // 2, qr_height + border_size + (text_padding - text_height) // 2)
    draw.text(text_position, appearance_text, fill="white", font=font)

    return new_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QR code with logo and text")
    parser.add_argument("--data", required=True, help="URL or data for the QR code")
    parser.add_argument("--text", required=False, help="Text to appear below the QR code")
    parser.add_argument("--logo", required=False, help="Path to the logo image")
    parser.add_argument("--output", default="qr.png", help="Output path for the generated QR code")
    parser.add_argument("--corner-radius", type=int, default=15, help="Border Corner radius for the QR code")
    parser.add_argument("--outer-border-size", type=int, default=15,
                        help="Outer border size of the QR code. Only applicable if text param is provided")
    parser.add_argument("--inner-border-size", type=int, default=15, help="Inner border size of the QR code")

    args = parser.parse_args()

    # Generate the QR code with the logo
    generate_qr_code(
        args.data,
        args.text,
        args.logo,
        save_path=args.output,
        border_corner_radius=args.corner_radius,
        outer_border_size=args.outer_border_size,
        inner_border_size=args.inner_border_size
    )
