import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from TexTableConverter import TexTableConverter
from copy_to_clipboard import copy_to_clipboard


class LaTeXTableConverterApp:
    """LaTeX Table ConverterのGUIアプリ"""

    def __init__(self):
        self.converter = TexTableConverter()
        self.root = tk.Tk()
        self.root.title("LaTeX Table Converter")
        self.root.geometry("800x600")

        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        """GUIの各ウィジェットを作成"""
        self.root_frame = tk.Frame(self.root, padx=10, pady=10)
        self.root_frame.pack(expand=True, fill="both")

        self.create_menu_buttons()
        self.create_output_area()
        self.create_status_and_worksheet_box()

    def create_menu_buttons(self):
        """ファイル操作とコピーのボタンを作成"""
        button_frame = tk.Frame(self.root_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=5)

        tk.Button(
            button_frame, text="Open File", command=self.open_file, width=20, height=2
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=lambda: copy_to_clipboard(self.output_text.get(1.0, tk.END)),
            height=2,
        ).grid(row=0, column=1, padx=5)

        tk.Label(self.root_frame, text="Select Format:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.format_menu = ttk.Combobox(
            self.root_frame, values=["horizontal", "vertical"], state="readonly"
        )
        self.format_menu.set("horizontal")
        self.format_menu.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.format_menu.bind("<<ComboboxSelected>>", self.update_table_format)

    def create_output_area(self):
        """出力エリアの作成"""
        self.output_text = scrolledtext.ScrolledText(
            self.root_frame, wrap=tk.WORD, height=15
        )
        self.output_text.grid(
            row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=10
        )

    def create_status_and_worksheet_box(self):
        """ステータスラベルとワークシートボックスの作成"""
        self.status_label = tk.Label(self.root_frame, text="", fg="green")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.worksheet_box = tk.Frame(self.root_frame)
        self.worksheet_box.grid(
            row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )

    def configure_grid(self):
        """ウィンドウのサイズ変更に追従する設定"""
        self.root_frame.grid_rowconfigure(2, weight=1)
        self.root_frame.grid_rowconfigure(4, weight=1)
        self.root_frame.grid_columnconfigure(1, weight=1)

    def open_file(self):
        """ファイルを開く処理"""
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Excel Files", "*.xlsx"),
                (".csv Files", "*.csv"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath:
            return

        try:
            self.converter.open_file(filepath)
            if filepath.endswith(".csv"):
                self.display_csv_sheet()
            else:
                self.display_sheet_buttons()
        except FileNotFoundError:
            self.show_status_message(f"File '{filepath}' not found.", error=True)

    def display_sheet_buttons(self):
        """Excelシートのボタンを表示"""
        self.clear_buttons()
        sheet_names = self.converter.sheet_names

        for index, sheet in enumerate(sheet_names):
            row, col = divmod(index, 7)
            tk.Button(
                self.worksheet_box,
                text=sheet,
                command=lambda s=sheet: self.display_excel_sheet(s),
            ).grid(row=row, column=col, padx=5, pady=5)

        self.display_excel_sheet(sheet_names[0])

    def display_csv_sheet(self):
        """CSVファイルの内容を表示"""
        self.clear_buttons()
        latex_code = self.converter.convert_to_latex("CSV")
        self.update_output_and_copy(
            latex_code, "CSV file opened and copied successfully."
        )

    def display_excel_sheet(self, sheet_name):
        """指定されたExcelシートの内容を表示"""
        latex_code = self.converter.convert_to_latex(sheet_name)
        self.update_output_and_copy(
            latex_code, f"Sheet '{sheet_name}' copied successfully."
        )

    def update_table_format(self, event):
        """テーブル形式を更新"""
        table_format = self.format_menu.get()
        self.converter.set_table_format(table_format)
        latex_code = self.converter.convert_to_latex(self.converter.sheet_names[0])
        self.update_output_and_copy(
            latex_code, f"Table format set to '{table_format}'."
        )

    def update_output_and_copy(self, latex_code, message):
        """出力エリアの更新とクリップボードへのコピー"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, latex_code)
        copy_to_clipboard(latex_code)
        self.show_status_message(message)

    def show_status_message(self, message, error=False):
        """ステータスラベルの更新"""
        self.status_label.config(text=message, fg="red" if error else "green")
        self.root.after(5000, lambda: self.status_label.config(text=""))

    def clear_buttons(self):
        """ワークシートボックス内のボタンをクリア"""
        for widget in self.worksheet_box.winfo_children():
            widget.destroy()

    def run(self):
        """GUIのメインループを開始"""
        self.root.mainloop()


if __name__ == "__main__":
    app = LaTeXTableConverterApp()
    app.run()
