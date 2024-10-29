from TexTableConverter import TexTableConverter

convert 
def csv_to_latex(filepath: str) -> str:
    df = read_csv(filepath)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    latex_code = df.to_latex(
        index=False, escape=False, column_format="c" * len(df.columns)
    )
    return add_header_footer(latex_code)


def add_header_footer(latex_code: str) -> str:
    entire_talbe_code: str = (
        "\\begin{table}[H]\n"
        "\\centering\n"
        "\\caption{}\n"
        "\\label{table:}\n"
        "\\end{table}"
    )
    return entire_talbe_code
