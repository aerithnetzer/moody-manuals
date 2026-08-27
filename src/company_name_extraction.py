# This file extracts company names from the pages

from itertools import batched
import os
from pathlib import Path
from lift import extract_images
from lift.model import InferenceManager
from PIL import Image

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.json"
def main():
    
    model = InferenceManager(method="hf")


    for batch in batched(os.scandir(DATA_DIR / "raw"), n=8):
        results = extract_images(images=[Image.open(p) for p in batch], schema=str(SCHEMA_PATH), model=model)
        print(results)


if __name__ == "__main__":
    main()
