from lxml import etree

# This transforms the TEI/XML to text with proprietary encoding for paragaphs (< text >), persons ([person]) and places ({place}) for further processing and normalizes whitespace

# Load the XML and XSLT files (this must be done for the ground truth xml and the annotated flair xml)
xml_file = "input/flair/annotated_with_flair_split.xml"  # CHANGE HERE - the TEI/XML File that shall be transformed to text, z.B. "input/gpt/prompt3_edited_NE_edited_NE_edited_NE.xml""
xslt_file = "xslt/tei2text_flair.xsl"  # XSLT for transforming TEI/XML to text - tei2text.xsl is for transforming the ground truth and the LLMs Output, tei2text_flair.xsl for the flair output.

# Parse the XML and XSLT
xml_tree = etree.parse(xml_file)
xslt_tree = etree.parse(xslt_file)

# Create an XSLT transformer
transform = etree.XSLT(xslt_tree)

# Apply the transformation
result_tree = transform(xml_tree)

# Save the transformed XML to a new file
output_file = "output/txt/annotated_with_flair_split.txt"  # CHANGE HERE - Replace with your desired output file path - same name as TEI/XML-Input-File, z.B. "output/gpt_prompt3_edited_NE_edited_NE_edited_NE.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(result_tree))  # Use str to get the text output

print(f"Transformation completed. Output saved to {output_file}")


# NOW: normalize it

import re

def normalize_paragraph(text: str) -> str:
    # Collapse line breaks into spaces
    text = text.replace('\n', ' ')
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing space
    return text.strip()

def load_and_normalize_file(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as f:
        raw_text = f.read()
    return normalize_paragraph(raw_text)

# Example Usage 
input_file = "output/txt/annotated_with_flair_split.txt" # CHANGE HERE - use the txt file from above
output_file = "output/txt/annotated_with_flair_split_normalized.txt" # CHANGE HERE - same name as the initial XML/FILE + "_normalized.txt"

normalized_text = load_and_normalize_file(input_file)

# Print result
print(normalized_text)

# Save to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(normalized_text)

print(f"Normalized text saved to: {output_file}")
