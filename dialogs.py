from PyQt6.QtWidgets import *
from main import MainWindow

class file_chos(QFileDialog):
    def __init__(self, parent):
        super().__init__()
        self.parents = parent
    
    def exec(self):
        self.path,_ = self.getOpenFileName(
            self.parents,
            "Dosya Seçiniz",
            "",
            "CSV Dosyası (*.csv);;Tüm Dosyalar (*)"
        )
        return self.path

class json_chos(QFileDialog):
    def __init__(self, parent):
        super().__init__()
        self.parents = parent

    def exec(self):
        self.csv_path,_ = self.getOpenFileName(
            self.parents,
            "Dosya seçiniz",
            "",
            "JSON Dosyası (*.json);;Tüm Dosyalar (*)"
        )
        return self.csv_path

class csv_chos_folder(QFileDialog):
    def __init__(self,parent):
        super().__init__()
        self.parents = parent

    def exec(self):
        self.csv_folder_path = self.getExistingDirectory(
            self.parents,
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

class table_warning(QMessageBox):
    def __init__(self, name, parent):
        super().__init__()
        
        self.setParent = parent
        self.setWindowTitle("UYARI!!!")
        self.setText(f"VERİ TABANINDA {name} ADINDA BİR TABLO VAR! (Yine de devam etmek istiyor musunuz ?)")
        self.setStandardButtons(self.StandardButton.Yes | self.StandardButton.No)
        self.setIcon(self.Icon.Warning)

class table_error(QMessageBox):
    def __init__(self,  name, parent):
        super().__init__()

        self.setParent = parent
        self.setWindowTitle("HATA!!!")
        self.setText(f"{name} ADINDA BİR TABLOYA VERİ EKLENEMEDİ!")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)

class table_success(QMessageBox):
    def __init__(self,parent):
        super().__init__()

        self.setParent = parent
        self.setWindowTitle("SUCCESS")
        self.setText("Program başarıyla sonlandı :) ")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Information)