import streamlit as st
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import io
import tempfile

st.set_page_config(page_title="📄 PDF Rotator", layout="centered")
st.title("📄 PDF Orientation Analyzer & Rotator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

rotation_target = st.radio("Target Rotation:", ["Rotate to Landscape", "Rotate to Portrait"])
rotation_value = 1 if rotation_target == "Rotate to Landscape" else 2

if uploaded_file:
    try:
        # Analyze current page orientations using PyPDF2
        reader = PdfReader(uploaded_file)
        orientations = []
        st.subheader("📊 Page Orientations")
        for i, page in enumerate(reader.pages):
            rotation = page.get("/Rotate", 0)
            if rotation == 0:
                orientation = "Portrait"
            elif rotation == 90:
                orientation = "Landscape (Right)"
            elif rotation == 180:
                orientation = "Portrait (Upside Down)"
            elif rotation == 270:
                orientation = "Landscape (Left)"
            else:
                orientation = f"Unknown ({rotation})"
            orientations.append(orientation)
            st.write(f"Page {i+1}: {orientation}")

        # Rotate and create new PDF using fitz (PyMuPDF)
        uploaded_file.seek(0)
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        output_pdf = fitz.open()

        for page_num, orientation in enumerate(orientations):
            page = pdf_doc.load_page(page_num)

            if orientation == "Portrait" and rotation_value == 1:
                page.set_rotation(270)  # to landscape
            elif orientation == "Landscape (Right)" and rotation_value == 2:
                page.set_rotation(180)  # to portrait
            elif orientation == "Portrait (Upside Down)" and rotation_value == 1:
                page.set_rotation(90)  # to landscape
            elif orientation == "Landscape (Left)" and rotation_value == 2:
                page.set_rotation(0)  # to portrait

            output_pdf.insert_pdf(pdf_doc, from_page=page_num, to_page=page_num)

        # Save to in-memory file
        pdf_bytes = output_pdf.write()
        st.success("✅ Rotation complete! Download below:")

        st.download_button(
            label="📥 Download Rotated PDF",
            data=pdf_bytes,
            file_name="rotated_output.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
