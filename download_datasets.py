import os
import shutil
from pathlib import Path
import kagglehub

DATASETS = [
    {
        "handle": "fahruu/komentar-judi-online",
        "folder": "fahruu_komentar-judi-online",
        "description": "Dataset Komentar Judi Online by fahruu",
    },
    {
        "handle": "kyyyy8/dataset-komentar-judi-online-di-youtube",
        "folder": "kyyyy8_dataset-komentar-judi-online-di-youtube",
        "description": "Dataset Komentar Judi Online di YouTube by kyyyy8",
    },
    {
        "handle": "yaemico/deteksi-judi-online",
        "folder": "yaemico_deteksi-judi-online",
        "description": "Deteksi Judi Online by yaemico",
    },
    {
        "handle": "kyyyy8/dataset-komentar-judi-online-platform-youtube",
        "folder": "kyyyy8_dataset-komentar-judi-online-platform-youtube",
        "description": "Dataset Komentar Judi Online Platform YouTube by kyyyy8",
    },
    {
        "handle": "ferdiansakti/gambling-comments-from-youtube-platform",
        "folder": "ferdiansakti_gambling-comments-from-youtube-platform",
        "description": "Gambling Comments from YouTube Platform by ferdiansakti",
    },
]

def main():
    base_dir = Path(__file__).resolve().parent / "datasets"
    base_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Mulai mengunduh dan mengorganisir dataset ke folder terpisah")
    print(f"Direktori target: {base_dir}")
    print("=" * 60)

    summary = []

    for idx, item in enumerate(DATASETS, 1):
        handle = item["handle"]
        folder_name = item["folder"]
        target_dir = base_dir / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{idx}/{len(DATASETS)}] Mengunduh: {handle}...")
        try:
            download_path = Path(kagglehub.dataset_download(handle))
            print(f"   -> Kagglehub cache path: {download_path}")

            # Copy all files from cache to target folder
            copied_files = []
            for src_item in download_path.rglob("*"):
                if src_item.is_file():
                    rel_path = src_item.relative_to(download_path)
                    dest_file = target_dir / rel_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_item, dest_file)
                    copied_files.append((dest_file.name, dest_file.stat().st_size))

            print(f"   -> Berhasil disalin ke: {target_dir}")
            for fname, fsize in copied_files:
                size_kb = fsize / 1024
                print(f"      - {fname} ({size_kb:.2f} KB)")

            summary.append({
                "handle": handle,
                "folder": str(target_dir),
                "files": copied_files,
                "status": "Success",
            })
        except Exception as e:
            print(f"   [ERROR] Gagal mengunduh {handle}: {e}")
            summary.append({
                "handle": handle,
                "folder": str(target_dir),
                "files": [],
                "status": f"Failed: {e}",
            })

    print("\n" + "=" * 60)
    print("RINGKASAN UNDUHAN DATASET:")
    print("=" * 60)
    for res in summary:
        print(f"Handle : {res['handle']}")
        print(f"Folder : {res['folder']}")
        print(f"Status : {res['status']}")
        print(f"File   : {[f[0] for f in res['files']]}")
        print("-" * 60)

if __name__ == "__main__":
    main()
