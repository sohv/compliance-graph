import os
from PyPDF2 import PdfReader

def read_pdf(file_path):
    pdf_text = ''
    
    try:
        reader = PdfReader(file_path)
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text
                
        print("PDF text successfully extracted.")
        return pdf_text
        
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None

def save_text_to_file(text, output_file="output.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted text has been saved to '{output_file}'.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_pdf = os.path.join(script_dir, "..", "data", "docs", "synthetic_financial_rules.pdf")
    output_txt = os.path.join(script_dir, "..", "data", "output.txt")
    
    os.makedirs(os.path.dirname(input_pdf), exist_ok=True)
    
    if not os.path.exists(input_pdf):
        print(f"Please place your PDF file at: {input_pdf}")
        return
    
    pdf_text = read_pdf(input_pdf)
    if pdf_text:
        save_text_to_file(pdf_text, output_txt)

if __name__ == "__main__":
    main() 