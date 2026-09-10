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
LOG_PATH = BASE_DIR / "logs" / f"{os.getenv("SLURM_JOB_ID")}.log"

logger = logging.getLogger(__name__)

def main():
    Path(LOG_PATH).touch()
    logging.basicConfig(filename=LOG_PATH)

    now = datetime.now()
    date = now.strftime("%d_%m_%Y")
    time = now.strftime("%H_%M_%S")
    logger.info("Run started on: ", date, ",at time: ", time) 
    EXECUTION_MANIFEST_DIR = DATA_DIR / date / time

    absolute_paths = [str(item.resolve()) for item in RAW_DATA_DIR.iterdir()]
    try:
        os.makedirs(EXECUTION_MANIFEST_DIR)
    except Exception as e:
        raise e

    try:
        with open(EXECUTION_MANIFEST_DIR / "run_manifest.txt", "w") as f:
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.write("EXTRACTION SCHEMA\n")
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.writelines(json.dumps(json.load(open(SCHEMA_PATH, "r")), indent = 4))
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.write("END OF SCHEMA\n")
            _ = f.write(("#" * 20 + "\n\n\n" ))
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.write("RESOURCES PROCESSED IN THIS RUN")
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.writelines([str(p) for p in absolute_paths])
            _ = f.write(("#" * 20 + "\n" ))
            _ = f.write("END OF RESOURCES PROCESSED IN THIS RUN")
            _ = f.write(("#" * 20 + "\n" ))

    except Exception as e:
        raise e

    logger.info(f"Running compnay extraction on: {DATA_DIR}")
    logger.info(f"Using schema: {SCHEMA_PATH}")
    logger.info(f"Logging to: {LOG_PATH}")

    model = InferenceManager(method="hf")
    i = 0
    os.makedirs(EXECUTION_MANIFEST_DIR / "extracted_data", exist_ok=True)
    for p in absolute_paths:
        results = extract_images(images=[Image.open(p)], schema=str(SCHEMA_PATH), model=model)
        result_path = EXECUTION_MANIFEST_DIR / "extracted_data" / f"{p.split("/")[0].strip(".png")}.json"
        print(f"Saving to {result_path}")
        with open(result_path, "w") as f:
            f.writelines(json.dumps(asdict(results), indent=4))

        logger.info(f"Completed iteration {i}")
        i += 1


if __name__ == "__main__":
    main()
