# PagePivot
A tool that manage and align PDF pages with varying orientations.

A web-based tool to detect and correct PDF page orientations using `PyMuPDF` and `PyPDF2`. Built with **Streamlit**, this app lets users upload PDFs, analyze page rotations, and rotate them to either landscape or portrait formats.

## 🚀 Features

- Upload any PDF and analyze the rotation of each page
- Choose a target orientation: **Landscape** or **Portrait**
- Automatically adjusts page rotations accordingly
- Download the newly rotated PDF
- No installation required – runs in the browser


🌐 Try the live app:https://pagepivot-1.streamlit.app/

## 💻 Running Locally

```bash
git clone https://github.com/yourusername/pdf-rotator.git
cd pdf-rotator
pip install -r requirements.txt
streamlit run app.py
