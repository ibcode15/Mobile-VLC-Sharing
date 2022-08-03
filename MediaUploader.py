import os
import sys
import fire
import requests
import src.File as File
import src.Utilities as Utils



def Upload(VLC_IP: str,file: File.File,Log: Utils.Logging | None = None) -> int:
    try:
        req = requests.post(f"http://{VLC_IP}/upload.json",
                   headers={
                       "Host": VLC_IP,
                       "Connection": "keep-alive",
                       "Content-Type": file.Monitor.content_type
                    },
                   data =file.Monitor
                   )
    except requests.exceptions.ConnectionError:
        if isinstance(Log, Utils.Logging):
            Log.Add(f"Error: Could not connect to {VLC_IP}.")
        exit(1)
            
    if isinstance(Log, Utils.Logging):
        Log.AddUploadResult(req.status_code,file.Name)
    return 0
def Main(VLC_IP: str,*MediaFiles: tuple[str]) -> None:
    LoggingName = os.path.basename(__file__).split('.')[0]
    Log = Utils.Logging(LoggingName,VLC_IP)
    try:
        MediaFiles: list[File.File] = File.ProcessMediaFileInput(Log,*MediaFiles)
        if MediaFiles == []:
            Log.Add("Exiting program due to the lack of media files in the specified directory.")
            exit(1)
        Log.Add("Starting Uploading phase.")
        for Item in MediaFiles:
            setup = Item.SetupUpload()
            if setup[0]:
                Upload(VLC_IP,Item,Log)
            else:
                Log.Add(setup[1])
        Log.Add("Finished Uploading all Media files.")
    except KeyboardInterrupt:
        Log.Add("Exiting program due to keyboard interrupt.")
        exit(1)
    except Exception as E:
        Log.Add(str(E))

if __name__ == "__main__":
    fire.Fire(Main)
