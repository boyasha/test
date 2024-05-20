from PIL import Image
from PIL.ExifTags import TAGS
import json
import os

allowed_audio_extension = ['mp3', 'opus', 'aac', 'flac', 'wav', 'pcm']

def get_filename_of_file(filename: str) -> str:
  extension_index = filename.rfind('.')
  if extension_index != -1:
    return filename[:extension_index]
  return filename
  
def get_extension_of_file(file_name):
    file_parts = file_name.split(".")
    
    if len(file_parts) > 1:
        extension = file_parts[-1]
        return extension
    else:
        return None
  
 
def get_metadata_of_image(img):
  result_dict = dict()
  exifdata = img.getexif()
  for tag_id in exifdata:
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    if isinstance(data, bytes):
      result_dict.update({tag: data})
    
  return result_dict

def once_call(func):
    def wrapper(*args, **kwargs):
        if not wrapper.called:
            wrapper.called = True
            return func(*args, **kwargs)
    wrapper.called = False
    return wrapper
  
@once_call
def create_directory(name: str):
  os.mkdir(name)

