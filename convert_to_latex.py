import pandas as pd

def excel_to_latex(filepath:str) -> str:
    df = pd.read_excel(filepath, engine='openpyxl')
    latex_code = df.to_latex(index=False, escape=False)
    return latex_code

def csv_to_latex(filepath:str) -> str:
    df = pd.read_csv(filepath)
    latex_code = df.to_latex(index=False, escape=False)
    return latex_code