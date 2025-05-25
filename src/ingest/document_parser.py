# Code to parse PDFs and emails into JSONL
import os
import fitz  # PyMuPDF
import json
from email import policy
from email.parser import BytesParser

# Paths
input_dir = "data/unstructured"
output_file = "data/unstructured/parsed.jsonl"
documents = []

# --- Parse PDFs ---
for file in os.listdir(input_dir):
    if file.lower().endswith(".pdf"):
        with fitz.open(os.path.join(input_dir, file)) as doc:
            text = "".join([page.get_text() for page in doc])
        documents.append({
            "source": file,
            "type": "pdf",
            "content": text.strip()
        })

# --- Parse Emails (.eml) ---
for file in os.listdir(input_dir):
    if file.lower().endswith(".eml"):
        with open(os.path.join(input_dir, file), "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            subject = msg["subject"]
            body = msg.get_body(preferencelist=('plain')).get_content()
        documents.append({
            "source": file,
            "type": "email",
            "subject": subject,
            "content": body.strip()
        })

# --- Save Output as JSONL ---
with open(output_file, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(json.dumps(doc) + "\n")

print(f"✅ Parsed {len(documents)} documents into {output_file}")
