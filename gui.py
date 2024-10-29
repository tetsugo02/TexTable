import tkinter as tk
from tkinter import filedialog, scrolledtext
from TexTableConverter import TexTableConverter
import subprocess
import platform

convert = TexTableConverter()

def launch_gui() -> None:
    global output_text, root, frame, button_frame, status_label
    root = tk.Tk()
    root.title("LaTeX Table Converter")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    open_button = tk.Button(frame, text="Open file", command=open_file)
    open_button.pack(pady=10)

    button_frame = tk.Frame(frame)  # 横にボタンを並べるためのフレーム
    button_frame.pack(pady=5)

    copy_button = tk.Button(
        frame, text="Copy to clipboard", 
        command=lambda: copy_to_clipboard(output_text.get(1.0, tk.END))
    )
    copy_button.pack(pady=10)

    output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)  # 出力エリア
    output_text.pack(expand=True, fill=tk.BOTH, pady=5)

    status_label = tk.Label(frame, text="", fg="green")  # ステータスメッセージ用
    status_label.pack(pady=5)

    root.mainloop()

def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx"), (".csv Files", "*.csv"), ("All Files", "*.*")]
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
    for widget in button_frame.winfo_children():
        widget.destroy()
    latex_code = convert.convert_to_latex("CSV")
    update_output_and_copy(latex_code, "CSV file opened and copied successfully.")

def display_sheet_buttons(filepath: str):
    for widget in button_frame.winfo_children():
        widget.destroy()

    sheet_names = convert.sheet_names
    for i, sheet in enumerate(sheet_names):
        button = tk.Button(
            button_frame, text=sheet, 
            command=lambda s=sheet: display_excel_sheet(filepath, s)
        )
        button.grid(row=0, column=i, padx=5, pady=5)

    # 最初のシートを自動的に表示
    display_excel_sheet(filepath, sheet_names[0])

def display_excel_sheet(filepath: str, sheet_name: str):
    latex_code = convert.convert_to_latex(sheet_name)
    update_output_and_copy(latex_code, f"Sheet '{sheet_name}' copied successfully.")

def update_output_and_copy(latex_code: str, message: str):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, latex_code)
    copy_to_clipboard(latex_code)
    show_status_message(message)

def copy_to_clipboard(text: str):
    """OSに応じたクリップボード操作を実行"""
    try:
        if platform.system() == "Darwin":  # MacOSの場合
            process = subprocess.Popen("pbcopy", stdin=subprocess.PIPE, close_fds=True)
            process.communicate(text.encode("utf-8"))
        elif platform.system() == "Linux":  # Linuxの場合
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, close_fds=True
            )
            process.communicate(text.encode("utf-8"))
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")

def show_status_message(message: str, error: bool = False):
    status_label.config(text=message, fg="red" if error else "green")
    root.after(5000, lambda: status_label.config(text=""))
