import pylightxl as xl
import csv
import chardet


class TexTableConverter:

    def __init__(self):
        self.file_path: str = None
        self.file_datas: dict[str, list] = {}  # シートごとのデータを格納
        self.sheet_names: list[str] = []
        self.file_type: str = None
        self.table_format: str = "horizontal"

    def open_file(self, file_path: str) -> None:

        file_type = file_path.split(".")[-1]
        if file_type == "csv":
            encode_style = "utf-8"
            try:
                with open(file_path, "rb") as f:
                    encode_style = chardet.detect(f.read())["encoding"]

                with open(file_path, "r", newline="", encoding=encode_style) as f:
                    reader = csv.reader(f)
                    data = [row for row in reader]
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{file_path}' not found.")
            except Exception as e:
                raise RuntimeError(f"Failed to open the file: {e}")

            self.file_type = "csv"
            self.file_path = file_path
            self.sheet_names = ["CSV"]
            self.file_datas["CSV"] = self._remove_empty_rows_and_columns(data)

        elif file_type == "xlsx":
            try:
                file = xl.readxl(file_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{file_path}' not found.")
            except Exception as e:
                raise RuntimeError(f"Failed to open the file: {e}")

            self.file_path = file_path
            self.sheet_names = file.ws_names
            self.file_type = "xlsx"

            for sheet_name in self.sheet_names:
                # イテレータをリストに変換し、空の行・列を削除する
                raw_data = list(file.ws(sheet_name).rows)
                cleaned_data = self._remove_empty_rows_and_columns(raw_data)
                self.file_datas[sheet_name] = cleaned_data
        else:
            raise ValueError("File type must be 'csv' or 'xlsx '.")

    def _remove_empty_rows_and_columns(self, data: list) -> list:
        # 行全体がNoneまたは空文字("")のものを削除
        cleaned_rows = [
            row for row in data if any(cell not in [None, ""] for cell in row)
        ]

        # 列の削除（全行の同じインデックスがNoneまたは空文字なら削除）
        if cleaned_rows:
            transposed = list(zip(*cleaned_rows))  # 行と列を入れ替え
            cleaned_columns = [
                col for col in transposed if any(cell not in [None, ""] for cell in col)
            ]
            return [list(row) for row in zip(*cleaned_columns)]  # 元の行列構造に戻す
        return cleaned_rows

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

    def convert_to_latex(self, sheet_name: str) -> str:
        data = self.get_sheet_data(sheet_name)
        latex_code = self._generate_latex_table(data, self.table_format)
        return latex_code

    def set_table_format(self, format: str) -> None:
        if format in ["horizontal", "vertical"]:
            self.table_format = format
        else:
            raise ValueError("Table format must be 'horizontal' or 'vertical'.")

    def _generate_latex_table(self, data: list, format: str = "horizontal") -> str:
        table = []
        table.append(
            "\\begin{table}[H]\n"
            + "   \\centering\n"
            + "   \\caption{}\n"
            + "   \\label{table:}"
        )
        match format:
            case "horizontal":
                for i, row in enumerate(data):
                    if i == 0:
                        table.append("   " + "\\begin{tabular}{" + "c" * len(row) + "}")
                        table.append("   " + "\\hline")
                        table.append(
                            "   "
                            + " & ".join(
                                check_and_replace_null(str(cell)) for cell in row
                            )
                            + " \\\\"
                        )
                        table.append("   " + "\\hline")
                    else:
                        table.append(
                            "     "
                            + " & ".join(
                                check_and_replace_null(str(cell)) for cell in row
                            )
                            + " \\\\"
                        )

                table.append("  \\hline")
                table.append("  \\end{tabular}")

            case "vertical":
                for i, row in enumerate(data):
                    if i == 0:
                        table.append(
                            "   " + "\\begin{tabular}{|" + "c|" * len(row) + "}"
                        )
                        table.append("   " + "\\hline")
                        table.append(
                            "   "
                            + " & ".join(
                                check_and_replace_null(str(cell)) for cell in row
                            )
                            + " \\\\"
                        )
                    else:
                        table.append("   \\hline")
                        table.append(
                            "     "
                            + " & ".join(
                                check_and_replace_null(str(cell)) for cell in row
                            )
                            + " \\\\"
                        )
                table.append("  \\hline")
                table.append("  \\end{tabular}")

        table.append("\\end{table}")
        return "\n".join(table)


def check_and_replace_null(str: str) -> str:
    if str == "":
        return "~"
    return str
