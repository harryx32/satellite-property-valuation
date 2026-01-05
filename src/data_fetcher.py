import os
import requests
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

BASE_URL = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static"


def fetch_and_save_image(lat, lon, save_path, zoom=18, size=256):
    if MAPBOX_TOKEN is None:
        raise ValueError("MAPBOX_TOKEN not found. Check .env file loading.")

    url = (
        f"{BASE_URL}/{lon},{lat},{zoom}/{size}x{size}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            return False
    except Exception:
        return False


def download_images_fast(
    df,
    output_dir,
    id_col="id",
    lat_col="lat",
    lon_col="long",
    zoom=18,
    size=256,
    max_images=None,
    workers=6,
    log_path=None
):
    """
    FAST downloader using parallel workers.
    - Resume supported
    - Much faster than serial
    - Safe if workers <= 8
    """

    if MAPBOX_TOKEN is None:
        raise ValueError("MAPBOX_TOKEN not found. Check .env file loading.")

    os.makedirs(output_dir, exist_ok=True)

    rows = list(df.iterrows())
    if max_images:
        rows = rows[:max_images]

    failed = []
    downloaded = 0

    def task(row):
        image_id = row[id_col]
        lat = row[lat_col]
        lon = row[lon_col]

        img_path = os.path.join(output_dir, f"{image_id}.png")

        if os.path.exists(img_path):
            return "skipped", image_id

        ok = fetch_and_save_image(lat, lon, img_path, zoom=zoom, size=size)

        if ok:
            return "downloaded", image_id
        else:
            return "failed", image_id

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(task, row)
            for _, row in rows
        ]

        for future in tqdm(as_completed(futures), total=len(futures)):
            status, image_id = future.result()

            if status == "downloaded":
                downloaded += 1
            elif status == "failed":
                failed.append(image_id)

    if log_path and failed:
        with open(log_path, "w") as f:
            for fid in failed:
                f.write(str(fid) + "\n")

    return {
        "downloaded": downloaded,
        "failed": len(failed),
        "total_attempted": len(rows)
    }
