import os
import json

backups_folder_path = "./backups"
backups_name = "chat.json"

class Read():
    def __init__(self):
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

    def read(self):
        with open(f"{backups_folder_path}/{backups_name}", "r") as file:
            data = json.load(file)

            return data


# print(Read().read())