
import requests
from sys import platform
import os

def GetFileName(name: str) -> str: return os.path.basename(name).split('.')[0]

class Logging:
    def __init__(self,Name: str, IP: str):
        self.Log = []
        self.Name = Name
        self.IP = IP
        self.ClearCommand = {
            "linux": "clear",
            "darwin":"clear",
            "win32":"cls"
            }.get(platform,"cls")
    def Update(self):
        os.system(self.ClearCommand)
        print("\n".join(self.Log))
    def ExitingDueTo(self,MSG,Exitcode=1):
        self.Log.append(f"[{self.Name}] Exiting program due to {MSG}.")
        self.Update()
        exit(Exitcode)
    def ExitingError(self,MSG: str,Exitcode=1):
        self.Log.append(f"[{self.Name}] Error: Exiting program due to {MSG}.")
        self.Update()
        exit(Exitcode)
        
    def AddUploadResult(self, Response: requests.Response ,Filename: str):
        if Response.status_code == 200:
            self.Log.append(f'[{self.Name}] Successfully Uploaded "{Filename}" to {self.IP}. ({Response.status_code}: {Response.reason})')
        else:
            self.Log.append(f'[{self.Name}] Failed to Upload "{Filename}" to {self.IP}. ({Response.status_code}: {Response.reason})')
        self.Update()
    def Add(self,text):
        self.Log.append(f"[{self.Name}] {text}")
        self.Update()
        
