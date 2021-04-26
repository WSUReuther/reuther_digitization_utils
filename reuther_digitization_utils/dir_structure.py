import os


def create_directories(output_dir, collection_id, item_identifiers):
    """Creates a directory structure at output_dir consisting of a
    collection_id subdirectory with one or more item_identifier subdirectories
    """
    if not os.path.isdir(output_dir):
        raise Exception(f"Error creating directories: {output_dir} does not exist")
    collection_base_dir = os.path.join(output_dir, collection_id)
    if not os.path.exists(collection_base_dir):
        os.makedirs(collection_base_dir)
    for item_identifier in item_identifiers:
        item_directory = os.path.join(collection_base_dir, item_identifier)
        if not os.path.exists(item_directory):
            preservation_scans_dir = os.path.join(item_directory, "preservation")
            derivatives_dir = os.path.join(item_directory, "access")
            os.makedirs(preservation_scans_dir)
            os.makedirs(derivatives_dir)


def rename_files_in_directory(directory, identifier):
    """Renames individual page scans within an item directory to match Reuther guidelines.
    Excpects a directory with sequential numbered TIFFs (001.tif, 002.tif, etc.) and renames them
    to meet the following convention: [item_identifier]_[object_number].tif
    """
    renamed = False
    error = False
    message = ""

    if not os.path.isdir(directory):
        raise Exception(f"Error renaming files: {directory} does not exist")

    tiff_filenames = get_tiff_filenames(directory)
    if not tiff_filenames:
        raise Exception(f"Error renaming files: no TIFFs found in {directory}")

    qualifies_resp = check_qualifies_for_renaming(tiff_filenames, identifier)
    if qualifies_resp["qualifies"]:
        for tiff_filename in tiff_filenames:
            basename, ext = os.path.splitext(tiff_filename)
            if ext == ".tiff":
                ext = ".tif"
            parts = basename.rsplit("_", 1)
            if len(parts) == 1:
                object_number = int(parts[0])
            elif len(parts) == 2:
                object_number = int(parts[1])
            new_filename = f"{identifier}_{object_number:03}{ext}"
            if tiff_filename != new_filename:
                old_filepath = os.path.join(directory, tiff_filename)
                new_filepath = os.path.join(directory, new_filename)
                os.rename(old_filepath, new_filepath)
        renamed = True
        message = "files renamed"
    else:
        error = qualifies_resp["error"]
        message = qualifies_resp["message"]
    return renamed, error, message


def get_tiff_filenames(directory):
    return [filename for filename in os.listdir(directory) if filename.endswith(".tif") or filename.endswith(".tiff")]


def check_qualifies_for_renaming(filenames, identifier):
    """Runs some checks on existing filenames before renaming
    Checks the following conditions:
        - Filenames end in consecutive numbers (001, 002, 003, etc.)
        - If filenames start with an identifier component, confirm that it matches the item identifier
    """
    resp = {"qualifies": True, "error": False, "message": ""}
    identifiers_align = True
    object_numbers_ints = True
    object_numbers_align = True
    identifier_parts = []
    number_parts = []
    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        parts = basename.rsplit("_", 1)
        if len(parts) == 1:
            identifiers_align = False
            number_parts.append(parts[0])
        elif len(parts) == 2:
            identifier_part, number_part = parts
            identifier_parts.append(identifier_part)
            number_parts.append(number_part)
    if identifiers_align:
        for identifier_part in identifier_parts:
            if identifier_part != identifier:
                identifiers_align = False
                break
    for number_part in number_parts:
        if not number_part.isdigit():
            object_numbers_ints = False
            resp["qualifies"] = False
            resp["error"] = True
            resp["message"] = "existing filenames do not end in a numbered part (e.g., 001.tif)"
            break
    if object_numbers_ints:
        object_numbers = [int(number_part) for number_part in number_parts]
        if not expected(object_numbers):
            object_numbers_align = False
            resp["qualifies"] = False
            resp["error"] = True
            resp["message"] = "image numbers do not match expectations"
    if identifiers_align and object_numbers_ints and object_numbers_align:
        resp["qualifies"] = False
        resp["error"] = False
        resp["message"] = "files are already correctly named"
    return resp


def expected(object_numbers):
    """Confirms that object_numbers are a consecutive sequence beginning with 1
    """
    total = len(object_numbers)
    expected_range = list(range(1, total+1))
    return sorted(object_numbers) == expected_range
