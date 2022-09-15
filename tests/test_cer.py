from cer import calculate_cer


def test_example_saudis(example_saudis):
    hyp = example_saudis["hyp"].split()
    ref = example_saudis["ref"].split()
    result = calculate_cer(hyp, ref)

    assert abs(result - example_saudis["cer"]) < 0.00000001


def test_example_estimate(example_estimate):
    hyp = example_estimate["hyp"].split()
    ref = example_estimate["ref"].split()
    result = calculate_cer(hyp, ref)

    assert abs(result - example_estimate["cer"]) < 0.00000001
