"""
setup_credentials.py
Auto-find and copy credentials.json from Downloads to auth/ folder.
Run: python auth/setup_credentials.py
"""
import os
import shutil
import glob
import sys

AUTH_DIR = os.path.join(os.path.dirname(__file__))
DEST = os.path.join(AUTH_DIR, "credentials.json")


def find_credentials():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    # Search for client_secret JSON files
    patterns = [
        os.path.join(downloads, "client_secret_*.json"),
        os.path.join(downloads, "credentials*.json"),
    ]
    found = []
    for pattern in patterns:
        found.extend(glob.glob(pattern))
    return found


def main():
    if os.path.exists(DEST):
        print(f"[OK] credentials.json already exists at {DEST}")
        print("     Delete it first if you want to replace it.")
        return

    files = find_credentials()
    if not files:
        print("[ERROR] No credentials file found in Downloads folder.")
        print("  Please download from GCP Console:")
        print("  https://console.cloud.google.com/apis/credentials?project=maplab-pipeline")
        print("  -> Click on 'maplab-pipeline-desktop' row download icon")
        sys.exit(1)

    if len(files) == 1:
        src = files[0]
    else:
        print("Multiple files found:")
        for i, f in enumerate(files):
            print(f"  [{i}] {os.path.basename(f)}")
        idx = int(input("Enter number to use: "))
        src = files[idx]

    shutil.copy2(src, DEST)
    print(f"[OK] Copied: {os.path.basename(src)}")
    print(f"     -> {DEST}")
    print()
    print("Next step:")
    print("  python -m src.auth.google_auth --account owner")


if __name__ == "__main__":
    main()
