import os

import fire
from requests import post
try:
    import Progress
except ModuleNotFoundError:
    import src.Progress as Progress
import src.File as File
import src.Utilities as Utils
global Log

GlobalLoggingName = f"[{os.path.basename(__file__).split('.')[0]}]"

def Upload(VLC_IP:int,file: File.File):
    req = post(f"http://{VLC_IP}/upload.json",
               headers={
                   "Host": VLC_IP,
                   "Connection": "keep-alive",
                   "Content-Type": file.Monitor.content_type
                },
               data =file.Monitor
               )
    return req.status_code
def Main(VLC_IP: str,*MediaFiles: tuple) -> None:
    Log = Utils.Logging(os.path.basename(__file__).split('.')[0],VLC_IP)
    #Completed_uploads: list[tuple] = []
    #Utils.InitNaming(GlobalLoggingName,VLC_IP)
    MediaFiles: list[File.File] = File.ProcessMediaFileInput(Log,*MediaFiles)
    for Item in MediaFiles:
        status_code = Upload(VLC_IP,Item)
        Log.AddUploadResult(status_code,Item.Name)
        #Completed_uploads.append((status_code,Item.Name))
        #Utils.clear()
        #Utils.Display(Completed_uploads)

if __name__ == "__main__":
    fire.Fire(Main)
