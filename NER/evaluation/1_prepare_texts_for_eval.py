"""
TEI/XML -> Proprietary Text -> Normalized Text

This script:
1) Applies an XSLT to a TEI/XML file to produce plain text with custom markup:
   - < ... >  : paragraph boundaries
   - [ ... ]  : persons
   - { ... }  : places
2) Normalizes whitespace in the produced text (single-line, single-spaced).
"""

from lxml import etree
import re

# --- Configuration (CHANGE PATHS HERE) ---
xml_file = "input/flair/annotated_with_flair_split.xml"   # The TEI/XML to transform
xslt_file = "xslt/tei2text_flair.xsl"                     # XSLT that produces proprietary text. Use tei2text.xsl for the Output from LLMs.
output_text = "output/txt/annotated_with_flair_split.txt" # Output of the XSLT step
output_norm = "output/txt/annotated_with_flair_split_normalized.txt"  # Normalized output


# --- XSLT Transformation ---
# Load and parse the XML and XSLT files
xml_tree = etree.parse(xml_file)
xslt_tree = etree.parse(xslt_file)

# Compile the XSLT
transform = etree.XSLT(xslt_tree)

# Apply the transformation to TEI/XML -> custom text
result_tree = transform(xml_tree)

# Save the transformed text to disk
with open(output_text, "w", encoding="utf-8") as f:
    # lxml returns a special _XSLTResultTree; str(...) yields the text output
    f.write(str(result_tree))

print(f"Transformation completed. Output saved to {output_text}")


# --- Whitespace Normalization ---

def normalize_paragraph(text: str) -> str:
    """Collapse newlines to spaces, squeeze repeated whitespace, and strip ends."""
    text = text.replace('\n', ' ')           # join lines
    text = re.sub(r'\s+', ' ', text)         # collapse multiple spaces/tabs
    return text.strip()                       # trim leading/trailing spaces


def load_and_normalize_file(file_path: str) -> str:
    """Read a UTF-8 text file and return its normalized content."""
    with open(file_path, encoding='utf-8') as f:
        raw_text = f.read()
    return normalize_paragraph(raw_text)


# Normalize the freshly generated text file
normalized_text = load_and_normalize_file(output_text)

# Show a preview in the console (optional; remove if the text is very large)
print(normalized_text)

# Save normalized text to disk
with open(output_norm, "w", encoding="utf-8") as f:
    f.write(normalized_text)

print(f"Normalized text saved to: {output_norm}")
