import subprocess

scripts = [
    r"emerow_cat\gmail\inbox.py",
    r"emerow_cat\gmail\sent.py",
    r"emerow_cat\gpt\data_prep.py",
    r"emerow_cat\gpt\data_embedding.py"
]
for script in scripts:
    subprocess.call(["python", script])
