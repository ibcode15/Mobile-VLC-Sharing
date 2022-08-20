import requests

try:
    import Utilities as Utils
except ModuleNotFoundError:
    import src.Utilities as Utils

try:
    import File
except ModuleNotFoundError:
    import src.File as File


def Upload(VLC_IP: str,file: File.File,Log: Utils.Logging | None = None) -> int:
    try:
        req = requests.post(f"http://{VLC_IP}/upload.json",
                            headers={
                                "Host": VLC_IP,
                                "Connection": "keep-alive",
                                "Content-Type": file.Monitor.content_type,
                                "X-Requested-With": "XMLHttpRequest"
                                },
                            data = file.Monitor
                            )
        req.close()
    except requests.exceptions.RequestException:
        if isinstance(Log, Utils.Logging):
            Log.ExitingError(f'not being able to connect to "http://{VLC_IP}"')
        exit(1)
    except Exception as E:
        Log.Add(str(E))
        exit(1)
    if isinstance(Log, Utils.Logging):
        Log.AddUploadResult(req,file.Name)
        
    return 0


def UploadAll(VLC_IP: str, MediaFiles: list[File.File],Log: Utils.Logging | None = None) -> int:
    ServerStatus,Reason = ServerUp(VLC_IP,Log)
    if ServerStatus == 200:
        Log.Add(f'"http://{VLC_IP}" has been found. ({ServerStatus}:{Reason})')
    else:
        Log.ExitingError(f'problems accessing "http://{VLC_IP}" ({ServerStatus}:{Reason})')
    for file in MediaFiles:
        init = file.SetupUpload()
        if init[0]:
            Upload(VLC_IP,file,Log)
        else:
            Log.Add(init[1])
            
def ServerUp(VLC_IP: str, Log) -> (int,str):
    try:
        req = requests.get(f"http://{VLC_IP}",timeout=3)
        return (req.status_code, req.reason)
    except Exception as E:
        if isinstance(Log, Utils.Logging):
            Log.ExitingError(f'not being able to connect to "http://{VLC_IP}"')
        exit(1)
