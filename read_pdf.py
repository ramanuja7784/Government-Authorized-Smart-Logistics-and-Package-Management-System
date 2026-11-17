import sys
import subprocess

try:
    import pypdf
except ImportError:
    print("Installing pypdf...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

def extract_pdf():
    try:
        reader = pypdf.PdfReader("D:\\final year project\\TARUN print.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        with open("D:\\final year project\\pdf_content.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully extracted the PDF to pdf_content.txt!")
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    extract_pdf()
