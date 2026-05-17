import os
from pypdf import PdfWriter

def mergePdfs(fileList: list[str], outputFilename = "4.1.1_MaxRedka.pdf"):
    # Initialize the PDF writer
    merger = PdfWriter()
    
    
    if not fileList:
        print("No PDF files provided.")
        return

    # Append each PDF to the merger
    try:
        for pdf in fileList:
            print(f"Adding: {pdf}")
            merger.append(pdf)
    except:
        print("Failed to add pdfs, check file paths.")

    # Write the merged PDF to a file
    merger.write(outputFilename)
    merger.close()
    print(f"Successfully merged {len(fileList)} files into {outputFilename}")

if __name__ == "__main__":
    mergePdfs([
        "client.py.pdf",
        "paint.py.pdf",
        "colorbar.py.pdf",
        "toolbar.py.pdf",
        "tools.py.pdf",
        "actions.py.pdf",
        "point.py.pdf",
        "main.py.pdf",
        "network.py.pdf"
    ])
