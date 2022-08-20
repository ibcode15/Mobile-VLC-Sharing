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



def is_media(file: str,loadingbar: bool) -> bool | tuple:
    mime = magic.from_file(file, mime=True)
    if "video" in mime or "audio" in mime:
        return (file, 0, mime, loadingbar)
    
    return False


@dataclass()
class File:
    Name: str
    Mode: int
    Mime: str
    loadingbar: bool
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
            if self.loadingbar:
                self.Callback = Progress.LoadingBarCallback(self.Path,self.Encoder)
            else:
                self.Callback = Progress.NoLoadingBarCallback(self.Path,self.Encoder)
            self.Monitor = MultipartEncoderMonitor(self.Encoder, self.Callback)
            return (True,"")
        return (False, "Could not find mode {self.Mode} and so will skip the upload of {self.Name}")
        




def ProcessMediaFileInput(Log: Utilities.Logging,loadingbar: bool,*MediaFiles: tuple) -> list[File]:
    Temp_MediaFiles = []
    if MediaFiles == ():
        CurrentDir = os.getcwd()
        Log.Add(f"Finding Media Files in {CurrentDir}.")
        
        GetFiles = [is_media(os.path.join(CurrentDir,path),loadingbar) for path in os.listdir(CurrentDir) if os.path.isfile(os.path.join(CurrentDir,path))]
        if GetFiles != []:
            Temp_MediaFiles += [File(*i) for i in GetFiles if i]
            Log.Add(f"Found {len(Temp_MediaFiles)} Media files in {CurrentDir}.")
        else:
            Log.Add(f"Found 0 Media Files in {CurrentDir}")
            pass
    else:
        for file in MediaFiles:
            if os.path.isdir(file):
                dir_ = file
                Log.Add(f"Finding Media Files in {dir_}.")
                GetFiles = [is_media(os.path.join(dir_,path),loadingbar) for path in os.listdir(dir_) if os.path.isfile(os.path.join(dir_,path))]
                if GetFiles != []:
                    Temp_MediaFiles += [File(*i) for i in GetFiles if i]
                    Log.Add(f"Found {len(Temp_MediaFiles)} Media files in {dir_}.")
                else:
                    Log.Add(f"Found 0 media files in {dir_}.")
            elif os.path.isfile(file):
                Log.Add(f'Checking to see if "{file}" is a Media File.')
                file = is_media(file,loadingbar)
                
                if file != False:
                    Log.Add(f'"{file[0]}" is a Media File.')
                    Temp_MediaFiles.append(File(*file))
                else:
                    Log.Add(f'"{file[0]}" is a "{file[2]}" file which is not a Media File.')
            else:
                Log.Add(f'"{file}" could not be found.')
    return Temp_MediaFiles
                
