import pandas as pd

class convert:
    def __init__(self,file_path):
        super().__init__()
        self.file_path = file_path
        self.liste = []
        self.sonuc = []
        self.ayirici = " "
    
    def exec(self):
        self.df = pd.read_csv(self.file_path, encoding="utf-8",delimiter=";")