import subprocess

scripts = [
    r"gmail\re_inbox.py",
    r"gmail\re_sent.py",
]
for script in scripts:
    subprocess.call(["python", script])
