from PyQt6.QtWidgets import QMessageBox

def show_error(parent, title: str, message: str):
    QMessageBox.critical(parent, title, message)

def show_info(parent, title: str, message: str):
    QMessageBox.information(parent, title, message)

def show_warning(parent, title: str, message: str):
    QMessageBox.warning(parent, title, message)
