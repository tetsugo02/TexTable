import tkinter as tk
from tkinter import filedialog, scrolledtext
from TexTableConverter import TexTableConverter
import pyperclip

convert = TexTableConverter()


def launch_gui() -> None:
    global output_text, root, frame, button_frame, status_label
    root = tk.Tk()
    root.title("LaTeX Table Converter")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    open_button = tk.Button(frame, text="Open file", command=open_file)
    open_button.pack(pady=10)

    # 横にボタンを並べるためのフレーム
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=5)

    copy_button = tk.Button(frame, text="Copy to clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    # 出力エリア
    output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
    output_text.pack(expand=True, fill=tk.BOTH, pady=5)

    # ステータスメッセージを表示するラベル
    status_label = tk.Label(frame, text="", fg="green")
    status_label.pack(pady=5)

    root.mainloop()


def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[
            ("Excel Files", "*.xlsx"),
            (".csv Files", "*.csv"),
            ("All Files", "*.*"),
        ]
    )
    if not filepath:
        return

    extension = filepath.split(".")[-1]
    try:
        convert.open_file(filepath)
    except FileNotFoundError:
        show_status_message(f"File '{filepath}' not found.", error=True)
        return

    match extension:
        case "csv":
            display_csv_sheet()
        case "xlsx":
            display_sheet_buttons(filepath)


def display_csv_sheet():
    # 既存のボタンをクリア
    for widget in button_frame.winfo_children():
        widget.destroy()
    latex_code = convert.convert_to_latex("CSV")
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, latex_code)
    copy_to_clipboard()
    show_status_message("CSV file opened and copied successfully.")


def display_sheet_buttons(filepath: str):
    # 既存のボタンをクリア
    for widget in button_frame.winfo_children():
        widget.destroy()

    # シート名ごとにボタンを横に並べて作成
    sheet_names = convert.sheet_names
    for i, sheet in enumerate(sheet_names):
        button = tk.Button(
            button_frame,
            text=sheet,
            command=lambda s=sheet: display_excel_sheet(filepath, s),
        )
        # xlsxファイル開いたら、最初のシートを表示
        display_excel_sheet(filepath, sheet_names[0])
        button.grid(row=0, column=i, padx=5, pady=5)


def display_excel_sheet(filepath: str, sheet_name: str):
    latex_code = convert.convert_to_latex(sheet_name)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, latex_code)
    copy_to_clipboard()
    show_status_message(f"Sheet '{sheet_name}' copied successfully.")


def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END))


def show_status_message(message: str, error: bool = False):
    """ステータスメッセージを一時的に表示する"""
    status_label.config(text=message, fg="red" if error else "green")
    root.after(5000, lambda: status_label.config(text=""))  # 3秒後にメッセージを消す
