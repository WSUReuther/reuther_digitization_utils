import os

from reuther_digitization_utils.derivatives import create_derivative_images, create_pdf, compress_pdf, ocr_pdf
from reuther_digitization_utils.dir_structure import rename_files_in_directory
from reuther_digitization_utils.file_copying import check_create_remote_dir, copy_item_directory


class ItemUtils:

    def __init__(self, collection_dir, item_identifier, remote_scans_dir=None):
        self.collection_dir = collection_dir
        self.item_dir = os.path.join(self.collection_dir, item_identifier)
        self.tiffs_dir = os.path.join(self.item_dir, "preservation")
        self.access_dir = os.path.join(self.item_dir, "access")
        self.item_identifier = item_identifier
        self.remote_scans_dir = remote_scans_dir

    def generate_derivatives(self, derivative_type="jp2"):
        if derivative_type in ["jp2", "jpg"]:
            self.derivative_type = derivative_type
            self.derivatives_dir = os.path.join(self.access_dir, derivative_type)
        else:
            raise Exception(f"unsupported derivative type: {derivative_type}")
        self._check_create_derivative_dirs()
        derivative_images_resp = self._generate_derivative_images()
        pdf_resp = self._generate_pdf()
        return f"{derivative_images_resp}, {pdf_resp}"

    def rename_preservation_scans(self):
        success, error, message = rename_files_in_directory(self.tiffs_dir, self.item_identifier)
        if error:
            raise Exception(f"Error renaming files: {message}")
        else:
            return message

    def copy_item_to_remote_dir(self):
        if not self.remote_scans_dir:
            raise Exception("cannot copy files. no remote scans dir defined")
        check_create_remote_dir(self.remote_scans_dir)
        copy_item_directory(self.item_dir, self.remote_scans_dir)
        return f"copied to {self.remote_scans_dir}"

    def check_complete(self):
        return "function not implemented"

    def _check_create_derivative_dirs(self):
        if not os.path.exists(self.item_dir):
            raise Exception(f"Item directory not found: {self.item_dir}")
        if not os.path.exists(self.derivatives_dir):
            os.makedirs(self.derivatives_dir)

    def get_derivative_filepaths(self):
        return [os.path.join(self.derivatives_dir, filename) for filename in os.listdir(self.derivatives_dir) if filename.endswith(self.derivative_type)]

    def get_tiff_filepaths(self):
        return [os.path.join(self.tiffs_dir, filename) for filename in os.listdir(self.tiffs_dir) if filename.endswith(".tif")]

    def get_pdf_filepath(self):
        return os.path.join(self.access_dir, f"{self.item_identifier}_001.pdf")

    def _generate_derivative_images(self):
        tiff_filepaths = self.get_tiff_filepaths()
        if tiff_filepaths:
            derivative_filepaths = self.get_derivative_filepaths()
            if len(tiff_filepaths) == len(derivative_filepaths):
                return f"an equal number of {self.derivative_type}s to tiffs already exist"
            else:
                create_derivative_images(tiff_filepaths, self.derivatives_dir, derivative_type=self.derivative_type)
                return "created derivative images"
        else:
            raise Exception(f"Error creating derivative images. No TIFF files found for {self.item_identifier}")

    def _generate_pdf(self):
        image_filepaths = self.get_derivative_filepaths()
        if image_filepaths:
            pdf_filepath = self.get_pdf_filepath()
            if not os.path.exists(pdf_filepath):
                create_pdf(image_filepaths, pdf_filepath)
                compress_pdf(pdf_filepath)
                ocr_pdf(pdf_filepath)
                return "PDF created"
            else:
                return "PDF already exists"
        else:
            raise Exception(f"Error creating PDF. No derivative images found for {self.item_identifier}")
