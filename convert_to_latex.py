import pandas as pd

def excel_to_latex(filepath:str) -> str:
    df = pd.read_excel(filepath)
    df = df.dropna(how='all') #NaNになっている行を削除
    df = df.dropna(axis=1, how='all')  
    latex_code = df.to_latex(index=False, escape=False, column_format= 'c' * len(df.columns))
    return latex_code

def csv_to_latex(filepath:str) -> str:
    df = pd.read_csv(filepath)
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')  
    latex_code = df.to_latex(index=False, escape=False, column_format= 'c' * len(df.columns))
    return add_header_footer(latex_code)

def add_header_footer(latex_code:str) -> str:
        begin = latex_code.find("\\begin{tabular}")
        end = latex_code.rfind("\\end{tabular}") + len("\\end{tabular}")
        body_code = latex_code[begin:end]
        entire_talbe_code = (
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\caption{}\n"
        "\\label{table:}\n"
        f"{body_code}\n"
        "\\end{table}"
    )
        return entire_talbe_code
        