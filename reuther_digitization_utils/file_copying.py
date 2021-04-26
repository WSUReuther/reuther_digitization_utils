import os
import subprocess


def check_create_remote_dir(remote_dir):
    if not os.path.isdir(remote_dir):
        os.makedirs(remote_dir)


def copy_item_directories(collection_directory, destination_directory):
    item_dirnames = os.listdir(collection_directory)
    for item_dirname in item_dirnames:
        item_directory = os.path.join(collection_directory, item_dirname)
        if os.path.isdir(item_directory):
            copy_item_directory(item_directory, destination_directory)


def copy_item_directory(item_directory, destination_directory):
    cmd = [
        "rsync", "-t", "-q", "-r", item_directory, destination_directory
    ]
    subprocess.run(cmd)
