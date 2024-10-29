import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext
from TexTableConverter import TexTableConverter
import pyperclip


convert = TexTableConverter()


def launch_gui() -> None:
    root = tk.Tk()
    root.title("LaTeX Table Converter")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    open_button = tk.Button(frame, text="Open file", command=open_file)
    open_button.pack(pady=10)

    copy_button = tk.Button(frame, text="Copy to clipboard")
    copy_button.pack(pady=10)

    global output_text  # コピー用にグローバル変数にする
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
            messagebox.showinfo("Success", "File opened successfully.")
        case "xlsx":
            pass


def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END))
