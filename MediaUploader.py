import fire
import src.File as File
import src.Utilities as Utils
import src.Uploader as Uploader

def Main(VLC_IP: str,*MediaFiles: tuple[str],loadingbar: bool = True) -> None:
    try:
        LoggingName = Utils.GetFileName(__file__)
        Log = Utils.Logging(LoggingName,VLC_IP)
        MediaFiles: list[File.File] = File.ProcessMediaFileInput(Log,loadingbar,*MediaFiles)
        if MediaFiles == []:
            Log.ExitingDueTo("the lack of media files in the specified directory")
        Log.Add("Starting Uploading phase.")
        Uploader.UploadAll(
            VLC_IP = VLC_IP,
            MediaFiles = MediaFiles,
            Log = Log
            )
        Log.Add("Finished Uploading all Media files.")
    except KeyboardInterrupt:
        Log.ExitingDueTo("keyboard interrupt")
    except Exception as E:
        Log.ExitingError(str(E))

if __name__ == "__main__":
    fire.Fire(Main)
