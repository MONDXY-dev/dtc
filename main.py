import os
import time
import random
from datetime import datetime, timedelta
from subprocess import *
import subprocess

result = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE)
installed_packages = result.stdout.decode('utf-8')


try:
    installed_packages.index("pywin32")

    def change_file_times_random(file_path):
        current_time = datetime.now()
        random_days = random.randint(0, 10)
        new_date = current_time - timedelta(days=random_days)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)

        new_time = new_date.replace(hour=random_hours, minute=random_minutes, second=random_seconds)
        new_epoch = new_time.timestamp()
        os.utime(file_path, (new_epoch, new_epoch))
        if os.name == 'nt':
            import pywintypes
            import win32file
            import win32con
            
            file_handle = win32file.CreateFile(
                file_path, win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None, win32con.OPEN_EXISTING, 0, None)
            
            new_pytime = pywintypes.Time(new_epoch)
            
            win32file.SetFileTime(file_handle, new_pytime, new_pytime, new_pytime)
            file_handle.close()
    def scan_directory_for_sldprt(directory):
        sldprt_files = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.SLDPRT'):
                    file_path = os.path.join(root, file)
                    sldprt_files[file] = file_path
        return sldprt_files

    current_directory = os.getcwd()
    sldprt_files = scan_directory_for_sldprt(current_directory)

    for file_path in sldprt_files :
        print(file_path)
        if os.path.exists(file_path):
            change_file_times_random(file_path)
            print(f"File times for {file_path} have been changed successfully.")
        else:
            print(f"The file {file_path} does not exist.")
except ValueError:
    print("Not Have Pywin32 Package, We Are Loading.")
    result = subprocess.run(['pip', 'install', 'pywin32'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    p = Popen(["run.bat", "4"], shell=True, stdin=PIPE)
