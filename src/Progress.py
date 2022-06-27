
import os

import progressbar
from requests_toolbelt import MultipartEncoder


def Bar(FileSize: int, FileName: str) -> progressbar.ProgressBar:
    DataFormat = '%(scaled).0f %(prefix)s%(unit)s'
    return progressbar.ProgressBar(max_value = FileSize, widgets=[
        f"{FileName} ",
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
        progressbar.DataSize(format=DataFormat),"/",progressbar.DataSize(format=DataFormat,variable='max_value')," ",
        progressbar.FileTransferSpeed()]
        )

def create_callback(Filepath: str, encoder: MultipartEncoder):
    bar = Bar(encoder.len,os.path.basename(Filepath))
    def callback(monitor):
        bar.update(monitor.bytes_read)

    return callback


