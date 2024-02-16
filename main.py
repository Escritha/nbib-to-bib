import os
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from conversion import NbibToBibConverter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adiciona uma rota estática para servir os arquivos na pasta 'bibs'
app.mount("/bibs", StaticFiles(directory="bibs", html=False), name="bibs")

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            content = await file.read()
            converter = NbibToBibConverter(os.getcwd())
            converter.convert_file(content)

        return {"message": "Files uploaded successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
async def download_ref_bib():
    # Retorna o conteúdo do arquivo 'ref.bib'
    file_path = os.path.join(os.getcwd(), 'bibs', 'ref.bib')
    return FileResponse(file_path, filename='ref.bib', media_type='application/x-bibtex')