import shutil
def delete_folders_with_name(root_dir, target_name):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for dir_name in dirs:
            if dir_name == target_name:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except OSError as e:
                    print(f"Error deleting folder {dir_path}: {e}")

isos = os.listdir(DATA_RESULTS)
for iso in isos:
    root_directory = os.path.join( DATA_RESULTS, iso)
    target_folder_name = 'unconnected_csv_files'
    delete_folders_with_name(root_directory, target_folder_name)