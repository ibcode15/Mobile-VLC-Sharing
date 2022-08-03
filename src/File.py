import os
import random
import re
import string
from dataclasses import dataclass
try:
    import Progress
except ModuleNotFoundError:
    import src.Progress as Progress
import _io
import magic
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
try:
    import Utilities
except ModuleNotFoundError:
    import src.Utilities as Utilities



URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
def is_media(file: str) -> bool | tuple:
    mime = magic.from_file(file, mime=True)
    if "video" in mime or "audio" in mime:
        return (file, 0, mime)
    
    return False
def is_url(url: str) -> bool:
    return re.findall(URL_REGEX,url) != []

@dataclass()
class File:
    Name: str
    Mode: int # 0 means file and 1 means url
    Mime: str
    Path: str = ""
    Data: _io.TextIOWrapper = ""
    @staticmethod
    def Boundary() -> str:
        return f"----WebKitFormBoundary{''.join(random.sample(string.ascii_letters + string.digits, 16))}" 
    def SetupUpload(self) -> tuple[bool, str]:
        if self.Mode == 0:
            self.Path = self.Name
            self.Name = os.path.basename(self.Path)
            self.Data = open(self.Path, "rb")
            self.Encoder = MultipartEncoder(boundary=self.Boundary(),fields={
                'files[]':(self.Name,self.Data,self.Mime)
                })
            self.Callback = Progress.create_callback(self.Path,self.Encoder)
            self.Monitor = MultipartEncoderMonitor(self.Encoder, self.Callback)
            return (True,"")
        elif self.Mode == 1:
            return (False, "Mode 1 aka 'Url mode' has not been implemented yet and so will skip the upload of {self.Name}")
        return (False, "Could not find mode {self.Mode} and so will skip the upload of {self.Name}")
        




def ProcessMediaFileInput(Log: Utilities.Logging,*MediaFiles: tuple) -> list[File]:
    Temp_MediaFiles = []
    if MediaFiles == ():
        Log.Add(f"Finding Media Files in {os.curdir}.")
        
        GetFiles = [is_media(os.path.join(os.curdir,path)) for path in os.listdir(os.curdir) if os.path.isfile(os.path.join(os.curdir,path))]
        if GetFiles != []:
            Temp_MediaFiles += [File(*i) for i in GetFiles if i]
            Log.Add(f"Found {len(Temp_MediaFiles)} Media files in {os.curdir}.")
        else:
            Log.Add(f"Found 0 Media Files in {os.curdir}")
            pass
    else:
        for file in MediaFiles:
            if os.path.isdir(file):
                dir_ = file
                Log.Add(f"Finding Media Files in {dir_}.")
                GetFiles = [is_media(os.path.join(dir_,path)) for path in os.listdir(dir_) if os.path.isfile(os.path.join(dir_,path))]
                if GetFiles != []:
                    Temp_MediaFiles += [File(*i) for i in GetFiles if i]
                    Log.Add(f"Found {len(Temp_MediaFiles)} Media files in {dir_}.")
                else:
                    Log.Add(f"Found 0 media files in {dir_}.")
            elif os.path.isfile(file):
                Log.Add(f'Checking to see if "{file}" is a Media File.')
                file = is_media(file)
                
                if file != False:
                    Log.Add(f'"{file[0]}" is a Media File.')
                    Temp_MediaFiles.append(File(*file))
                else:
                    Log.Add(f'"{file[0]}" is a "{file[2]}" file which is not a Media File.')
            #elif is_url(file):
            #    Temp_MediaFiles.append(file)
            else:
                Log.Add(f'"{file}" could not be found.')
    return Temp_MediaFiles
                
