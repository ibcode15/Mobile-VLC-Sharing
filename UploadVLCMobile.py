import requests
import random,string
from requests_toolbelt import MultipartEncoder,MultipartEncoderMonitor
import magic
import os
import fire
from clint.textui.progress import Bar as ProgressBar
import socket
global Start
Start = f"[{os.path.basename(__file__).split('.')[0]}]"
def Bytes_to_MB(byte):
    return round(byte/1000000, 2)

def create_callback(filename: str, encoder: MultipartEncoder):
    encoder_len = Bytes_to_MB(encoder.len)
    bar = ProgressBar(label = os.path.basename(filename), expected_size=encoder_len, filled_char='=')
    def callback(monitor):
        bar.show(Bytes_to_MB(monitor.bytes_read))

    return callback

def is_media(file: str) -> bool:
    mime = magic.from_file(file, mime=True)
    if "video" in mime or "audio" in mime:
        return True
    
    return False

def Display(files: list) -> None:
    print("\n".join([f"{Start} Completed {i}" for i in files]))
        

def Boundary() -> str:
    return f"----WebKitFormBoundary{''.join(random.sample(string.ascii_letters + string.digits, 16))}"
def Fields(file: str) -> dict:
    return {
        'files[]': (os.path.basename(file), open(file, "rb"), magic.from_file(file, mime=True))
        }


def Main(VLC_IP: str,*MediaFiles):
    Completed_uploads = []

    if MediaFiles == ():
        print(f"{Start} Finding Media Files in {os.curdir}")
        MediaFiles = tuple(filter(is_media, filter(os.path.isfile, os.listdir( os.curdir ))))
    elif len(MediaFiles) == 1 and os.path.isdir(MediaFiles[0]):
        print(f"{Start} Finding Media Files in {MediaFiles[0]}")
        dir_ = MediaFiles[0]
        MediaFiles = [os.path.join(dir_,path) for path in os.listdir(dir_) if os.path.isfile(os.path.join(dir_,path))]
        MediaFiles = tuple(filter(is_media, MediaFiles))
    if MediaFiles == ():
        return f"{Start} Error: Cannot find any Media Files to upload."
    print("\r",sep="",end="")
    for file in MediaFiles:
        print("",end="")
        m = MultipartEncoder(fields=Fields(file), boundary=Boundary())
        callback = create_callback(file,m)
        monitor = MultipartEncoderMonitor(m, callback)
        req = requests.post(f"http://{VLC_IP}/upload.json",
                            headers={
                                "Host": VLC_IP,
                                "Connection": "keep-alive",
                                "Content-Type": monitor.content_type
                                },
                            data=monitor)
        Completed_uploads.append(os.path.basename(file))
        os.system("cls")
        Display(Completed_uploads)
if __name__ == "__main__":
    fire.Fire(Main)
    
