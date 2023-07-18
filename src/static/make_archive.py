import logging
import os
import zipfile
from pathlib import Path
from typing import Optional

THIS_FOLDER = Path(__file__).parent.resolve()


def make_archive(folder: Path, zip_handle, base_folder: Optional[Path] = None):
    for file in folder.rglob("*"):
        if file.is_file() and not str(file).endswith(".Tests.ps1"):
            arcname = str(file.relative_to(base_folder)) if base_folder else str(file.name)
            zip_handle.write(str(file), arcname)


if __name__ == "__main__":
    cwd = os.curdir

    try:
        os.chdir(THIS_FOLDER)

        for path in THIS_FOLDER.iterdir():
            if not path.is_dir():
                continue

            with zipfile.ZipFile(f"{path.stem}.zip", "w", zipfile.ZIP_DEFLATED) as zipfile_handle:
                make_archive(path.resolve(), zipfile_handle, base_folder=path.resolve())
    except Exception as ex:
        logging.error(f"make archive error: {ex}")
    finally:
        os.chdir(cwd)
