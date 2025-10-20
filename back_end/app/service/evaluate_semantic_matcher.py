import json

def compute_metrics(true_positives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1

def evaluate_semantic_matcher(result_path="prompt_data.json", ground_truth_path="ground_truth.json", threshold=0.75):
    # Charger les données
    with open(result_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(ground_truth_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    # Créer un dictionnaire rapide pour accéder aux sections par URL et texte
    gt_dict = {}
    for page in ground_truth:
        gt_dict[page["url"]] = {}
        for section in page["sections"]:
            gt_dict[page["url"]][section["contenu"]] = [
                (m["numero"], m["titre_chapitre"]) for m in section.get("expected_matches", [])
            ]

    tp = 0
    fp = 0
    fn = 0

    # Parcours des résultats
    for page in results:
        url = page["url"]
        for section in page["sections"]:
            text = section["contenu"]
            predicted = [
                (m["numero"], m["titre_chapitre"])
                for m in section.get("matches", [])
                if m["score"] >= threshold
            ]
            expected = gt_dict.get(url, {}).get(text, [])

            # Comptage TP, FP, FN
            for match in predicted:
                if match in expected:
                    tp += 1
                else:
                    fp += 1
            for match in expected:
                if match not in predicted:
                    fn += 1

    precision, recall, f1 = compute_metrics(tp, fp, fn)

    report = {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }

    print("✅ Évaluation terminée")
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    evaluate_semantic_matcher("prompt_data.json", "ground_truth.json", threshold=0.75)
