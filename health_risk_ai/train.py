"""Train one model per disease, compare algorithms, save best + metrics."""
import json, joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, recall_score, precision_score, brier_score_loss
from config import DISEASES, FEATURE_NAMES
from data_gen import generate

def candidates():
    return {
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
        "Random Forest": RandomForestClassifier(n_estimators=250, min_samples_leaf=10, random_state=0, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.08, random_state=0),
    }

def main():
    df = generate()
    df.to_csv("models/synthetic_cohort.csv", index=False)
    X = df[FEATURE_NAMES]
    ref = X.median().to_dict()
    bundle, report = {"reference": ref, "models": {}}, {}
    for key, (name, *_ ) in DISEASES.items():
        y = df[key]
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1)
        scores = {}
        best, best_auc = None, -1
        for mname, model in candidates().items():
            model.fit(Xtr, ytr)
            p = model.predict_proba(Xte)[:, 1]
            auc = roc_auc_score(yte, p)
            scores[mname] = round(auc, 3)
            if auc > best_auc:
                best, best_auc, best_name, best_p = model, auc, mname, p
        thr = float(np.clip(y.mean(), 0.05, 0.5))
        pred = (best_p >= thr).astype(int)
        report[key] = {"disease": name, "best_model": best_name, "auc": round(best_auc, 3),
                       "accuracy": round(accuracy_score(yte, pred), 3),
                       "recall": round(recall_score(yte, pred), 3),
                       "precision": round(precision_score(yte, pred), 3),
                       "brier": round(brier_score_loss(yte, best_p), 3),
                       "all_auc": scores, "prevalence": round(float(y.mean()), 3)}
        bundle["models"][key] = best
        print(f"{name:24s} best={best_name:20s} AUC={best_auc:.3f}  all={scores}")
    joblib.dump(bundle, "models/bundle.joblib")
    json.dump(report, open("models/metrics.json", "w"), indent=2)

if __name__ == "__main__":
    main()
