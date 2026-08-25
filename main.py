from pathlib import Path
from PIL import Image


def jpgs_to_pdf(input_dir: str, output_pdf: str):
    input_dir = Path(input_dir)

    jpgs = sorted(list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")))

    if not jpgs:
        raise FileNotFoundError(f"No .jpg/.jpeg files found in {input_dir}")

    images = []
    for p in jpgs:
        img = Image.open(p).convert("RGB")  # PDF needs RGB (no alpha)
        images.append(img)

    first, rest = images[0], images[1:]
    first.save(output_pdf, save_all=True, append_images=rest)

    print(f"Saved {len(images)} images -> {output_pdf}")


if __name__ == "__main__":
    jpgs_to_pdf("./1937_MoodysManual", "output.pdf")
