import os, shutil

def copy_folder(src, dest, new_folder_name=None, create_symlinks=False):
    """
    Copy a folder to a destination folder with an option to rename the folder
    and make the whole new folder a symbolic link instead of copying it.

    :param src: Source folder path to copy.
    :param dest: Destination folder path where the source will be copied.
    :param new_folder_name: (Optional) New name for the copied folder. If None, keeps the original folder name.
    :param create_symlinks: (Optional) Boolean flag to create a symlink for the whole folder instead of copying.
    """
    
    if not os.path.isdir(src):
        raise ValueError(f"The source path '{src}' is not a valid directory.")
    
    if not os.path.isdir(dest):
        raise ValueError(f"The destination path '{dest}' is not a valid directory.")
    
    # Determine the new folder name if provided or use the existing one
    folder_name = new_folder_name if new_folder_name else os.path.basename(src)
    new_dest = os.path.join(dest, folder_name)

    # If folder already exists, remove it
    if os.path.exists(new_dest):
        print(f"Warning: Folder '{new_dest}' already exists. It will be removed.")
        if os.path.isdir(new_dest):
            shutil.rmtree(new_dest)  # Remove existing folder
        else:
            os.remove(new_dest)  # Remove existing symlink if it's already there

    if create_symlinks:
        # Create a symbolic link for the entire folder instead of copying
        os.symlink(src, new_dest)
        #print(f"Created symbolic link from '{src}' to '{new_dest}'.")
    else:
        # Recursively copy the folder contents
        shutil.copytree(src, new_dest)
        #print(f"Folder copied successfully from '{src}' to '{new_dest}'.")

# Example usage:
# copy_folder('/path/to/source', '/path/to/destination', 'new_folder_name', create_symlinks=True)


# Example usage:
# copy_folder('/path/to/source', '/path/to/destination', 'new_folder_name', create_symlinks=True)

dataset_name = "val"
label_dir = "/home/robodev/Documents/BPC/Data/ipd/output/ipd"
image_dir = "/home/robodev/Documents/BPC/Data/ipd/{}_pbr".format(dataset_name)
output_dir = "/home/robodev/Documents/BPC/Data/ipd/" + dataset_name
scene_id = [i for i in range (10)]
cams = ["cam1", "cam2", "cam3"]

for cam in cams:
    for scene in scene_id:
        # os.makedirs(os.path.join(output_dir, "{data_name}_{cam}_{id:06d}".format(data_name=dataset_name,cam=cam,id=scene), "labels"), exist_ok=True)
        # os.makedirs(os.path.join(output_dir, "{data_name}_{cam}_{id:06d}".format(data_name=dataset_name,cam=cam,id=scene), "images"), exist_ok=True)
        copy_folder(os.path.join(label_dir, dataset_name + "_" +cam, "{id:06d}".format(id=scene)), 
                 dest=output_dir, new_folder_name="{data_name}_{cam}_{id:06d}/labels".format(data_name=dataset_name,cam=cam,id=scene))
        copy_folder(src=os.path.join(image_dir, "{id:06d}".format(id=scene), "rgb_"+cam), 
                 dest=output_dir, new_folder_name="{data_name}_{cam}_{id:06d}/images".format(data_name=dataset_name,cam=cam,id=scene),
                 create_symlinks=True)
        print("{data_name}_{cam}_{id:06d}".format(data_name=dataset_name,cam=cam,id=scene))