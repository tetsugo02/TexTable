import pandas as pd

def csv_to_latex(filepath:str) -> str:
    df = pd.read_csv(filepath)
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')  
    latex_code = df.to_latex(index=False, escape=False, column_format= 'c' * len(df.columns))
    return add_header_footer(latex_code)

def add_header_footer(latex_code:str) -> str:
        begin:int = latex_code.find("\\begin{tabular}")
        end:int = latex_code.rfind("\\end{tabular}") + len("\\end{tabular}")
        body_code:str = latex_code[begin:end]
        entire_talbe_code:str = (
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\caption{}\n"
        "\\label{table:}\n"
        f"{body_code}\n"
        "\\end{table}"
    )
        return entire_talbe_code
        