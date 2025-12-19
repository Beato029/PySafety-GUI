from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGroupBox, QSizePolicy, QLabel, QWidget, QToolBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import json
from ui.chat.read import Read
from ui.chat.write import Write


class Chat(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setup_ui()
         

    def setup_ui(self):
        layout = QVBoxLayout(self)
        horizontal_layout = QHBoxLayout()

        left_vertical_layout = QVBoxLayout()
        
        self.rooms_box = self.create_box("Rooms")
        left_vertical_layout.addWidget(self.rooms_box)
        
        add_chat = QPushButton("Nuova Chat")
        add_chat.clicked.connect(self.new_chat)
        left_vertical_layout.addWidget(add_chat)
        
        del_chat = QPushButton("Elimina Chat")
        left_vertical_layout.addWidget(del_chat)


        right_vertical_layout = QVBoxLayout()

        chat_box = self.create_box("Chat")
        right_vertical_layout.addWidget(chat_box)
        

        right_bottom_horizontal_layout = QHBoxLayout()

        message = QLineEdit()
        right_bottom_horizontal_layout.addWidget(message)

        send_button = QPushButton("Invia")
        right_bottom_horizontal_layout.addWidget(send_button)

        right_vertical_layout.addLayout(right_bottom_horizontal_layout)


        horizontal_layout.addLayout(left_vertical_layout, 1)
        horizontal_layout.addLayout(right_vertical_layout, 3)


        layout.addLayout(horizontal_layout)

        self.setup_chat()


    def create_box(self, title):
        widget = QGroupBox(title)

        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        return widget
    
    def new_chat(self):
        self.newChat = None
        if self.newChat is None:
            self.newChat = NewChat()
        self.newChat.show()


    def setup_chat(self):
        self.rooms_box.setStyleSheet("""
            QPushButton {
                background-color: #353535;        
            }

        """)

        chat_ids = Read().read()["chats"]
        chats_buttons = []
        chats_layout = QVBoxLayout()
        for chat in chat_ids:
            button = QPushButton(chat["chat_id"])
            chats_layout.addWidget(button)
            chats_buttons.append(button)

        self.rooms_box.setLayout(chats_layout)


class NewChat(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nuova Chat")
        self.setWindowIcon(QIcon("sources/logo.png"))
        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout()

        self.label1 = QLabel("ID Chat:")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label1)

        self.IDEntry = QLineEdit()
        self.IDEntry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.IDEntry)

        self.label2 = QLabel("Nome Utente")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label2)

        self.USEREntry = QLineEdit()
        self.USEREntry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.USEREntry)

        buttons_layout = QHBoxLayout()

        self.createButton = QPushButton("Crea")
        self.createButton.clicked.connect(self.create_new_chat)
        buttons_layout.addWidget(self.createButton)

        self.cancelButton = QPushButton("Annulla")
        self.cancelButton.clicked.connect(self.cancel_button)
        buttons_layout.addWidget(self.cancelButton)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)


    def create_new_chat(self):
        add_new_chat_json(self.IDEntry.text())
        

    def cancel_button(self):
        self.destroy()


def add_new_chat_json(chat_id):
    Write(chat_id).add_new_chat()