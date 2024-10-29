import pylightxl as xl


class ExcelReader:

    def __init__(self):
        self.file_path: str = None
        self.file_datas: dict[str, list] = {}  # シート名をキーとした辞書形式
        self.sheet_names: list[str] = []

    def open_file(self, file_path: str) -> None:
        try:
            file = xl.readxl(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to open the file: {e}")

        self.file_path = file_path
        self.sheet_names = file.ws_names

        for sheet_name in self.sheet_names:
            # イテレータをリストに変換して保存
            self.file_datas[sheet_name] = list(file.ws(sheet_name).rows)

    def get_sheet_names(self) -> list[str]:
        return self.sheet_names

    def get_sheet_data(self, sheet_name: str = None) -> dict | list:
        if sheet_name:
            if sheet_name in self.file_datas:
                return self.file_datas[sheet_name]
            else:
                raise ValueError(
                    f"Sheet name '{sheet_name}' not found in {self.sheet_names}."
                )
        else:
            return self.file_datas
