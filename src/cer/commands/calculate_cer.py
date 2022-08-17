from os import PathLike
from pathlib import Path
from statistics import mean, median, stdev
from typing import Union

from cer import calculate_cer, calculate_cer_corpus


def calculate_cer_from_files(fhyp: Union[str, PathLike], fref: Union[str, PathLike], per_sentence: bool = False):
    """Entry point to calculate CER between two given files and reporting the results to stdout.
    :param fhyp: path to file containing reference sentences. One per line.
    :param fref: path to file containing reference sentences. One per line.
    :param per_sentence: whether to output CER scores per ref/hyp pair in addition to corpus-level statistics
    """
    hyp_sents = [l.split() for l in Path(fhyp).read_text(encoding="utf-8").splitlines()]
    ref_sents = [l.split() for l in Path(fref).read_text(encoding="utf-8").splitlines()]

    if len(ref_sents) != len(hyp_sents):
        raise ValueError("Both files need to contain the same number of lines!")

    if per_sentence:
        cers = []
        for line_idx, (hyp, ref) in enumerate(zip(hyp_sents, ref_sents), 1):
            cer_score = calculate_cer(hyp, ref)
            print(f"Hypothesis {line_idx:,}:\t{' '.join(hyp)}")
            print(f"Reference {line_idx:,}:\t{' '.join(ref)}")
            print(f"CER score {line_idx:,}:\t{cer_score}")
            print()
            cers.append(cer_score)

        stats = {
            "count": len(cers),
            "mean": mean(cers),
            "median": median(cers),
            "std": stdev(cers),
            "min": min(cers),
            "max": max(cers),
        }
    else:
        stats = calculate_cer_corpus(hyp_sents, ref_sents)

    print("Processing completed! Corpus statistics:\n========================================")
    print(stats)
    return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description="CharacTER: Character Level Translation Edit Rate")
    parser.add_argument("fhyp", help="Path to file containing hypothesis sentences. One per line.")
    parser.add_argument("fref", help="Path to file containing reference sentences. One per line.")

    parser.add_argument(
        "-r",
        "--per_sentence",
        action="store_true",
        default=False,
        help="Whether to output CER scores per ref/hyp pair in addition to corpus-level statistics",
    )

    args = parser.parse_args()
    calculate_cer_from_files(**vars(args))


if __name__ == "__main__":
    main()
