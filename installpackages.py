import subprocess
import sys
import os

#from pathlib import Path

#requirements = Path("/voc/router-support-agent/requirements.txt")
print(os.getcwd())
requirements = os.path.join(os.getcwd(), "work/router-support-agent/requirements.txt")

print (requirements)
if not requirements:
    print("requirements.txt not found!")
    sys.exit(1)

print("Installing libraries from requirements.txt...\n")

subprocess.check_call([
    sys.executable,
    "-m",
    "pip",
    "install",
    "-r",
    str(requirements)
])

print("\n✅ All libraries installed successfully!")