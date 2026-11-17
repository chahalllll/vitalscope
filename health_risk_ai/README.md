# VitalScope: AI-Based Personalized Health Risk Assessment System

A web application that estimates an individual's risk for six chronic conditions
(type 2 diabetes, heart disease, hypertension, stroke, chronic kidney disease, fatty liver),
explains the factors behind each estimate and suggests prioritised lifestyle actions.

## Run it
```bash
pip install -r requirements.txt
python train.py        # trains the models (auto-runs on first launch if skipped)
python app.py          # open http://127.0.0.1:5000
```

## Architecture
```
Browser form ──► Flask API (/api/assess) ──► engine.py
                                              ├─ validation + median imputation of missing labs
                                              ├─ one ML model per disease  (models/bundle.joblib)
                                              ├─ explanation: counterfactual feature contribution
                                              └─ rule-based recommendation + red-flag alerts
train.py  ← data_gen.py (synthetic cohort)  ← config.py (features, diseases, thresholds, advice)
```

## Key design choices (useful for your viva)
- **Multi-disease, modular:** diseases live in `config.DISEASES`. "All diseases" is not achievable in one
  project; this design lets you add one by adding a config entry, a label rule (or a real dataset column) and retraining.
- **Model selection per disease:** Logistic Regression, Random Forest and Gradient Boosting are trained and
  the best AUC on a stratified hold-out set is kept. Metrics: AUC, accuracy, recall, precision, Brier score
  (`models/metrics.json`).
- **Explainability:** for each disease, every input is reset to the population median and the drop in predicted
  risk is reported (positive = raises your risk). This is model-agnostic; you can swap in SHAP.
- **Personalised advice:** only *modifiable* factors that actually contribute to your risk generate advice.
- **Missing data:** optional lab values are imputed with medians and the user is told which ones.
- **Safety:** blood-pressure/glucose red-flag messages and a medical disclaimer.

## Honest limitations (state these in your report)
1. **Training data is simulated** from published risk relationships (`data_gen.py`). Logistic Regression wins
   because the simulated labels are logistic. On real data, tree ensembles often compete or win.
   Reported AUCs describe the pipeline, not clinical performance.
2. Not a diagnostic device and not clinically validated.
3. Cross-sectional features only; no time-series or imaging.

## Recommended real datasets for the final report
| Disease | Dataset |
|---|---|
| Diabetes | Pima Indians Diabetes (UCI/Kaggle), NHANES |
| Heart disease | UCI Cleveland Heart Disease, Framingham Heart Study |
| Hypertension / CKD | NHANES, UCI Chronic Kidney Disease |
| Liver | Indian Liver Patient Dataset (ILPD) |

To use real data: build a DataFrame with the columns in `config.FEATURES` (leave unavailable ones to median
imputation) plus one binary column per disease, replace `generate()` in `train.py`, and retrain.

## Suggested future work
Calibration curves, SHAP explanations, user accounts with risk history, wearable-data input (Fit/Apple Health),
fairness analysis across sex/age groups, multilingual UI, Docker deployment.
