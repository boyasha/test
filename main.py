from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from typing import Annotated
from pydantic import BaseModel
from PIL import Image
import os
from io import BytesIO
import numpy as np
import utilities
import openai
import json
import shutil

app = FastAPI()

@app.get('/')
async def root():
  return {'status': 'connected'}

@app.post("/save_image/")
async def save_image(file: UploadFile, name_directory='./save_image/'):
    if name_directory not in os.listdir():
      utilities.create_directory(name_directory)
     
    img = Image.open(file.file)
    img2numpy = np.asarray(img)
    name_of_file = utilities.get_filename_of_file(file.filename)
    np.save(name_directory + name_of_file ,img2numpy)
    img.save(name_directory + file.filename, img.format)
    
    result_json = {'size': img.size, 'format': img.format, 'file_path': os.path.abspath('./save_image/'+file.filename)}
    return json.dumps(result_json)
    
    
@app.get('/static/{file_name}')
async def download_json(file_name: str, name_directory='./static/'):  
    if name_directory not in os.listdir():
      utilities.create_directory(name_directory)
    
    files = os.listdir(name_directory)
    if file_name in files:
      return FileResponse(path=name_directory+file_name, filename=file_name)
    else:
      return {'error': 'the file doesn\'t exist'}
      
      
@app.post('/transcribe/')
async def get_transcribe(file: UploadFile):
  if utilities.get_extension_of_file(file.filename) in utilities.allowed_audio_extension:
    with open(file.filename, 'wb') as audio_file:
      shutil.copyfileobj(file.file, audio_file)
    api = openai.OpenAIAPI(file.filename)
    result = json.dump({'transcription': api.request()['text']})
    os.remove(file.filename)
    return json.dump({'transcription': api.request()})
  else:
    return {'error': 'this is doesn\'t audio file'}
