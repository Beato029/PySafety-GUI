import os
import json
from datetime import datetime
from ui.chat.read import Read

backups_folder_path = "./backups"
backups_name = "chat.json"

class Write():
    def __init__(self, chat_id=""):
        self._chat_id_ = chat_id
        self.buildFolder()

    def buildFolder(self):
        if not os.path.exists(backups_folder_path):
            os.mkdir(backups_folder_path)
        
        if not os.path.exists(f"{backups_folder_path}/{backups_name}"):
            with open(f"{backups_folder_path}/{backups_name}", "w") as file:
                data = {
                    "backup_data": "",
                    "chats": [
  
                    ]
                }
                json.dump(data, file, indent=4, ensure_ascii=False)

    def write(self, data):
        with open(f"{backups_folder_path}/{backups_name}", "w") as file: 
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(data)

    def add_new_chat(self):
        old_data = Read().read()
        
        new_data = {
            "chat_id": f"{self._chat_id_}",
            "partcipants": [

            ],
            "messages": [
                {
    
                }
            ]
        }
        
        old_data["chats"].append(new_data)

        self.write(old_data)

# backup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
# data = f"""
# {{
#     "backup_date": "{backup_date}",
#     "chats": [
#         {
#             "chat_id": "52"
        
#         }
#     ]
# }}
# """