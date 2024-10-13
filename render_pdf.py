import os
import sys

import fitz  # PyMuPDF


def render_pdf_to_images(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)
        # Render the page to an image
        pix = page.get_pixmap()
        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        pix.save(image_path)
        print(f"Saved {image_path}")

    # Close the PDF document
    pdf_document.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_pdf.py <pdf_path> <output_folder>")
        sys.exit(1)

    pdf_path = sys.argv[1]  # Path to your PDF file
    output_folder = sys.argv[2]  # Folder to save images
    render_pdf_to_images(pdf_path, output_folder)
