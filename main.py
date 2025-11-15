from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QToolButton, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeatoShare")
        self.setWindowIcon(QIcon("sources/logo.png"))

        width, height = self.getGeometry()
        perc = 20
        self.setMinimumSize(width // 2 + ((width * perc) // 100), height // 2 + ((height * perc) // 100))

        self.mainMenu()

    def getGeometry(self):
        screen = self.screen()
        screen_size = screen.size()
        width = int(screen_size.width())
        height = int(screen_size.height())

        return width, height

    def mainMenu(self):
        self.ServerButton()
        self.ClientButton()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        layout.addWidget(self.server_button)
        layout.addWidget(self.client_button)

    def ServerButton(self):     
        screen_width, screen_height = self.getGeometry()
        width = screen_width // 7
        height = screen_height // 4

        self.server_button = QToolButton()
        self.server_button.setFixedSize(width, height)

        server_widget = QWidget(self.server_button)
        server_widget.setFixedSize(width, height)

        server_layout = QVBoxLayout(server_widget)
        server_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_layout.setSpacing(2)
        server_layout.setContentsMargins(0, 0, 0, 0)

        server_icon = QLabel()
        server_icon.setPixmap(QIcon("sources/server.png").pixmap(130, 130))
        server_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        server_title = QLabel("Server")
        server_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_title.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 25px;
                font-weight: bold;
                color: white;                      
            }

        """)

        server_text = QLabel("Avvia Server")
        server_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_text.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 15px;
                color: white;
            }
                                  
        """)

        self.server_button.setStyleSheet("""
            QToolButton {
                border: 2px solid black;
                border-radius: 5px;                             
            }
            QToolButton:hover {
                background-color: gray;                             
            }

        """)

        server_layout.addWidget(server_icon)
        server_layout.addWidget(server_title)
        server_layout.addWidget(server_text)
        
    def ClientButton(self):
        screen_width, screen_height = self.getGeometry()
        width = screen_width // 7
        height = screen_height // 4

        self.client_button = QToolButton()
        self.client_button.setFixedSize(width, height)

        client_widget = QWidget(self.client_button)
        client_widget.setFixedSize(width, height)

        client_layout = QVBoxLayout(client_widget)
        client_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        client_layout.setSpacing(2)
        client_layout.setContentsMargins(0, 0, 0, 0)

        client_icon = QLabel()
        client_icon.setPixmap(QIcon("sources/client.png").pixmap(130, 130))
        client_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        client_title = QLabel("Client")
        client_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        client_title.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 25px;
                font-weight: bold;
                color: white;     
            }

        """)

        client_text = QLabel("Crea Client")
        client_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        client_text.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 15px;
                color: white;                      
            }
        """)

        self.client_button.setStyleSheet("""
            QToolButton {
                border: 2px solid black;
                border-radius: 5px;                             
            }
            QToolButton:hover {
                background-color: gray;                             
            }

        """)

        client_layout.addWidget(client_icon)
        client_layout.addWidget(client_title)
        client_layout.addWidget(client_text)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon("sources/logo.png"))

window = MainWindow()
window.show()

app.exec()
