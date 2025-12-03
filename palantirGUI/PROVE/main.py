import json

with open("./PROVE/chat.json", "w") as file:
    data = {
    "backup_data": "",
    "chats": [
        {
            "chat_id": "prova123",
            "users": [
                "User 1",
                "User 2"
            ],
            "messages": [
                {
                    "sender": "User 1",
                    "content": "Hello World!",
                    "timestamp": "2025"
                },
                {
                    "sender": "User 2",
                    "content": "Ciao",
                    "timestamp": "1925"
                }
            ]        
        }
    ]
}
    
new_data = {
    "sender": "User 3",
    "content": "Come Va?",
    "timestamp": "1945"
}

data["chats"][0]["messages"].append(new_data)

print(json.dumps(data["chats"], indent=4, ensure_ascii=False))
print(data["chats"][0]["messages"][2]["sender"])
    # json.dump(data, file, indent=4, ensure_ascii=False)


# def read():
#     with open("./PROVE/chat.json", "r") as file:
#         data = json.load(file)
#         print(data)

# read()

# def write(data):
#     with open("./PROVE/chat.json", "w") as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)


# write(data)