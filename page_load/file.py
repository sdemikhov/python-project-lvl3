from pathlib import Path


def make_dir(destination=None):
    if destination is None:
        path = Path.cwd()
    else:
        path = Path(destination)
        if not path.exists():
            path.mkdir()
    return path
