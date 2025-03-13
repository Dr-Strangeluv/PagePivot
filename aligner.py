import tkinter as tk
from tkinter import filedialog
import os
import fitz  # Import PyMuPDF
from PyPDF2 import PdfReader

def open_pdf_file():
    """Opens a file explorer window for PDF selection and analyzes orientation."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select PDF File",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
    )
    if filepath:
        analyze_pdf_orientation(filepath)

def analyze_pdf_orientation(filepath):
    """Performs structural rotation analysis."""
    print("-" * 30)
    print(f"Analyzing PDF: {os.path.basename(filepath)}")
    try:
        current_orientations = analyze_structural_rotation(filepath)
    except FileNotFoundError:
        print(f"Error: File '{os.path.basename(filepath)}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        rotate_and_save_pdf(filepath, current_orientations)

def analyze_structural_rotation(filepath):
    """Analyzes PDF page rotation based on the '/Rotate' attribute."""
    print("\nStructural Page Orientation Analysis:")
    orientations = []
    try:
        with open(filepath, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                rotation = page.get('/Rotate', 0)
                if rotation == 0:
                    orientation = "Portrait"
                elif rotation == 90:
                    orientation = "Landscape (Right)"
                elif rotation == 180:
                    orientation = "Portrait (Upside Down)"
                elif rotation == 270:
                    orientation = "Landscape (Left)"
                else:
                    orientation = f"Unknown (Rotation: {rotation} degrees)"
                print(f"Page {page_num + 1}: {orientation}")
                orientations.append(orientation)
    except Exception as e:
        print(f"Error during structural analysis: {e}")
        orientations = []
    return orientations

def rotate_and_save_pdf(filepath, current_orientations):
    filename, ext = os.path.splitext(os.path.basename(filepath))
    new_filename = f"{filename}_fixed{ext}"
    new_filepath = os.path.join(os.path.dirname(filepath), new_filename)

    try:
        with fitz.open(filepath) as pdf_doc:
            rotated_pdf = fitz.open()
            for page_num, orientation in enumerate(current_orientations):
                page = pdf_doc[page_num]

                # Rotate based on desired orientation
                if orientation == "Portrait" and rotation_var.get() == 1:
                    page.set_rotation(270)  # Rotate to landscape
                elif orientation == "Landscape (Right)" and rotation_var.get() == 2:
                    page.set_rotation(180)  # Rotate to portrait
                elif orientation == "Portrait (Upside Down)" and rotation_var.get() == 1:
                    page.set_rotation(90)  # Rotate to landscape
                elif orientation == "Landscape (Left)" and rotation_var.get() == 2:
                    page.set_rotation(0)  # Rotate to portrait
                else:
                    print(f"Skipping unknown orientation: {orientation}")

                rotated_pdf.insert_pdf(pdf_doc, from_page=page_num, to_page=page_num)  # Append page to the rotated PDF

            rotated_pdf.save(new_filepath)  # Save the new PDF
            print(f"PDF rotation complete! New file saved as: {new_filename}")
    except Exception as e:
        print(f"An error occurred during PDF rotation: {e}")

# GUI Setup
root = tk.Tk()
root.title("PDF Rotator")

# Get the default filepath
initial_filepath = filedialog.askopenfilename(
    initialdir="/",
    title="Select PDF File",
    filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
)

filepath_label = tk.Label(root, text="PDF Filepath:")
filepath_label.pack()

filepath_entry = tk.Entry(root, width=50)
filepath_entry.insert(0, initial_filepath)
filepath_entry.pack()

def browse_file():
    new_filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Select PDF File",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
    )
    filepath_entry.delete(0, tk.END)  # Clear existing entry
    filepath_entry.insert(0, new_filepath)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

rotation_var = tk.IntVar()
rotation_var.set(1)  # Default to landscape

rotation_frame = tk.Frame(root)
rotation_frame.pack(pady=10)

landscape_radio = tk.Radiobutton(
    rotation_frame,
    text="Rotate to Landscape",
    variable=rotation_var,
    value=1
)
landscape_radio.pack(side=tk.LEFT)

portrait_radio = tk.Radiobutton(
    rotation_frame,
    text="Rotate to Portrait",
    variable=rotation_var,
    value=2
)
portrait_radio.pack(side=tk.LEFT)

rotate_button = tk.Button(root, text="Rotate PDF", command=lambda: analyze_pdf_orientation(filepath_entry.get()))
rotate_button.pack()

root.mainloop()

if __name__ == "__main__":
    open_pdf_file()
