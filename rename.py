import os


def rename_files_in_directory(directory_path, prefix="file", file_extensions=[".xml", ".jpg"]):
    """
    Rename all files in the specified directory with the given prefix and supported extensions.

    :param directory_path: str, path to the directory containing the files to rename
    :param prefix: str, prefix to add to the renamed files
    :param file_extensions: list of str, list of file extensions to rename
    """
    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    # Initialize a counter for renaming
    counter = 1

    for file_name in files:
        # Get the file extension
        file_extension = os.path.splitext(file_name)[1].lower()

        # Check if the file has one of the desired extensions
        if file_extension in file_extensions:
            # Generate the new file name
            new_name = f"{prefix}_{counter}{file_extension}"

            # Get the full path to the old and new file
            old_file = os.path.join(directory_path, file_name)
            new_file = os.path.join(directory_path, new_name)

            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed '{file_name}' to '{new_name}'")

            # Increment the counter
            counter += 1


# Example usage
directory_path = "C:\\Users\\congy\\Desktop\\no_idle_cy\\img1"
rename_files_in_directory(directory_path, prefix="img")