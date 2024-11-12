import os
import pdfplumber

def pdf_to_text(source_folder, destination_folder):
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Iterate over each PDF file in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(source_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(destination_folder, txt_filename)
            
            # Extract text from PDF
            with pdfplumber.open(pdf_path) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text() + '\n'  # Extract text from each page

            # Write the extracted text to a .txt file
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)

            print(f"Converted '{filename}' to '{txt_filename}'")

# Example usage
source_folder = 'C:/Users/karth/Documents/Projects/ML/ManupatraGPT/pdfs'       # Replace with your source folder path
destination_folder = 'C:/Users/karth/Documents/Projects/ML/ManupatraGPT/txts'  # Replace with your destination folder path
pdf_to_text(source_folder, destination_folder)

