import os
import json
import fitz  # PyMuPDF

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = None

    font_stats = {}  # size -> count

    for page in doc:
        for span in page.get_text("dict")["blocks"]:
            if "lines" not in span:
                continue
            for line in span["lines"]:
                for run in line["spans"]:
                    size = round(run["size"], 1)
                    font_stats[size] = font_stats.get(size, 0) + 1

    # Sort sizes by frequency (most common first)
    sorted_sizes = sorted(font_stats.items(), key=lambda x: (-x[1], -x[0]))
    if not sorted_sizes:
        return {"title": "Untitled", "outline": []}

    most_common_size = sorted_sizes[0][0]
    h1_threshold = most_common_size + 1.5
    h2_threshold = most_common_size + 0.5
    h3_threshold = most_common_size - 0.5

    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not text:
                    continue
                size = line["spans"][0]["size"]
                flags = line["spans"][0]["flags"]
                is_bold = flags & 2 != 0

                if size >= h1_threshold and is_bold:
                    if not title:
                        title = text
                    outline.append({"level": "H1", "text": text, "page": page_num})
                elif size >= h2_threshold:
                    outline.append({"level": "H2", "text": text, "page": page_num})
                elif size >= h3_threshold:
                    outline.append({"level": "H3", "text": text, "page": page_num})

    return {
        "title": title or "Untitled Document",
        "outline": outline
    }


def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            result = extract_headings(pdf_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
