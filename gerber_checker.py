# gerber_checker.py

from fastapi import FastAPI, UploadFile, File
import os
import shutil
import tempfile

app = FastAPI()

REQUIRED_GERBER_FILES = ['GTL', 'GBL', 'GTS', 'GBS', 'TXT']

def check_gerber_folder(folder_path):
    existing_files = os.listdir(folder_path)
    found_files = []

    for req in REQUIRED_GERBER_FILES:
        if any(req in filename.upper() for filename in existing_files):
            found_files.append(req)

    missing_files = list(set(REQUIRED_GERBER_FILES) - set(found_files))

    return {
        "all_required_present": len(missing_files) == 0,
        "missing_files": missing_files
    }

@app.post("/check_gerber/")
async def check_gerber(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_location = os.path.join(tmpdirname, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Assume the file is a zip or folder of Gerber files
        # In real world, you may unzip if necessary
        result = check_gerber_folder(tmpdirname)

    return result

