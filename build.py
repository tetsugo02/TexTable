import platform
import subprocess
import sys
import os


def build_command():
    """OSに応じたNuitkaのビルドコマンドを作成"""

    # TexTable.py の絶対パスを設定
    script_path = os.path.join(os.path.dirname(__file__), "src/TexTable.py")

    # 出力先を build ディレクトリに設定
    output_dir = os.path.join(os.path.dirname(__file__), "build")

    # Nuitkaビルドコマンドの基本部分
    base_command = [
        sys.executable,  # 現在使用しているPythonの実行パス
        "-m",
        "nuitka",
        "--standalone",  # 依存ライブラリをバンドル
        "--follow-imports",  # インポートをすべて追跡
        "--include-module=tkinter",  # tkinterの明示的な含有
        f"--output-dir={output_dir}",  # 出力先ディレクトリを指定
        script_path,  # ビルド対象のスクリプト
    ]

    # OSごとの設定
    system = platform.system()
    if system == "Darwin":  # macOS
        icon_path = os.path.join(os.path.dirname(__file__), "public/icon.icns")
        base_command.extend(
            [
                "--macos-create-app-bundle",  # macOS向けのAppバンドル
                f"--macos-app-icon={icon_path}", 
            ]
        )
    elif system == "Windows":  # Windows
        icon_path = os.path.join(os.path.dirname(__file__), "public/icon.ico")
        base_command.extend(
            [   
                "--windows-disable-console",
                "--onefile",  
                "--enable-plugin=tk-inter", 
            ]
        )
    elif system == "Linux":  # Linux
        base_command.append("--onefile")
        print("Building for Linux...")

    return base_command


def main():
    try:
        # ビルドコマンドを生成
        command = build_command()
        print("Running build command:")
        print(" ".join(command))

        result = subprocess.run(command, check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
