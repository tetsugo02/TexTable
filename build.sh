python -m nuitka --standalone\
  --enable-console \
  --macos-create-app-bundle --macos-app-icon="./public/icon.icns" \
  --follow-imports --include-module=tkinter --include-module=pyperclip \
  TexTable.py
