import os

def does_fs_entry_exists(filename: str) -> bool:
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

def does_fdir_exists(filename: str) -> bool:
    try:
        return (os.stat(filename)[0] & 0x4000) != 0
    except OSError:
        return False

def does_file_exists(filename: str) -> bool:
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False
