from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QSystemTrayIcon, QAction, QMenu, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class RoundedWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons()

    def buttons(self):
        self.configure_window()
        self.create_buttons()
        self.configure_buttons()
        self.create_layout()

    def configure_window(self):
        # Configurar la ventana para que tenga esquinas redondeadas
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #131313;
                border: none;
            }
            QPushButton {
                background-color: #FFFFFF;
                border: none;
                border-radius: 15px;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
            }
            QPushButton:hover {
                background-color: #b7b7b7;
            }
            QPushButton#appIconButton {
                background-color: #FFFFFF;
                border: none;
                border-radius: 40px;
            }
        """)

    def create_buttons(self):
        # Crear los botones de cerrar, maximizar y minimizar
        self.close_button = QPushButton(self)
        self.close_button.clicked.connect(self.close)

        # Crear tres botones circulares
        self.quest_button = QPushButton(self)
        self.save_last_record_button = QPushButton(self)
        self.leave_button = QPushButton(self)
        self.leave_button.clicked.connect(self.minimize_to_tray)

        # Crear un cuarto botón circular para el icono de la aplicación
        self.app_icon_button = QPushButton(self)

    def configure_buttons(self):
        # Configurar el logo de la aplicación
        self.setWindowIcon(QIcon('resources/icons/icon.png'))

        # Configurar los iconos de los botones
        self.close_button.setIcon(QIcon('resources/buttons/close.png'))
        self.quest_button.setIcon(QIcon('resources/buttons/microphone.png'))
        self.save_last_record_button.setIcon(QIcon('resources/buttons/save.png'))
        self.leave_button.setIcon(QIcon('resources/buttons/leave_door.png'))

        # Configurar el botón del icono de la aplicación
        self.app_icon_button.setIcon(QIcon('resources/icons/icon.png'))
        self.app_icon_button.setIconSize(QSize(70, 70))  # Ajusta el tamaño del icono
        self.app_icon_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: none;
                border-radius: 40px;
                min-width: 80px;
                max-width: 80px;
                min-height: 80px;
                max-height: 80px;
            }
        """)
        self.app_icon_button.setObjectName("appIconButton")

    def create_layout(self):
        # Crear un layout y agregar los botones a él
        layout = QHBoxLayout()
        layout.addWidget(self.close_button)
        layout.addWidget(self.quest_button)
        layout.addWidget(self.save_last_record_button)
        layout.addWidget(self.leave_button)
        layout.addWidget(self.app_icon_button)

        # Crear un widget central para la ventana y establecer el layout en él
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    def minimize_to_tray(self):
        self.hide()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('resources/icons/icon.png'))

        # Crear un menú de clic derecho para el icono de la bandeja del sistema
        quit_action = QAction("Salir", self)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('Loki - Asistente de voz')
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            
if __name__ == "__main__":
    app = QApplication([])
    window = RoundedWindow()
    window.show()
    app.exec_()