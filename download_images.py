import urllib.request
import os

images = [
    "vc-standard.png",
    "vc-paths.png",
    "vc-link-libs.png",
    "vc-static.png",
    "vc-app.png"
]

base_url = "https://www.sfml-dev.org/tutorials/3.1/getting-started/"
out_dir = "d:/my-blog/static/images/sfml/getting-started/"
os.makedirs(out_dir, exist_ok=True)

for img in images:
    url = base_url + img
    out_path = os.path.join(out_dir, img)
    print(f"Downloading {url} to {out_path}")
    urllib.request.urlretrieve(url, out_path)
print("Done.")
