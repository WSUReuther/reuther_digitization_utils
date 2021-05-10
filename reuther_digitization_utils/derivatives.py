import os
import subprocess

from PIL import Image


def create_derivative_images(tiff_filepaths, derivative_images_dir, derivative_type="jp2"):
    alpha_channels = check_alpha_channels(tiff_filepaths)
    if alpha_channels:
        raise Exception(f"Alpha channel detected. Remove alpha channels before proceeding. {'; '.join(alpha_channels)}")
    for tiff_filepath in tiff_filepaths:
        identifier, _ = os.path.splitext(os.path.basename(tiff_filepath))
        derivative_filepath = os.path.join(derivative_images_dir, f"{identifier}.{derivative_type}")
        if derivative_type == "jp2":
            create_jp2(tiff_filepath, derivative_filepath)
        elif derivative_type == "jpg":
            create_jpeg(tiff_filepath, derivative_filepath)


def check_alpha_channels(tiff_filepaths):
    alpha_channel_tiffs = []
    for tiff_filepath in tiff_filepaths:
        with Image.open(tiff_filepath) as img:
            if img.mode in ["RGBA", "LA"]:
                alpha_channel_tiffs.append(tiff_filepath)
    return alpha_channel_tiffs


def create_jp2(tiff_filepath, jp2_filepath):
    openjpeg_opts = [
                "-r", "2.4",
                "-c", "[256,256],[256,256],[128,128]",
                "-b", "64,64",
                "-p", "RPCL",
                "-n", "7",
                "-t", "512,512",
                "-I",
                "-SOP"]
    if not os.path.exists(jp2_filepath):
        cmd = [
            "/usr/local/bin/opj_compress",
            "-i", tiff_filepath,
            "-o", jp2_filepath] + openjpeg_opts
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def create_jpeg(tiff_filepath, jpeg_filepath):
    if not os.path.exists(jpeg_filepath):
        with Image.open(tiff_filepath) as input_img:
            icc_profile = input_img.info.get("icc_profile")
            if input_img.mode == "RGBA":
                input_img = input_img.convert(mode="RGB")
            input_img.save(jpeg_filepath, "JPEG", quality=92, icc_profile=icc_profile)


def create_pdf(image_filepaths, pdf_filepath):
    if not os.path.exists(pdf_filepath):
        cmd = ["img2pdf"] + sorted(image_filepaths) + ["-o", pdf_filepath]
        subprocess.run(cmd)


def compress_pdf(pdf_filepath):
    pdf_base_dir = os.path.dirname(pdf_filepath)
    pdf_base_filename, _ = os.path.splitext(os.path.basename(pdf_filepath))
    compressed_filepath = os.path.join(pdf_base_dir, f"{pdf_base_filename}_compressed.pdf")
    cmd = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS={}".format("/screen"), "-dNOPAUSE",
        "-dQUIET", "-dBATCH", f"-sOutputFile={compressed_filepath}",
        pdf_filepath
        ]
    subprocess.run(cmd)
    os.remove(pdf_filepath)
    os.rename(compressed_filepath, pdf_filepath)


def ocr_pdf(pdf_filepath):
    ocrmypdf_path_check = subprocess.run(["which", "ocrmypdf"], capture_output=True, encoding="utf-8")
    ocrmypdf_path = ocrmypdf_path_check.stdout.strip()
    if not ocrmypdf_path:
        raise Exception("PDF not OCR'd. Could not find ocrmypdf")
    cmd = [
        ocrmypdf_path,
        pdf_filepath, pdf_filepath,
        "--optimize", "0",
        "--quiet"]
    subprocess.run(cmd)
