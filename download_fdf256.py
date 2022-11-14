import wget
import os
import zipfile
import click
from pathlib import Path
from hashlib import md5
md5sums = {
    "cc-by-2": "e45e313358a5912927ed3a8aa620b3b1",
    "cc-by-nc-2": "12c531a59a47783bca53d69b04653805",
    "cc-by-sa-2": "2cd40e77def0e14148530d7f250a199e",
    "cc-by-nc-sa-2": "afad28fdb033ae57ce5e5e2d95a6be18",
}

image_urls = {
    "cc-by-nc-sa-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/33bb6132-a30e-4169-a09e-48b94cd5e09010fd8f59-1db9-4192-96f0-83d18adf50b4ee3ab25c-b8f8-4c40-a8ba-eaa64d830412",
    "cc-by-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/cb545564-120f-4f35-8b68-63e59e4fd273b1c36452-21e7-4976-85dd-a86c0738ebc256264f20-f969-4a82-ae1c-f6345d8e8d1f",
    "cc-by-sa-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/4e5c27bd-f5fd-4dd3-bf2b-4434a8952df0ff4d11f8-e993-4517-9378-b35d89e7882ecae76ce7-88a0-417b-b5d8-e030863e97f6",
    "cc-by-nc-2": "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/da46d666-4378-4e75-9182-e683ebe08f2e9203750f-7ed8-42f7-8bce-90a7dfddd3764401df36-a3c3-4d39-ae8e-0cb4397e5c74",
}

fdf_metainfo_url = "https://api.loke.aws.unit.no/dlr-gui-backend-resources-content/v2/contents/links/b704049a-d465-4a07-9cb3-ca270ffab80292e4d5ac-6172-4d37-bf63-4438f61f8aa0e1f6483d-5d45-40b5-b356-10b71fc00e89"
fdf_metainfo_md5sum = "b790269bd64e9a6c1b1b032a9ff60410"

def extract_zip(zip_path: Path, target_path: Path):
    print(f"Extracting contents of {zip_path} to  {target_path}")
    with zipfile.ZipFile(zip_path, "r") as fp:
        fp.extractall(str(target_path))


def is_valid(filepath: Path, md5sum):
    with open(filepath, "rb") as fp:
        cur_md5sum = md5(fp.read()).hexdigest()
    print(cur_md5sum, md5sum)
    return cur_md5sum == md5sum


def download(url, target_path: Path, md5sum):
    target_path.parent.mkdir(exist_ok=True, parents=True)
    if target_path.is_file():
        if is_valid(target_path, md5sum):
            print(f"File already downloaded: {target_path}. Skipping download")
            return
        print("Downloaded file is not correct. Deleting old.", target_path)
        target_path.unlink()
    print("Downloading:", url)
    wget.download(url, str(target_path))
    assert is_valid(target_path, md5sum), "Downloaded file is not correct."


@click.command()
@click.argument("target_path")
def main(target_path):
    target_path = Path(target_path)
    download(fdf_metainfo_url, target_path.joinpath("metainfo.zip"), fdf_metainfo_md5sum)
    
    extract_zip(target_path.joinpath("metainfo.zip"), target_path)

    for image_license, image_url in image_urls.items():
        print("Downloading images with license:", image_license)
        download(image_url, target_path.joinpath(image_license + ".zip"), md5sums[image_license])
        extract_zip(target_path.joinpath(image_license + ".zip"), target_path)


main()