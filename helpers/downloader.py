from pathlib import Path

import requests


def download_to_local(url: str, destination_path: Path, parent_makedir: bool = True):
    if not isinstance(destination_path, Path):
        raise ValueError(f'{destination_path} must be a Path object')
    if parent_makedir:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        destination_path.write_bytes(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False
