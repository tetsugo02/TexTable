import platform
import subprocess
import sys


def build_command():
    """OSに応じたNuitkaのビルドコマンドを作成"""
    base_command = [
        sys.executable,  # 現在使用しているPythonの実行パス
        "-m",
        "nuitka",
        "--standalone",  # 依存ライブラリをバンドル
        "--enable-console",  # コンソール出力を有効化
        "--follow-imports",  # インポートをすべて追跡
        "--include-module=tkinter",  # tkinterの明示的な含有
        "TexTable.py",  # ビルド対象のスクリプト
    ]

    # プラットフォームごとのオプションを追加
    system = platform.system()
    if system == "Darwin":  # MacOS
        base_command.extend(
            [
                "--macos-create-app-bundle",  # MacOS向けのAppバンドル
                "--macos-app-icon=./public/icon.icns",  # アイコンの指定
            ]
        )
    elif system == "Windows":  # Windows
        base_command.extend(
            [
                '--windows-icon="./public/icon.ico"',  # Windowsのアイコン指定
            ]
        )
    elif system == "Linux":  # Linux
        # Linuxでは、追加の特別なオプションは必要ないことが多い
        base_command.extend("--onefile")  # 1つの実行可能ファイルにまとめる
        print("Building for Linux...")

    return base_command


def main():
    try:
        # ビルドコマンドを生成
        command = build_command()
        print("Running build command:")
        print(" ".join(command))

        # Nuitkaのビルドコマンドを実行
        result = subprocess.run(command, check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
