import wget
import argparse
import tqdm
import os
import zipfile

def extract_metainfo(zip_path, target_dir):
    with zipfile.ZipFile(zip_path, "r") as fp:
        for fileinfo in fp.infolist():
            if fileinfo.is_dir():
                continue
            orig_filename = fileinfo.filename
            target_filename = orig_filename.replace("metainfo" + os.sep, "")
            target_path = os.path.join(target_dir, target_filename)
            dirname = os.path.dirname(target_path)
            if dirname != "":
                os.makedirs(dirname, exist_ok=True)
            fileinfo.filename = os.path.basename(target_path)
            fp.extract(orig_filename, os.path.dirname(target_path))


def extract_images(zip_path, orig_folder_name, target_dir):
    with zipfile.ZipFile(zip_path, "r") as fp:
        for fileinfo in tqdm.tqdm(fp.infolist(), desc=f"Extracting: {orig_folder_name}"):
            if fileinfo.is_dir():
                continue
            orig_filename = fileinfo.filename
            target_filename = orig_filename.replace(orig_folder_name, "images")
            target_path = os.path.join(target_dir, target_filename)
            #target_path = os.path.dirname(target_path)
            dirname = os.path.dirname(target_path)
            if dirname != "":
                print("Creating:", dirname)
                os.makedirs(dirname, exist_ok=True)
            fileinfo.filename = os.path.basename(target_path)
#            target_dir = os.path.dirname(target_path)
            fp.extract(orig_filename, os.path.dirname(target_path))


def download(url, target_path):
    if os.path.isfile(target_path):
        print(f"File already downloaded: {target_path}. Skipping download")
        return
    print("Downloading:", url)
    wget.download(url, target_path)



parser = argparse.ArgumentParser()
parser.add_argument("--target_directory", default=os.path.join("data", "fdf"))
parser.add_argument("--download_images", default=False, action="store_true")
args = parser.parse_args()

os.makedirs(args.target_directory, exist_ok=True)


fdf_metainfo_url = "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/87c06e58-a6cc-4299-81b6-c36f2bed6a0ce5810e37-59d6-4d8f-9e86-fdafe7b58c86106c2d7d-91e8-4c80-986a-0ccdbe02ddb0"

print("Downloading metainfo")
metainfo_path = os.path.join(args.target_directory, "metainfo.zip")
download(fdf_metainfo_url, metainfo_path)

extract_metainfo(metainfo_path, args.target_directory)

if not args.download_images:
    exit(0)

image_urls = {
    "cc-by-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/30d325f8-f726-4974-96d5-5cb351f58db378d1ec02-3261-492d-a77d-194efc8e32d6becdc34b-0f1f-45ec-9a6a-dc2bff37f3d8",
    "cc-by-nc-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/e0dd287a-9a55-4082-a100-842279450bd9aa116eea-73fd-42e3-8b6a-6e3bb3e5629b765d7093-c784-4c69-90b2-694adf76c992",
    "cc-by-nc-sa-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/cc32f149-d109-4e1e-ae6d-aa92dc10148e56a00d43-8d11-4ce4-b5f9-5ac4419bc86b2b3cfe29-74dd-4ef1-893f-f87b41170b12",
    "cc-by-sa-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/21aeaf4d-c6e9-4dfe-86ce-2203601623bfa9028100-9e89-49eb-8426-99eccd5ea7ac06082e81-0c2e-45b4-827d-a4abae7a9e78"
}

for image_license, image_url in image_urls.items():
    print("Downloading images with license:", image_license)
    filename = f"{image_license}.zip"
    target_path = os.path.join(args.target_directory, filename)
    download(image_url, target_path)
    extract_images(target_path, image_license, args.target_directory)

