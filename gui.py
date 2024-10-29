import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from TexTableConverter import TexTableConverter
import pyperclip

convert = TexTableConverter()


def launch_gui() -> None:
    global output_text, root, frame, button_frame
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
        messagebox.showerror("Error", f"File '{filepath}' not found.")
        return

    match extension:
        case "csv":
            latex_code = convert.convert_to_latex("CSV")
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, latex_code)
            copy_to_clipboard()
            messagebox.showinfo("Success", "CSV file opened successfully.")
        case "xlsx":
            display_sheet_buttons(filepath)


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
        button.grid(row=0, column=i, padx=5, pady=5)


def display_excel_sheet(filepath: str, sheet_name: str):
    latex_code = convert.convert_to_latex(sheet_name)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, latex_code)
    copy_to_clipboard()
    


def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END))
