"""Inference + explanation + recommendation engine."""
import os, json, joblib
import pandas as pd
from config import FEATURES, FEATURE_NAMES, DISEASES, ADVICE

BASE = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(BASE, "models", "bundle.joblib")):
    import train; os.chdir(BASE); train.main()

_bundle = joblib.load(os.path.join(BASE, "models", "bundle.joblib"))
MODELS, REF = _bundle["models"], _bundle["reference"]
METRICS = json.load(open(os.path.join(BASE, "models", "metrics.json")))

def level(key, p):
    _, _, mod, high = DISEASES[key]
    return "High" if p >= high else "Moderate" if p >= mod else "Low"

def validate(raw):
    """Clean user input. Blank optional values are imputed with the population median."""
    row, imputed = {}, []
    for f in FEATURE_NAMES:
        label, unit, default, lo, hi, _ = FEATURES[f]
        v = raw.get(f)
        if v in (None, ""):
            row[f] = default; imputed.append(label); continue
        try:
            v = float(v)
        except ValueError:
            raise ValueError(f"{label} must be a number")
        if not lo <= v <= hi:
            raise ValueError(f"{label} must be between {lo} and {hi} {unit}".strip())
        row[f] = v
    if row["bmi"] == FEATURES["bmi"][2] and raw.get("height") and raw.get("weight"):
        h = float(raw["height"]) / 100
        row["bmi"] = round(float(raw["weight"]) / (h * h), 1)
        imputed = [i for i in imputed if i != FEATURES["bmi"][0]]
    return row, imputed

def assess(raw):
    row, imputed = validate(raw)
    x = pd.DataFrame([row])[FEATURE_NAMES]
    results, advice_pool = [], {}
    for key, model in MODELS.items():
        p = float(model.predict_proba(x)[0, 1])
        # Local explanation: change in risk when one feature is reset to the population median
        contribs = []
        for f in FEATURE_NAMES:
            if f in imputed_names(imputed):
                continue
            xr = x.copy(); xr[f] = REF[f]
            delta = p - float(model.predict_proba(xr)[0, 1])
            contribs.append((f, delta))
        contribs.sort(key=lambda t: -abs(t[1]))
        top = [{"feature": FEATURES[f][0], "key": f, "effect": round(d * 100, 1),
                "value": row[f], "unit": FEATURES[f][1]} for f, d in contribs[:4] if abs(d) >= 0.005]
        for f, d in contribs:
            if d > 0.01 and FEATURES[f][5] and f in ADVICE:
                advice_pool[f] = advice_pool.get(f, 0) + d
        results.append({"key": key, "disease": DISEASES[key][0], "risk": round(p * 100, 1),
                        "baseline": round(DISEASES[key][1] * 100, 1), "level": level(key, p),
                        "drivers": top, "auc": METRICS[key]["auc"]})
    results.sort(key=lambda r: -r["risk"] / max(r["baseline"], 1))
    recs = [{"key": f, "text": ADVICE[f], "label": FEATURES[f][0]}
            for f, _ in sorted(advice_pool.items(), key=lambda t: -t[1])[:5]]
    urgent = []
    if row["sbp"] >= 180 or row["dbp"] >= 120:
        urgent.append("Your blood pressure reading is in a severely elevated range. Seek medical advice promptly; if you have chest pain, breathlessness, weakness or vision/speech changes, get emergency care.")
    if row["glucose"] >= 300:
        urgent.append("Your fasting glucose is very high. Please see a doctor soon.")
    return {"results": results, "recommendations": recs, "urgent": urgent,
            "bmi": row["bmi"], "imputed": imputed}

def imputed_names(imputed):
    inv = {v[0]: k for k, v in FEATURES.items()}
    return {inv[i] for i in imputed}
