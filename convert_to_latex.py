import pandas as pd

def excel_to_latex(filepath:str) -> str:
    df = pd.read_excel(filepath, engine='openpyxl')
    df = df.dropna(how='all')  # Drop rows where all elements are NaN
    df = df.dropna(axis=1, how='all')  # Drop columns where all elements are NaN
    latex_code = df.to_latex(index=False, escape=False)
    return latex_code

def csv_to_latex(filepath:str) -> str:
    df = pd.read_csv(filepath)
    df = df.dropna(how='all')  # Drop rows where all elements are NaN
    df = df.dropna(axis=1, how='all')  # Drop columns where all elements are NaN
    latex_code = df.to_latex(index=False, escape=False)
    return latex_code