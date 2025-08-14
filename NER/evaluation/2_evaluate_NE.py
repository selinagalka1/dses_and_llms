"""
BIO NER evaluation script.

Input format:
- Paragraphs are enclosed in angle brackets: < ... >
- Persons are marked with square brackets: [Louis XIV]
- Locations are marked with curly braces: {Paris}

The script:
1) Reads gold and system-annotated files.
2) Converts bracket markup to BIO tags with consistent tokenization.
3) Checks token alignment (skips misaligned paragraphs).
4) Reports sequence-level metrics (seqeval) and token-level metrics (scikit-learn).
5) Appends results to a text file.
"""

import re
import unicodedata
from seqeval.metrics import classification_report
from sklearn.metrics import classification_report as sk_report


def normalize(text):
    """Normalize Unicode to NFKC, replace NBSP with space, remove zero-width spaces."""
    return (
        unicodedata.normalize("NFKC", text)
        .replace("\u00A0", " ")
        .replace("\u200b", "")
    )


def tokenize(text):
    """Tokenize into words and punctuation; punctuation is kept as separate tokens."""
    text = normalize(text)
    # \w+ = word chars (letters/digits/underscore), [^\w\s] = any non-word, non-space (i.e., punctuation)
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)


def extract_bio(paragraphs):
    """
    Convert a list of annotated paragraphs into BIO token/label sequences.

    Markup conventions:
      [ ... ]  -> PER  (B-PER, I-PER)
      { ... }  -> LOC  (B-LOC, I-LOC)
      plain    -> O

    Note: Assumes brackets are well-formed and non-nested.
    """
    bio_data = []

    for para in paragraphs:
        tokens = []
        labels = []
        i = 0

        while i < len(para):
            if para[i] == "[":  # Person entity
                end = para.find("]", i)
                entity = para[i + 1 : end]
                ent_tokens = tokenize(entity)
                tokens.extend(ent_tokens)
                labels.extend(["B-PER"] + ["I-PER"] * (len(ent_tokens) - 1))
                i = end + 1

            elif para[i] == "{":  # Location entity
                end = para.find("}", i)
                entity = para[i + 1 : end]
                ent_tokens = tokenize(entity)
                tokens.extend(ent_tokens)
                labels.extend(["B-LOC"] + ["I-LOC"] * (len(ent_tokens) - 1))
                i = end + 1

            else:
                # Consume plain text until the next entity marker or end of paragraph
                j = i
                while j < len(para) and para[j] not in "[{":
                    j += 1

                normal_text = para[i:j]
                norm_tokens = tokenize(normal_text)
                tokens.extend(norm_tokens)
                labels.extend(["O"] * len(norm_tokens))
                i = j

        bio_data.append((tokens, labels))

    return bio_data


def read_and_parse(file_path):
    """Read file, extract paragraphs inside <...>, and convert them to BIO sequences."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # DOTALL allows paragraphs to span multiple lines
    paragraphs = re.findall(r"<(.*?)>", text, re.DOTALL)
    return extract_bio(paragraphs)


# --- Load and process both files ---
human_bio = read_and_parse("output/txt/french_gold_normalized.txt")
gpt_bio = read_and_parse("output/txt/annotated_with_flair_split_normalized.txt")

# --- Collect labels for evaluation (only if tokens align) ---
y_true = []
y_pred = []

for i, ((toks_h, labs_h), (toks_g, labs_g)) in enumerate(zip(human_bio, gpt_bio), start=1):
    # Alignment check ensures a fair comparison; mismatched tokenization would invalidate scores
    if toks_h != toks_g:
        print(f"\nToken mismatch in paragraph {i}!")
        # Print first differing token to help diagnose tokenization drift
        for j, (th, tg) in enumerate(zip(toks_h, toks_g)):
            if th != tg:
                print(f"  Token {j}: Human={repr(th)} vs GPT={repr(tg)}")
                break  # remove break to list more differences
        continue

    y_true.append(labs_h)
    y_pred.append(labs_g)

# --- Evaluation using seqeval (sequence-aware entity metrics) ---
print("\nSEQEVAL REPORT:")
try:
    print(classification_report(y_true, y_pred))
except ValueError as e:
    # Seqeval may raise if sequences are empty or malformed
    print(f"Seqeval error: {e}")

# --- Evaluation using scikit-learn (token-level label metrics) ---
# Flatten to per-token lists expected by sklearn
flat_true = [label for seq in y_true for label in seq]
flat_pred = [label for seq in y_pred for label in seq]

print("\nSKLEARN REPORT:")
print(sk_report(flat_true, flat_pred))

# --- Persist results to file ---
output_report_file = "results/evaluation_results_flair.txt"
experiment_name = "Flair annotated with NE vs Human Gold (normalized paragraphs)"

with open(output_report_file, "a", encoding="utf-8") as f:
    f.write(f"\n=== Experiment: {experiment_name} ===\n")
    f.write("SEQEVAL REPORT:\n")
    try:
        f.write(classification_report(y_true, y_pred))
    except ValueError as e:
        f.write(f"Seqeval error: {e}\n")
    f.write("\nSKLEARN REPORT:\n")
    f.write(sk_report(flat_true, flat_pred))
    f.write("\n\n")
