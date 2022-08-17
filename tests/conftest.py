from pytest import fixture


@fixture
def example_saudis():
    return {"hyp": "this week the saudis denied information published in the new york times",
            "ref": "saudi arabia denied this week information published in the american new york times",
            "cer": 0.36619718309859156}


@fixture
def example_estimate():
    return {"hyp": "this is in fact an estimate",
            "ref": "this is actually an estimate",
            "cer": 0.25925925925925924}
