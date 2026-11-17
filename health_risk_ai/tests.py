from engine import assess
def test_high_risk_profile():
    r = assess({"age":58,"sex":1,"height":170,"weight":98,"waist":112,"sbp":160,"dbp":100,"glucose":140,"smoker":1})
    assert max(x["risk"] for x in r["results"]) > 40
def test_low_risk_profile():
    r = assess({"age":25,"sex":0,"height":165,"weight":58,"activity":5,"diet":8})
    assert all(x["level"] == "Low" for x in r["results"])
def test_invalid_input():
    import pytest
    with pytest.raises(ValueError): assess({"age":10,"sex":0})
