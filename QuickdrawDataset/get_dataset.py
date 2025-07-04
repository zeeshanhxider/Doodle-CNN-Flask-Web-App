import os
import urllib.request

labels = [
    "apple",
    "butterfly",
    "camera",
    "cake",
    "clock",
    "cup",
    "dolphin",
    "elephant",
    "fish",
    "flower",
    "guitar",
    "ice cream",
    "key",
    "mountain",
    "moon",
    "octopus",
    "pizza",
    "scissors",
    "star",
    "sun",
    "train",
    "umbrella",
    "bus"
]

# Remove duplicates
labels = list(dict.fromkeys(labels))

os.makedirs("quickdraw_npy", exist_ok=True)
base_url = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/"

for cls in labels:
    filename = cls + ".npy"
    save_path = os.path.join("quickdraw_npy", filename)

    # Skip if already downloaded
    if os.path.exists(save_path):
        print(f"Skipping {cls} (already downloaded).")
        continue

    cls_url = base_url + cls.replace(" ", "%20") + ".npy"
    
    try:
        print(f"Downloading {cls}...")
        urllib.request.urlretrieve(cls_url, save_path)
    except Exception as e:
        print(f"Failed to download {cls}: {e}")

print("Download complete.")