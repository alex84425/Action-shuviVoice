import os
import shutil
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()


def delete_files_with_subname(root_dir, subname):
    file_list = root_dir.glob(f"**/*{subname}")
    for file in file_list:
        Path.unlink(file)


if __name__ == "__main__":
    cwd = os.curdir

    try:
        os.chdir(THIS_FOLDER)
        delete_files_with_subname(THIS_FOLDER, ".Tests.ps1")
        for path in THIS_FOLDER.iterdir():
            if not path.is_dir():
                continue
            shutil.make_archive(base_name=str(path.stem), format="zip", root_dir=str(path.resolve()))
    finally:
        os.chdir(cwd)
