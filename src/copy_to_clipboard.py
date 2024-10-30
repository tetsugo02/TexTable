import subprocess
import platform


def copy_to_clipboard(text):
    """クリップボードにコピー"""
    try:
        if platform.system() == "Darwin":
            from AppKit import NSPasteboard, NSStringPboardType

            pb = NSPasteboard.generalPasteboard()
            pb.clearContents()
            pb.setString_forType_(text, NSStringPboardType)
        elif platform.system() == "Linux":
            subprocess.run(
                ["xclip", "-selection", "clipboard"], input=text.encode(), check=True
            )
        else:
            subprocess.run(["clip"], input=text.encode(), check=True)
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")
