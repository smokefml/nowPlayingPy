import subprocess

def kitty_icat(path, x=0, y=0, w=36, h=36):
    cmd = [
            "kitty", "+kitten", "icat",
            "--silent",
            "--transfer-mode=memory",
            f"--place={w}x{h}@{x}x{y}",
            "--align", "left",
            "--stdin", "no",
            path
        ]
    subprocess.run(cmd)
