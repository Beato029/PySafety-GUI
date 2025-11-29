import os
import json

backups_folder_path = "./backups"
backups_name = "chat.json"

def buildFolder():
    if not os.path.exists(backups_folder_path):
        os.mkdir(backups_folder_path)


a = json.dumps(["foo", {"bar": ("bar", None, 1.0, 2)}])
print(a)