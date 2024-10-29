python -m nuitka --standalone\
  --enable-console \
  --onefile \
  --follow-imports --include-module=tkinter --include-module=pyperclip \
  TexTable.py


