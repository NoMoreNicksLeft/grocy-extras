#!/usr/bin/env python

from pathlib import Path
from PIL import Image
import requests

################################################################################

file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################



################################################################################
#################################### main() ####################################
################################################################################

images = [
    Image.open("/Users/apple/Desktop/" + f)
    for f in ["bbd.jpg", "bbd1.jpg", "bbd2.jpg"]
]

pdf_path = "/Users/apple/Desktop/bbd1.pdf"
    
images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)