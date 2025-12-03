import os
import json

backups_folder_path = "./backups"
backups_name = "chat.json"

def buildFolder():
    if not os.path.exists(backups_folder_path):
        os.mkdir(backups_folder_path)


