"""Central configuration: features, diseases, thresholds.
Add a new disease by adding an entry to DISEASES and a label rule in data_gen.py."""

# name: (label, unit, default/median, min, max, modifiable)
FEATURES = {
    "age":          ("Age", "years", 45, 18, 90, False),
    "sex":          ("Sex (1 = male, 0 = female)", "", 0, 0, 1, False),
    "bmi":          ("BMI", "kg/m²", 26.5, 15, 50, True),
    "waist":        ("Waist circumference", "cm", 90, 55, 150, True),
    "sbp":          ("Systolic BP", "mmHg", 122, 85, 210, True),
    "dbp":          ("Diastolic BP", "mmHg", 80, 45, 130, True),
    "glucose":      ("Fasting glucose", "mg/dL", 98, 60, 400, True),
    "hba1c":        ("HbA1c", "%", 5.5, 4, 14, True),
    "chol":         ("Total cholesterol", "mg/dL", 195, 100, 400, True),
    "hdl":          ("HDL cholesterol", "mg/dL", 50, 20, 110, True),
    "ldl":          ("LDL cholesterol", "mg/dL", 115, 40, 300, True),
    "tg":           ("Triglycerides", "mg/dL", 130, 40, 800, True),
    "creatinine":   ("Serum creatinine", "mg/dL", 0.9, 0.4, 5, False),
    "smoker":       ("Current smoker", "", 0, 0, 1, True),
    "alcohol":      ("Alcohol", "drinks/week", 2, 0, 40, True),
    "activity":     ("Physical activity", "days/week", 3, 0, 7, True),
    "sleep":        ("Sleep", "hours/night", 7, 3, 11, True),
    "diet":         ("Diet quality (1 poor – 10 excellent)", "", 6, 1, 10, True),
    "stress":       ("Stress level (1 low – 10 high)", "", 5, 1, 10, True),
    "fh_diabetes":  ("Family history: diabetes", "", 0, 0, 1, False),
    "fh_heart":     ("Family history: heart disease / stroke", "", 0, 0, 1, False),
    "fh_hyper":     ("Family history: hypertension", "", 0, 0, 1, False),
}
FEATURE_NAMES = list(FEATURES)

# key: (display name, target prevalence in synthetic cohort, moderate threshold, high threshold)
DISEASES = {
    "diabetes":     ("Type 2 Diabetes",        0.12, 0.15, 0.40),
    "heart":        ("Heart Disease",          0.10, 0.12, 0.35),
    "hypertension": ("Hypertension",           0.30, 0.35, 0.65),
    "stroke":       ("Stroke",                 0.04, 0.06, 0.20),
    "ckd":          ("Chronic Kidney Disease", 0.08, 0.10, 0.30),
    "fatty_liver":  ("Fatty Liver (NAFLD)",    0.20, 0.25, 0.55),
}

ADVICE = {
    "bmi": "Aim for gradual weight loss (0.5 kg/week) with a calorie-aware diet; even 5–7% loss lowers diabetes, BP and liver risk.",
    "waist": "Reduce central fat: combine strength training, brisk walking and cutting refined carbs and sugary drinks.",
    "sbp": "Cut salt below 5 g/day, increase potassium-rich foods (DASH-style diet) and have your BP re-checked by a clinician.",
    "dbp": "Cut salt, manage stress and have your BP re-checked on several days by a clinician.",
    "glucose": "Reduce refined sugar/white-carb intake, walk 10–15 min after meals, and ask a doctor about an HbA1c test.",
    "hba1c": "Discuss long-term glucose control with a doctor; diet quality and regular exercise help most.",
    "chol": "Reduce saturated/trans fats, add fibre (oats, legumes) and discuss a lipid profile review.",
    "hdl": "Raise HDL via aerobic exercise, quitting smoking and healthy fats (nuts, olive oil, fish).",
    "ldl": "Lower LDL with less saturated fat, more soluble fibre; ask a doctor whether treatment is indicated.",
    "tg": "Limit sugar, refined carbs and alcohol; eat more omega-3-rich fish.",
    "smoker": "Quitting smoking is the single biggest risk reducer for heart disease and stroke; seek cessation support.",
    "alcohol": "Reduce alcohol intake; avoid binge drinking and keep several alcohol-free days each week.",
    "activity": "Build up to 150 minutes/week of moderate exercise (e.g., 30 min brisk walking, 5 days/week).",
    "sleep": "Aim for 7–8 hours of regular sleep; consistent sleep timing supports BP and glucose control.",
    "diet": "Shift towards vegetables, fruit, whole grains, pulses and lean protein; reduce ultra-processed food.",
    "stress": "Add stress-reduction habits: breathing exercises, yoga, time outdoors, and talk to someone if stress is persistent.",
}
