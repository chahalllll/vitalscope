"""Synthetic cohort generator.

IMPORTANT: this data is SIMULATED from published epidemiological relationships
(age, BMI, BP, glucose, lipids, smoking, etc.). It lets the full pipeline run
offline. For your final report, replace it with real datasets (see README)."""
import numpy as np
import pandas as pd
from config import DISEASES

def _sigmoid(z):
    return 1 / (1 + np.exp(-z))

def _calibrate(logit, prevalence):
    """Shift the intercept so the cohort hits the target prevalence."""
    lo, hi = -30, 30
    for _ in range(60):
        mid = (lo + hi) / 2
        if _sigmoid(logit + mid).mean() > prevalence:
            hi = mid
        else:
            lo = mid
    return logit + (lo + hi) / 2

def generate(n=8000, seed=42):
    r = np.random.default_rng(seed)
    age = np.clip(r.normal(45, 15, n), 18, 90).round()
    sex = r.binomial(1, 0.5, n)
    activity = r.integers(0, 8, n)
    diet = np.clip(r.normal(6, 2, n), 1, 10).round()
    stress = np.clip(r.normal(5, 2.2, n), 1, 10).round()
    smoker = r.binomial(1, 0.12 + 0.15 * sex, n)
    alcohol = np.clip(r.exponential(3, n) + 4 * sex * r.binomial(1, .3, n), 0, 40).round()
    sleep = np.clip(r.normal(7, 1.2, n), 3, 11).round(1)
    fh_d, fh_h, fh_ht = r.binomial(1, .2, n), r.binomial(1, .2, n), r.binomial(1, .3, n)

    bmi = np.clip(r.normal(24.5 + 0.04 * (age - 45) - 0.15 * activity + 2, 4.5), 15, 50)
    waist = np.clip(2.0 * bmi + 24 + 6 * sex + r.normal(0, 5, n), 55, 150)
    sbp = np.clip(98 + 0.4 * age + 0.7 * (bmi - 22) + 3 * smoker + 0.15 * alcohol
                  + 0.8 * stress + 4 * fh_ht + r.normal(0, 10, n), 85, 210)
    dbp = np.clip(38 + 0.42 * sbp + 0.2 * (bmi - 22) + r.normal(0, 6, n), 45, 130)
    glucose = np.clip(78 + 0.15 * age + 0.9 * (bmi - 22) + 5 * fh_d - 1.0 * activity
                      - 0.8 * diet + r.normal(0, 9, n) + r.exponential(5, n)
                      + 60 * r.binomial(1, 0.04, n), 60, 400)
    hba1c = np.clip(3.9 + 0.0165 * glucose + r.normal(0, 0.25, n), 4, 14)
    chol = np.clip(150 + 0.45 * age + 1.3 * (bmi - 22) - 1.5 * diet + r.normal(0, 28, n), 100, 400)
    hdl = np.clip(56 - 8 * sex - 0.7 * (bmi - 22) + 1.4 * activity - 4 * smoker + r.normal(0, 7, n), 20, 110)
    tg = np.clip(np.exp(r.normal(4.65 + 0.025 * (bmi - 22) + 0.01 * alcohol, 0.4)), 40, 800)
    ldl = np.clip(chol - hdl - tg / 5, 40, 300)
    creat = np.clip(0.65 + 0.28 * sex + 0.003 * age + r.normal(0, 0.1, n)
                    + 0.01 * np.maximum(age - 60, 0) * r.binomial(1, .1, n) * 5, 0.4, 5)

    X = pd.DataFrame(dict(age=age, sex=sex, bmi=bmi.round(1), waist=waist.round(), sbp=sbp.round(),
                          dbp=dbp.round(), glucose=glucose.round(), hba1c=hba1c.round(1),
                          chol=chol.round(), hdl=hdl.round(), ldl=ldl.round(), tg=tg.round(),
                          creatinine=creat.round(2), smoker=smoker, alcohol=alcohol,
                          activity=activity, sleep=sleep, diet=diet, stress=stress,
                          fh_diabetes=fh_d, fh_heart=fh_h, fh_hyper=fh_ht))

    noise = lambda s=0.6: r.normal(0, s, n)
    logits = {
        "diabetes": 0.05*(age-45) + 0.12*(bmi-26) + 0.04*(glucose-95) + 0.9*(hba1c-5.4)
                    + 0.6*fh_d - 0.12*activity + 0.02*(waist-90) - 0.08*diet + noise(),
        "heart": 0.07*(age-45) + 0.6*sex + 0.02*(sbp-120) + 0.012*(ldl-120) - 0.025*(hdl-50)
                 + 0.9*smoker + 0.01*(glucose-95) + 0.6*fh_h - 0.1*activity + 0.06*stress + noise(),
        "hypertension": 0.04*(age-45) + 0.06*(sbp-120) + 0.03*(dbp-80) + 0.06*(bmi-26)
                        + 0.4*fh_ht + 0.03*alcohol - 0.1*activity + 0.05*stress + noise(),
        "stroke": 0.08*(age-55) + 0.03*(sbp-130) + 0.8*smoker + 0.02*(glucose-95)
                  + 0.5*fh_h + 0.004*(ldl-120) + noise(),
        "ckd": 0.05*(age-50) + 2.5*(creat-0.9) + 0.02*(sbp-125) + 0.015*(glucose-95)
               + 0.3*smoker + noise(),
        "fatty_liver": 0.15*(bmi-26) + 0.03*(waist-90) + 0.004*(tg-130) + 0.02*(glucose-95)
                       + 0.05*alcohol - 0.1*activity - 0.05*diet + noise(),
    }
    for key, (_, prev, *_rest) in DISEASES.items():
        p = _sigmoid(_calibrate(logits[key], prev))
        X[key] = r.binomial(1, p)
    return X

if __name__ == "__main__":
    df = generate()
    print(df.shape); print(df[list(DISEASES)].mean().round(3))
