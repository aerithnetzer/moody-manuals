# This file extracts company names from the pages

import json
import os
from pathlib import Path
from lift import extract_images
from lift.model import InferenceManager
from PIL import Image
import logging
from dataclasses import asdict
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
SCHEMA_PATH = BASE_DIR / "schema.json"
LOG_DIR = BASE_DIR / "logs"
LOG_PATH = LOG_DIR / f"{os.getenv('SLURM_JOB_ID', 'local')}.log"

logger = logging.getLogger(__name__)

def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    now = datetime.now()
    date = now.strftime("%d_%m_%Y")
    time = now.strftime("%H_%M_%S")
    logger.info("Run started on: %s, at time: %s", date, time)
    EXECUTION_MANIFEST_DIR = DATA_DIR / date / time

    absolute_paths = sorted(
        str(item.resolve())
        for item in RAW_DATA_DIR.iterdir()
        if item.is_file() and item.suffix.lower() == ".png"
    )
    os.makedirs(EXECUTION_MANIFEST_DIR, exist_ok=True)

    with open(EXECUTION_MANIFEST_DIR / "run_manifest.txt", "w") as f:
        _ = f.write(("#" * 20 + "\n" ))
        _ = f.write("EXTRACTION SCHEMA\n")
        _ = f.write(("#" * 20 + "\n" ))
        _ = f.write(json.dumps(json.loads(SCHEMA_PATH.read_text()), indent=4) + "\n")
        _ = f.write(("#" * 20 + "\n" ))
        _ = f.write("END OF SCHEMA\n")
        _ = f.write(("#" * 20 + "\n\n\n" ))
        _ = f.write(("#" * 20 + "\n" ))
        _ = f.write("RESOURCES PROCESSED IN THIS RUN\n")
        _ = f.write(("#" * 20 + "\n" ))
        f.writelines(f"{p}\n" for p in absolute_paths)
        _ = f.write(("#" * 20 + "\n" ))
        _ = f.write("END OF RESOURCES PROCESSED IN THIS RUN\n")
        _ = f.write(("#" * 20 + "\n" ))

    logger.info(f"Running company extraction on: {RAW_DATA_DIR}")
    logger.info(f"Using schema: {SCHEMA_PATH}")
    logger.info(f"Logging to: {LOG_PATH}")

    model = InferenceManager(method="hf")
    os.makedirs(EXECUTION_MANIFEST_DIR / "extracted_data", exist_ok=True)
    for i, p in enumerate(absolute_paths):
        results = extract_images(images=[Image.open(p)], schema=str(SCHEMA_PATH), model=model)
        result_path = EXECUTION_MANIFEST_DIR / "extracted_data" / f"{Path(p).stem}.json"
        logger.info(f"Saving to {result_path}")
        with open(result_path, "w") as f:
            _ = f.write(json.dumps(asdict(results), indent=4))

        logger.info(f"Completed iteration {i}")


if __name__ == "__main__":
    main()
