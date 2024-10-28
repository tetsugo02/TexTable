import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from convert_to_latex import csv_to_latex

def launch_gui()->None:
  root = tk.Tk()
  root.title("LaTeX Table Converter")
  
  frame = tk.Frame(root, padx=10, pady=10)
  frame.pack(expand=True,fill='both')
  
  open_button = tk.Button(frame, text="Open file")# TODO 開く機能追加
  open_button.pack(pady=10)
  
  copy_button = tk.Button(frame, text="Copy to clipboard")# TODO コピー機能追加
  copy_button.pack(pady=10)
  
  root.mainloop()