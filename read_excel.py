import pylightxl as xl


class ExcelReader:

    def __init__(self):
        self.file_path: str = None
        self.file_datas = []  # リストとして初期化
        self.sheet_names: list = None

    def open_file(self, file_path: str) -> None:
        file = xl.readxl(file_path)
        self.file_path = file_path
        self.sheet_names = file.ws_names

        for sheet_name in self.sheet_names:
            self.file_datas.extend(file.ws(sheet_name).rows)

    def get_sheet_names(self) -> list:
        return self.sheet_names

    def get_sheet_data(self):
        return self.file_datas
