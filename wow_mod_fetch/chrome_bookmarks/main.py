import pathlib

from .classes import Bookmarks


def main(path=None):
    default_paths = [
        "~/.config/google-chrome/Default/Bookmarks",
        "~/.config/chromium/Default/Bookmarks",
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks",
        "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"]
    while not path and default_paths:
        dpath = default_paths.pop()
        try:
            try_path = pathlib.Path(dpath).expanduser()
        except (KeyError, RuntimeError):
            continue
        if try_path.exists():
            path = dpath
    full_path = pathlib.Path(path).expanduser().absolute()
    try:
        return Bookmarks(f"{full_path}")
    except Exception:
        return None
