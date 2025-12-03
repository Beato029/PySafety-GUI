import os
import json
from datetime import datetime

backups_folder_path = "./backups"

def buildFolder():
    if not os.path.exists(backups_folder_path):
        os.mkdir(backups_folder_path)

def writeData(data):
    buildFolder()
    if not os.path.exists(backups_folder_path):
        with open(f"{backups_folder_path}/chat.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)



backup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
data = f"""
{{
    "backup_date": "{backup_date}",
    "chats": [
        {
            "chat_id": "52"
        
        }
    ]
}}
"""