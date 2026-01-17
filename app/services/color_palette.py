from PIL import Image
import numpy as np
import os
from sklearn.cluster import KMeans

def extract_color_palette(
    image_url: str,
    num_colors: int = 6,
    resize: int = 150
):
    image_path = download_image(image_url)

    image = Image.open(image_path).convert("RGB")

    # Resize for speed
    image.thumbnail((resize, resize))

    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)

    kmeans = KMeans(
        n_clusters=num_colors,
        n_init=10,
        random_state=42
    )

    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_

    palette = [
        rgb_to_hex(color.astype(int))
        for color in colors
    ]

    os.remove(image_path)

    return palette


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0]),
        int(rgb[1]),
        int(rgb[2])
    )
