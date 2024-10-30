import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from TexTableConverter import TexTableConverter
from copy_to_clipboard import copy_to_clipboard

convert = TexTableConverter()

def launch_gui() -> None:
    """GUIのメインウィンドウを起動"""
    global root, output_text, status_label, worksheet_box, button_frame

    root = tk.Tk()
    root.title("LaTeX Table Converter")
    root.geometry("800x600")

    root_frame = create_root_frame(root)
    create_menu_buttons(root_frame)
    create_output_area(root_frame)
    create_status_and_worksheet_box(root_frame)

    # ウィンドウサイズ変更に追従する設定
    configure_grid(root_frame)

    root.mainloop()

def create_root_frame(root):
    """メインのフレームを作成"""
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill="both")
    return frame

def create_menu_buttons(parent):
    """ファイル操作とコピーのボタンを作成"""
    global button_frame
    button_frame = tk.Frame(parent)
    button_frame.grid(row=0, column=0, columnspan=2, pady=5)

    tk.Button(button_frame, text="Open File", command=open_file).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(output_text.get(1.0, tk.END))).grid(row=0, column=1, padx=5)

    tk.Label(parent, text="Select Format:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    format_menu = ttk.Combobox(parent, values=["horizontal", "vertical"], state="readonly")
    format_menu.set("horizontal")
    format_menu.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

def create_output_area(parent):
    """出力テキストエリアを作成"""
    global output_text
    output_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=15)
    output_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

def create_status_and_worksheet_box(parent):
    """ステータスラベルとシート選択ボックスを作成"""
    global status_label, worksheet_box

    status_label = tk.Label(parent, text="", fg="green")
    status_label.grid(row=3, column=0, columnspan=2, pady=5)

    worksheet_box = tk.Frame(parent)
    worksheet_box.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

def configure_grid(parent):
    """ウィンドウ拡大時のリサイズ設定"""
    parent.grid_rowconfigure(2, weight=1)  # テキストエリアの行を拡大
    parent.grid_rowconfigure(4, weight=1)  # ワークシートボックスも拡大
    parent.grid_columnconfigure(1, weight=1)  # メニューとテキストエリアの列も拡大

def open_file():
    """ファイルを開く処理"""
    filepath = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx"), (".csv Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        convert.open_file(filepath)
        extension = filepath.split(".")[-1]
        if extension == "csv":
            display_csv_sheet()
        else:
            display_sheet_buttons(filepath)
    except FileNotFoundError:
        show_status_message(f"File '{filepath}' not found.", error=True)

def display_csv_sheet():
    """CSVファイルの内容を表示"""
    clear_buttons()
    latex_code = convert.convert_to_latex("CSV")
    update_output_and_copy(latex_code, "CSV file opened and copied successfully.")

def display_sheet_buttons(filepath):
    """Excelの各シートのボタンを表示"""
    clear_buttons()
    sheet_names = convert.sheet_names
    max_columns = 7

    for index, sheet in enumerate(sheet_names):
        row, col = divmod(index, max_columns)
        tk.Button(
            worksheet_box,
            text=sheet,
            command=lambda s=sheet: display_excel_sheet(filepath, s)
        ).grid(row=row, column=col, padx=5, pady=5)

    display_excel_sheet(filepath, sheet_names[0])

def display_excel_sheet(filepath, sheet_name):
    """選択されたシートの内容を表示"""
    latex_code = convert.convert_to_latex(sheet_name)
    update_output_and_copy(latex_code, f"Sheet '{sheet_name}' copied successfully.")

def update_output_and_copy(latex_code, message):
    """出力エリアの更新とクリップボードへのコピー"""
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, latex_code)
    copy_to_clipboard(latex_code)
    show_status_message(message)


def show_status_message(message, error=False):
    """ステータスラベルの更新"""
    status_label.config(text=message, fg="red" if error else "green")
    root.after(5000, lambda: status_label.config(text=""))

def clear_buttons():
    """ボタンフレーム内のボタンをクリア"""
    for widget in worksheet_box.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    launch_gui()
