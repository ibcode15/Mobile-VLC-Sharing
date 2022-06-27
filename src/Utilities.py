
import http.client
from os import system
from sys import platform


#def InitNaming(Name: str,VLC_IP: str) -> None:
#    global loggingName
#    global IP
#    loggingName = Name
#    IP = VLC_IP

#def Successful(code: int, file: str):
#    
#    if code == 200:
#        return f"{loggingName} Successfully Uploaded {file} to {IP} ({code}: {http.client.responses[code]})"
#    return f"{loggingName} Failed to Upload {file} to {IP} ({code}: {http.client.responses[code]})"
#def Display(files: list[tuple]) -> None:
#    print("\n".join([Successful(*i) for i in files]))
#def clear() -> str:
#    if platform == "linux" or platform == "darwin":
#        system("clear")
#    elif platform == "win32":
#        system("cls")
#    else:
#        print("cannot find system")

class Logging:
    def __init__(self,Name: str, IP: str):
        self.Log = []
        self.Name = Name
        self.IP = IP
    @staticmethod
    def Clear() -> str:
        if platform == "linux" or platform == "darwin":
            system("clear")
        elif platform == "win32":
            system("cls")
        else:
            print("cannot find system")
    def Update(self):
        print("\n".join(self.Log))
    def AddUploadResult(self, status_code: str,Filename: str):
        if status_code == 200:
            self.Log.append(f"[{self.Name}] Successfully Uploaded {Filename} to {self.IP} ({status_code}: {http.client.responses[status_code]})")
        else:
            self.Log.append(f"[{self.Name}] Failed to Upload {Filename} to {self.IP} ({status_code}: {http.client.responses[status_code]})")
        self.Clear()
        self.Update()
    def Add(self,text):
        self.Log.append(f"[{self.Name}] {text}")
        self.Clear()
        self.Update()
        
