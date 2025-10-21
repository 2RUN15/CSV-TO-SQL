from PyQt6.QtWidgets import *
from main import MainWindow

class file_chos:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def exec(self):
        self.path,_ = QFileDialog.getOpenFileName(
            self.parent,
            "Dosya Seçiniz",
            "",
            "CSV Dosyası (*.csv);;Tüm Dosyalar (*)"
        )
        return self.path

class json_chos:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def exec(self):
        self.csv_path,_ = QFileDialog.getOpenFileName(
            self.parent,
            "Dosya seçiniz",
            "",
            "JSON Dosyası (*.json);;Tüm Dosyalar (*)"
        )
        return self.csv_path

class csv_chos_folder:
    def __init__(self,parent):
        super().__init__()
        self.parent = parent

    def exec(self):
        self.csv_folder_path = QFileDialog.getExistingDirectory(
            self.parent,
            "Klasör seçniz",
            ""
        )
        return self.csv_folder_path

class json_error(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HATA")
        self.setText("Lütfen json dosyasını seçiniz!")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)

class warning_run(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UYARI!!!")
        self.setText("CSV dosya yolunu ve mysql connector bilgilerini giriniz!")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)