# Fancy QR Code Generator

This Python project allows users to generate QR codes with optional logos and custom text.

## Features

- Generate QR codes with user-defined data.
- Add an optional logo to the center of the QR code.
- Display customizable text below the QR code.
- Control corner radius, inner and outer borders.
- Save generated QR codes in PNG format.

## Installation

Install dependencies using:

```
pip install -r requirements.txt
```

## Usage

Run the script with the following arguments:

### Mandatory Arguments:

- `--data`: The data to be encoded in the QR code (e.g., a URL, text).

### Optional Arguments:

- `--text`: Custom text to be displayed below the QR code.
- `--logo`: Path to the logo image to overlay in the QR code.
- `--output`: Specify the output file name (default: `qr.png`).
- `--corner-radius`: Border corner radius for the QR code (default: 15).
- `--outer-border-size`: Outer border size for the QR code when text is provided (default: 15).
- `--inner-border-size`: Inner border size for the QR code around the logo (default: 15).

### Example command:

```
python qr_generator.py --data "https://example.com" --text "Example" --logo "logo.png" --output "my_qr.png" --corner-radius 20
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.