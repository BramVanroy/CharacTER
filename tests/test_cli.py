from pathlib import Path
from statistics import mean, median, stdev

from cer.commands.calculate_cer import calculate_cer_from_files


def test_cli(example_saudis, example_estimate):
    real_results = [example_saudis["cer"], example_estimate["cer"]]

    curr_dir = Path(__file__).parent
    results = calculate_cer_from_files(curr_dir / "hyps.txt", curr_dir / "refs.txt")

    assert results["count"] == 2
    assert abs(results["mean"] - mean(real_results)) < 0.00000001
    assert abs(results["median"] - median(real_results)) < 0.00000001
    assert abs(results["std"] - stdev(real_results)) < 0.00000001
    assert abs(results["min"] - min(real_results)) < 0.00000001
    assert abs(results["max"] - max(real_results)) < 0.00000001
