import re
import unicodedata
from seqeval.metrics import classification_report
from sklearn.metrics import classification_report as sk_report

def normalize(text):
    """Normalize text for consistent tokenization."""
    return unicodedata.normalize("NFKC", text).replace('\u00A0', ' ').replace('\u200b', '')

def tokenize(text):
    """Tokenize text into words and punctuation."""
    text = normalize(text)
    return re.findall(r'\w+|[^\w\s]', text, re.UNICODE)

def extract_bio(paragraphs):
    bio_data = []
    for para in paragraphs:
        tokens = []
        labels = []
        i = 0
        while i < len(para):
            if para[i] == '[':
                end = para.find(']', i)
                entity = para[i+1:end]
                ent_tokens = tokenize(entity)
                tokens.extend(ent_tokens)
                labels.extend(['B-PER'] + ['I-PER'] * (len(ent_tokens) - 1))
                i = end + 1
            elif para[i] == '{':
                end = para.find('}', i)
                entity = para[i+1:end]
                ent_tokens = tokenize(entity)
                tokens.extend(ent_tokens)
                labels.extend(['B-LOC'] + ['I-LOC'] * (len(ent_tokens) - 1))
                i = end + 1
            else:
                j = i
                while j < len(para) and para[j] not in '[{':
                    j += 1
                normal_text = para[i:j]
                norm_tokens = tokenize(normal_text)
                tokens.extend(norm_tokens)
                labels.extend(['O'] * len(norm_tokens))
                i = j
        bio_data.append((tokens, labels))
    return bio_data

def read_and_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = re.findall(r'<(.*?)>', text, re.DOTALL)
    return extract_bio(paragraphs)

# Load and process both files
human_bio = read_and_parse('output/txt/french_gold_normalized.txt')
gpt_bio = read_and_parse('output/txt/annotated_with_flair_split_normalized.txt')

# Evaluation
y_true = []
y_pred = []

for i, ((toks_h, labs_h), (toks_g, labs_g)) in enumerate(zip(human_bio, gpt_bio)):
    if toks_h != toks_g:
        print(f"\nToken mismatch in paragraph {i + 1}!")
        for j, (th, tg) in enumerate(zip(toks_h, toks_g)):
            if th != tg:
                print(f"  Token {j}: Human={repr(th)} vs GPT={repr(tg)}")
                break  # or remove this to see more
        continue

    y_true.append(labs_h)
    y_pred.append(labs_g)

# Evaluation using seqeval
print("\nSEQEVAL REPORT:")
try:
    print(classification_report(y_true, y_pred))
except ValueError as e:
    print(f"Seqeval error: {e}")

# Flatten for sklearn-style report
flat_true = [label for sublist in y_true for label in sublist]
flat_pred = [label for sublist in y_pred for label in sublist]

print("\nSKLEARN REPORT:")
print(sk_report(flat_true, flat_pred))

# Save results
output_report_file = "results/evaluation_results_flair.txt"
experiment_name = "Flair annotated with NE vs Human Gold (normalized paragraphs)"

with open(output_report_file, 'a', encoding='utf-8') as f:
    f.write(f"\n=== Experiment: {experiment_name} ===\n")
    f.write("SEQEVAL REPORT:\n")
    try:
        f.write(classification_report(y_true, y_pred))
    except ValueError as e:
        f.write(f"Seqeval error: {e}\n")
    f.write("\nSKLEARN REPORT:\n")
    f.write(sk_report(flat_true, flat_pred))
    f.write("\n\n")
