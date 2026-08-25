import json

with open("./results.json", "r") as f:
    data = json.load(f)

for k in sorted(data.keys()):
    pages = data[k]
    for page in pages:
        text_lines = page.get("text_lines", "")
        texts = []
        for line in text_lines:
            texts.append(line.get("text", ""))

        with open(k, "w") as g:
            g.writelines(texts)
