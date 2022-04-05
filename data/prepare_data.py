import sys
import subprocess
try:
    sourcer = sys.argv[1]
except:
    sourcer = 0

print("""
    Sourcer Prepare
    1. Download /A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip
    2. Unzip Alphas.zip

    Run: py prepare_data.py [sourcer 0(Github)/1(Proxied) ] Default: 0
"""
)

print("Downloading Alphas...")
sourcer_url = "https://github.com" if sourcer == 0 else "https://hub.fastgit.xyz"
subprocess.Popen(["wget","-O","../Sync/Detect/Alphas.zip",f"{sourcer_url}/A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip" , "--no-check-certificate"]).wait()
print("Unzipping Alphas...")
subprocess.Popen(["unzip","../Sync/Detect/Alphas.zip","-d","../Sync/Detect/"]).wait()
print("Removing Alphas.zip...")
subprocess.Popen(["rm","../Sync/Detect/Alphas.zip"]).wait()
print("Done ")