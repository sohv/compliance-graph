from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os

def get_full_rules():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_json = os.path.join(script_dir, "..", "data", "extracted_rules.json")
    
    if not os.path.exists(output_json):
        print(f"Extracted rules file not found at: {output_json}")
        print("Please run extract_rules.py first to generate the extracted_rules.json file.")
        return []
    
    with open(output_json, 'r', encoding='utf-8') as f:
        all_extracted_rules = json.load(f)
    
    return [rule["FullRule"] for rule in all_extracted_rules if "FullRule" in rule]

def get_annotated_rules():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_txt = os.path.join(script_dir, "..", "data", "output.txt")
    
    if not os.path.exists(rules_txt):
        print(f"Output file not found at: {rules_txt}")
        print("Please ensure the output.txt file exists in the data directory.")
        return []
    
    with open(rules_txt, 'r', encoding='utf-8') as f:
        rules = [line.strip() for line in f if line.strip()]
    
    return rules

full_rules = get_full_rules()
rule_ls = get_annotated_rules()

print(f"Number of extracted rules: {len(full_rules)}")
print(f"Number of rules in output.txt: {len(rule_ls)}")

model = SentenceTransformer('all-MiniLM-L6-v2')

full_rule_embeddings = model.encode(full_rules)
rule_ls_embeddings = model.encode(rule_ls)

score_ls = []
score_ls_no_miss = []
partial = 0
similars = 0
miss = 0

for j, rule_embedding in enumerate(rule_ls_embeddings):
    similarities = cosine_similarity([rule_embedding], full_rule_embeddings)
    closest_match_index = np.argmax(similarities)
    highest_similarity = similarities[0][closest_match_index]

    if highest_similarity >= 0.80:
        score_ls.append(highest_similarity)
    elif 0.60 <= highest_similarity < 0.80:
        partial += 1
        score_ls.append(highest_similarity)
    elif 0.40 <= highest_similarity < 0.60:
        similars += 1
        score_ls.append(highest_similarity)
    else:
        miss += 1
        score_ls.append(0)

    score_ls_no_miss.append(highest_similarity)

total_rules = len(rule_ls)
fully_recovered = total_rules - partial - similars - miss
fully_recovered_percentage = (fully_recovered / total_rules) * 100 if total_rules > 0 else 0
partial_percentage = (partial / total_rules) * 100 if total_rules > 0 else 0
similar_percentage = (similars / total_rules) * 100 if total_rules > 0 else 0
missed_percentage = (miss / total_rules) * 100 if total_rules > 0 else 0
avg_similarity = sum(score_ls_no_miss) / total_rules if total_rules > 0 else 0
avg_corrected_similarity = sum(score_ls) / total_rules if total_rules > 0 else 0

print(f"Total Rules in output.txt: {total_rules}")
print(f"Fully Recovered Rules: {fully_recovered} ({fully_recovered_percentage:.2f}%)")
print(f"Partially Recovered Rules: {partial} ({partial_percentage:.2f}%)")
print(f"Similar Rules: {similars} ({similar_percentage:.2f}%)")
print(f"Missed Rules: {miss} ({missed_percentage:.2f}%)")
print(f"Average Similarity: {avg_similarity:.4f}")
print(f"Average Corrected Similarity: {avg_corrected_similarity:.4f}")

if len(full_rules) > 0:
    relative_excess = abs(abs(total_rules - miss) - len(full_rules)) / len(full_rules)
    print(f"Relative Excess Extracted Rules: {relative_excess:.4f}")
else:
    print("Relative Excess Extracted Rules: N/A (no extracted rules)")