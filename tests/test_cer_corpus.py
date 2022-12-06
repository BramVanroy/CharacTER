from statistics import mean, median, stdev

from cer import calculate_cer_corpus


def test_corpus(example_saudis, example_estimate):
    hyps = [example_saudis["hyp"].split(), example_estimate["hyp"].split()]
    refs = [example_saudis["ref"].split(), example_estimate["ref"].split()]
    results = calculate_cer_corpus(hyps, refs)
    real_results = [example_saudis["cer"], example_estimate["cer"]]

    assert abs(real_results[0] - example_saudis["cer"]) < 0.00000001
    assert abs(real_results[1] - example_estimate["cer"]) < 0.00000001

    assert results["count"] == len(hyps)
    assert abs(results["mean"] - mean(real_results)) < 0.00000001
    assert abs(results["median"] - median(real_results)) < 0.00000001
    assert abs(results["std"] - stdev(real_results)) < 0.00000001
    assert abs(results["min"] - min(real_results)) < 0.00000001
    assert abs(results["max"] - max(real_results)) < 0.00000001
    assert set(results.keys()) == {"count", "mean", "median", "std", "min", "max", "cer_scores"}


def test_corpus_singleton(example_saudis, example_estimate):
    hyps = [example_saudis["hyp"].split()]
    refs = [example_saudis["ref"].split()]
    results = calculate_cer_corpus(hyps, refs)
    real_results = example_saudis["cer"]

    assert abs(real_results - example_saudis["cer"]) < 0.00000001

    assert results["count"] == len(hyps)
    assert abs(results["mean"] - real_results) < 0.00000001
    assert abs(results["median"] - real_results) < 0.00000001
    assert results["std"] is None
    assert abs(results["min"] - real_results) < 0.00000001
    assert abs(results["max"] - real_results) < 0.00000001
    assert set(results.keys()) == {"count", "mean", "median", "std", "min", "max", "cer_scores"}
