from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

pdf_file="Carver_Allison CAQH Data_Summary-1.pdf"

# convert pdf pages to images
# Specify the Poppler path if necessary (for Windows)
poppler_path = r"C:/poppler/bin"  # Adjust to your actual Poppler installation directory

# Convert PDF pages to images
pages = convert_from_path(pdf_file, poppler_path=poppler_path)

def deskew(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray=cv2.bitwise_not(gray)
    coords=np.column_stack(np.where(gray>0))
    angle=cv2.minAreaRect(coords)[-1]
    if angle<-45:
        angle=-(90+angle)
    else:
        angle=-angle
    
    (h,w)=image.shape[:2]
    center=(w//2,h//2)
    M=cv2.getRotationMatrix2D(center,angle,1.0)
    rotated=cv2.warpAffine(image,M,(w,h),flag=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    return rotated

def extract_text_from_image(image):
    text=pytesseract.image_to_sring(image)
    return text

# Create a list to store extracted text from all pages
extracted_text = []

for page in pages:
    # Step 2: Preprocess the image (deskew)
    preprocessed_image = deskew(np.array(page))

    # Step 3: Extract text using OCR
    text = extract_text_from_image(preprocessed_image)
    extracted_text.append(text)

print(text)