import click
import json
from pathlib import Path

@click.command()
@click.argument("filepath", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("--user_nsid", required=True)
def main(filepath, user_nsid):
    assert user_nsid is not None
    with open(filepath, "r") as fp:
        data = json.load(fp)
    for key, item in data.items():
        if item["user_nsid"] == user_nsid:
            print(f"Image {key} includes your username")

if __name__ == "__main__":
    main()

