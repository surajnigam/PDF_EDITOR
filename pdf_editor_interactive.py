from pypdf import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Function to extract text from the first page of a PDF and save to a file
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)  # Create a PDF reader object to read the PDF file
    print(f"Number of pages: {len(reader.pages)}")  # Print the number of pages in the PDF
    page = reader.pages[0]  # Get the first page of the PDF
    extracted_text = page.extract_text()  # Extract text from the first page
    
    # Save the extracted text to a separate file
    output_file = pdf_file.split('.pdf')[0] + '_extracted_text.txt'  # Create an output file name
    with open(output_file, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)  # Write the extracted text to the file
    
    print(f"Extracted text has been saved to {output_file}")  # Inform the user that the text has been saved

# Function to rotate pages in a PDF
def PDFrotate(origFileName, newFileName, rotation):
    reader = PdfReader(origFileName)  # Create a PDF reader object to read the original PDF
    writer = PdfWriter()  # Create a PDF writer object to write the rotated PDF
    
    for page_num in range(len(reader.pages)):
        pageObj = reader.pages[page_num]  # Get each page of the PDF
        pageObj = pageObj.rotate(rotation)  # Rotate the page by the specified angle
        writer.add_page(pageObj)  # Add the rotated page to the writer
    
    # Write the rotated pages to a new file
    with open(newFileName, 'wb') as newFile:
        writer.write(newFile)  # Write the new PDF file
    print(f"Rotated PDF has been saved to {newFileName}")  # Inform the user that the rotated PDF has been saved

# Function to merge multiple PDFs into one
def PDFmerge(pdfs, output):
    merger = PdfMerger()  # Create a PDF merger object to merge the PDFs
    
    for pdf in pdfs:
        merger.append(pdf)  # Append each PDF to the merger
    
    # Write the merged PDFs to a new file
    with open(output, 'wb') as f:
        merger.write(f)  # Write the new merged PDF file
    print(f"Merged PDF has been saved to {output}")  # Inform the user that the merged PDF has been saved

# Function to split a PDF into multiple PDFs based on split points
def PDFsplit(pdf, splits):
    reader = PdfReader(pdf)  # Create a PDF reader object to read the PDF
    start = 0
    end = splits[0]
    
    for i in range(len(splits) + 1):
        writer = PdfWriter()  # Create a PDF writer object to write the split PDFs
        outputpdf = pdf.split('.pdf')[0] + f'_part{i+1}.pdf'  # Create an output file name for each split part
        
        for page in range(start, end):
            writer.add_page(reader.pages[page])  # Add the specified range of pages to the writer
        
        # Write the split PDF to a new file
        with open(outputpdf, 'wb') as f:
            writer.write(f)  # Write the new split PDF file
        
        print(f"Split PDF part {i+1} has been saved to {outputpdf}")  # Inform the user that the split part has been saved
        
        start = end  # Update the start page for the next split
        try:
            end = splits[i + 1]  # Update the end page for the next split
        except IndexError:
            end = len(reader.pages)  # If no more splits, set the end to the total number of pages

# Function to create a watermark PDF with user text
def create_watermark_pdf(watermark_text):
    packet = io.BytesIO()  # Create an in-memory binary stream to store the PDF
    can = canvas.Canvas(packet, pagesize=letter)  # Create a canvas to draw the watermark
    can.setFont("Helvetica", 40)  # Set the font and size for the watermark
    can.setFillGray(0.5, 0.5)  # Set the fill color to light gray
    can.saveState()
    can.translate(300, 500)
    can.rotate(45)  # Rotate the text to be diagonal
    can.drawCentredString(0, 0, watermark_text)  # Draw the watermark text at the center
    can.restoreState()
    can.save()  # Save the canvas to the binary stream

    packet.seek(0)
    return PdfReader(packet)  # Create a PDF reader object from the in-memory stream

# Function to add a watermark to each page of a PDF
def add_watermark(watermark_text, pageObj):
    wm_reader = create_watermark_pdf(watermark_text)  # Create a watermark PDF
    pageObj.merge_page(wm_reader.pages[0])  # Merge the watermark with the page
    return pageObj

def PDFadd_watermark(origFileName, watermark_text, newFileName):
    with open(origFileName, 'rb') as pdfFileObj:
        reader = PdfReader(pdfFileObj)  # Create a PDF reader object to read the original PDF
        writer = PdfWriter()  # Create a PDF writer object to write the watermarked PDF
        
        for page in range(len(reader.pages)):
            wmpageObj = add_watermark(watermark_text, reader.pages[page])  # Add watermark to each page
            writer.add_page(wmpageObj)
        
        # Write the watermarked pages to a new file
        with open(newFileName, 'wb') as newFile:
            writer.write(newFile)  # Write the new watermarked PDF file
    print(f"Watermarked PDF has been saved to {newFileName}")  # Inform the user that the watermarked PDF has been saved

def main():
    print("Choose an operation:")
    print("1. Extract text from the first page")
    print("2. Rotate pages in a PDF")
    print("3. Merge multiple PDFs")
    print("4. Split a PDF")
    print("5. Add a watermark to a PDF")
    
    choice = input("Enter the number of the operation you want to perform: ")
    
    if choice == '1':
        pdf_file = input("Enter the PDF file name: ")
        extract_text(pdf_file)  # Extract text from the first page of the specified PDF
    elif choice == '2':
        origFileName = input("Enter the original PDF file name: ")
        newFileName = input("Enter the new PDF file name: ")
        rotation = int(input("Enter the rotation angle (must be one of 90, 180, or 270): "))
        PDFrotate(origFileName, newFileName, rotation)  # Rotate the specified PDF
    elif choice == '3':
        try:
            num_pdfs = int(input("Enter the number of PDF files to merge: "))
            pdfs = [input(f"Enter PDF file {i+1} name: ") for i in range(num_pdfs)]
            output = input("Enter the output PDF file name: ")
            PDFmerge(pdfs, output)  # Merge the specified PDF files
        except ValueError:
            print("Please enter a valid number.")
    elif choice == '4':
        pdf = input("Enter the PDF file name to split: ")
        splits = list(map(int, input("Enter the split page numbers separated by spaces: ").split()))
        PDFsplit(pdf, splits)  # Split the specified PDF at the specified page numbers
    elif choice == '5':
        origFileName = input("Enter the original PDF file name: ")
        watermark_text = input("Enter the watermark text: ")
        newFileName = input("Enter the new PDF file name: ")
        PDFadd_watermark(origFileName, watermark_text, newFileName)  # Add watermark to the specified PDF
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  # Run the main function to start the program
