import sys
from PyQt6.QtWidgets import QApplication
from core.environment_checker import check_environment
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    env_status = check_environment()
    
    window = MainWindow(env_status)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
