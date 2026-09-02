from os import listdir, mkdir
from os.path import exists, join, isfile
from shutil import copy, rmtree

def copystatic():
    if exists('public'):
        rmtree('public')
    mkdir('public')
    copy_files_recursive('static', 'public')
    

def copy_files_recursive(src_dir_path: str, dst_dir_path: str):
    entry_names = listdir(src_dir_path)
    for entry_name  in entry_names:
        src_path = join(src_dir_path, entry_name )
        dst_path = join(dst_dir_path, entry_name )
        if isfile(src_path):
            print(f"Copying file: '{src_path}' -> '{dst_path}'")
            copy(src_path, dst_path)
        else:
            print(f"Creating new directory: '{dst_path}'")
            mkdir(dst_path)
            copy_files_recursive(src_path, dst_path)


