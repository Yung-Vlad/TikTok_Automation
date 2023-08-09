import os
from help_funcs import del_hash
import platform  # For checking os


# Video rename feature
def rename_file(tag, hashtags):
    down_folder = os.path.join(os.path.dirname(__file__), f"videos\\{del_hash(tag)}")
    downloaded_files = os.listdir(down_folder)
    downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(down_folder, x)), reverse=True)

    old_filename = os.path.join(down_folder, downloaded_files[0])
    new_filename = os.path.join(down_folder, hashtags) + ".mp4"

    os.rename(old_filename, new_filename)
    return hashtags + ".mp4"


# Reading hashtags and indexes from txt-file
def read_file():
    tags = []
    indexes = []
    with open("hashtags.txt") as file:
        for line in file:
            values = line.strip().split()
            tags.append(values[0])
            indexes.append(values[1])

    return tags, indexes


# Creating dirs for videos
def create_dir(name):
    project_directory = os.path.dirname(os.path.abspath(__file__))
    videos_folder_path = os.path.join(project_directory, "videos")

    name = del_hash(name)
    dir_path = os.path.join(videos_folder_path, name)

    if os.path.exists(dir_path):
        return dir_path

    os.makedirs(dir_path)
    return dir_path


# Checking count videos
def check_count_videos(tag):
    if platform.system() == "Windows":
        path = os.path.join(os.path.dirname(__file__), f"videos\\{del_hash(tag)}")
    else:
        path = os.path.join(os.path.dirname(__file__), f"videos/{del_hash(tag)}")

    count_videos = len(os.listdir(path))

    if count_videos == 0:
        with open("hashtags.txt") as file:
            lines = file.readlines()

        lines = [line for line in lines if tag not in line]

        with open("hashtags.txt", 'w') as file:
            file.writelines(lines)

        print(f"Videos with this tag: {tag} ended!")
        return False

    elif count_videos <= 10:
        print(f"There are {count_videos - 1} videos left with this tag: {tag}!")

    return True


# Deleting video
def del_video(video):
    os.remove(video)
