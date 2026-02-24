from pdf2image import convert_from_path
from tqdm import tqdm

pages = convert_from_path("output.pdf", 500)

# Source - https://stackoverflow.com/a/48583124
# Posted by Keval Dave, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-24, License - CC BY-SA 4.0

for count, page in tqdm(enumerate(pages), total=len(pages)):
    page.save(f"images/out{count:010d}.jpg", "JPEG")
