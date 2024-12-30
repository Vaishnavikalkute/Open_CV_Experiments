from fastapi import FastAPI,File,UploadFile
from fastapi.responses import FileResponse
import os
from PyPDF2 import PdfReader
import pyttsx3

app=FastAPI()
# Directory to store uploaded files and output audio
UPLOAD_DIR = "uploads"
AUDIO_DIR = "audios"


def extract_text(file_path):
    reader=PdfReader(file_path)
    if reader.is_encrypted:
        try:
            # Attempt to decrypt the PDF
            reader.decrypt('')
        except Exception as e:
            return f"Error decrypting PDF: {e}"
    text=""
    for page in reader.pages:
        text+=page.extract_text()

    return text

def text_to_audio(text,output_file):
    engine=pyttsx3.init()
    engine.setProperty("rate",150)
    engine.setProperty('volume',0.9)
    engine.save_to_file(text,output_file)
    engine.runAndWait()


@app.post("/upload")
async def upload_pdf(file:UploadFile=File(...)):
    if file.content_type!="application/pdf":
        return {'error':"Not a pdf"}
    
    file_path=os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,'wb') as f:
        f.write(await file.read())

    text=extract_text(file_path)
    audio_filename=f"{os.path.splitext(file.filename)[0]}.mp3"
    text_to_audio(text,audio_filename)
    

    return {"audio_file":audio_filename,"message":"Audio book created successfully!"}

@app.get('/audio/{filename}')
def download_audio(filename:str):
    filepath=os.path.join(AUDIO_DIR,filename)
    if os.path.exists(filepath):
        return FileResponse(filepath,media_type="audio/mpeg",filename=filename)
    
    return {"error":"file not found"}


