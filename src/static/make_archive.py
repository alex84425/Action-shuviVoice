import os
import shutil
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()


if __name__ == "__main__":
    cwd = os.curdir

    try:
        os.chdir(THIS_FOLDER)

        for path in THIS_FOLDER.iterdir():
            if not path.is_dir():
                continue
            shutil.make_archive(base_name=str(path.stem), format="zip", root_dir=str(path.resolve()))
    finally:
        os.chdir(cwd)
