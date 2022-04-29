import sys
import subprocess
try:
    sourcer = sys.argv[1]
    running_type = sys.argv[2]
except:
    sourcer = 0
    running_type = "once"

print("""

    Sourcer Prepare
    1. Download /A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip
    2. Unzip Alphas.zip

    Run: py prepare_data.py [sourcer 0(Github)/1(Proxied) ]  [Running Type /once(Default)/daemon ] Default: 0
"""
)
export_path = "../Sync/Detect/"

print("Downloading Alphas...")
sourcer_url = "https://github.com" if sourcer == 0 else "https://hub.fastgit.xyz"
subprocess.Popen(["wget","-O",f"{export_path}/Alphas.zip",f"{sourcer_url}/A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip" , "--no-check-certificate"]).wait()
print("Unzipping Alphas...")
subprocess.Popen(["unzip",f"{export_path}Alphas.zip","-d",export_path]).wait()
print("Removing Alphas.zip...")
subprocess.Popen(["rm",f"{export_path}Alphas.zip"]).wait()
print("Done ")