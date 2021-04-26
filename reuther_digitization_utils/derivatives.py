import os
import subprocess


def create_jp2s(tiff_filepaths, jp2_dir):
    openjpeg_opts = [
                "-r", "2.4",
                "-c", "[256,256],[256,256],[128,128]",
                "-b", "64,64",
                "-p", "RPCL",
                "-n", "7",
                "-SOP"]
    for tiff_filepath in tiff_filepaths:
        identifier, _ = os.path.splitext(os.path.basename(tiff_filepath))
        jp2_filepath = os.path.join(jp2_dir, f"{identifier}.jp2")
        if not os.path.exists(jp2_filepath):
            cmd = [
                "/usr/local/bin/opj_compress",
                "-i", tiff_filepath,
                "-o", jp2_filepath] + openjpeg_opts
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


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
