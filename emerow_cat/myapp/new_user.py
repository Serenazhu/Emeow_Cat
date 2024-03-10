import subprocess
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the file in the parent directory

inbox = file_path = os.path.join(parent_dir, r'gmail/inbox.py')
sent = os.path.join(parent_dir, r'gmail/sent.py')

scripts = [
    inbox,
    sent
]
for script in scripts:
    subprocess.call(["python", script])
    print("INBOX PATH" + inbox)
    print("SENT PATH" + sent)
