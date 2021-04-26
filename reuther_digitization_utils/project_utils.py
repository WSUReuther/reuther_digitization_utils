import os

from reuther_digitization_utils.dir_structure import create_directories
from reuther_digitization_utils.helpers import parse_csv
from reuther_digitization_utils.item_utils import ItemUtils


class ProjectUtils:

    def __init__(self, project_base_dir, project_csv, remote_scans_loc=None):
        project_metadata = parse_csv(project_csv)
        self.project_base_dir = project_base_dir
        self.collection_id = project_metadata["collection"]["collection_id"]
        self.collection_dir = os.path.join(self.project_base_dir, self.collection_id)
        self.items = project_metadata["items"]
        self.item_identifiers = [item["item_identifier"] for item in self.items]
        if remote_scans_loc:
            if not os.path.isdir(remote_scans_loc):
                raise Exception(f"remote scan directory not found: {remote_scans_loc}")
            self.remote_scans_dir = os.path.join(remote_scans_loc, self.collection_id)
        else:
            self.remote_scans_dir = False

    def setup_project(self):
        create_directories(self.project_base_dir, self.collection_id, self.item_identifiers)

    def item_for_identifier(self, item_identifier):
        return ItemUtils(self.collection_dir, item_identifier, remote_scans_dir=self.remote_scans_dir)
