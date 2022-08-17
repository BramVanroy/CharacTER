# CharacTER

CharacTER: Translation Edit Rate on Character Level

CharacTer (cer) is a novel character level metric inspired by the commonly applied translation edit rate (TER). It is defined
as the minimum number of character edits required to adjust a hypothesis, until it completely matches the reference,
normalized by the length of the hypothesis sentence. CharacTer calculates the character level edit distance while
performing the shift edit on word level. Unlike the strict matching criterion in TER, a hypothesis word is considered
to match a reference word and could be shifted, if the edit distance between them is below a threshold value. The
Levenshtein distance between the reference and the shifted hypothesis sequence is computed on the character level. In
addition, the lengths of hypothesis sequences instead of reference sequences are used for normalizing the edit
distance, which effectively counters the issue that shorter translations normally achieve lower TER.


## Modifications by Bram Vanroy

Bram Vanroy made some changes to this package that do not affect the result of calculate the metric but that should
improve usability. Code has been re-written to avoid the need for custom C++ code (instead the [C implementation
of Levenshtein](https://github.com/maxbachmann/Levenshtein) alongside an LRU cache is used), to make functions more
accessible and readable, and typing info has been included. Packaging has also improved to make uploading to PyPi a
breeze. This means that the package can now be installed via pip:

```shell
pip install cer
```

The main functions are `calculate_cer` and `calculate_cer_corpus`, which both expect tokenized input. The first
argument contains the hypotheses and the second the references.

```python
from cer import calculate_cer

cer_score = calculate_cer(["i", "like", "your", "bag"], ["i", "like", "their", "bags"])
cer_score
0.3333333333333333
```

`calculate_cer_corpus` is similar but instead it expects a sequence of sequence of words, basically a corpus of
sentences of words. It will report some statistics of the sentence-level CER scores that were calculated.

```python
from cer import calculate_cer_corpus

hyps = ["this week the saudis denied information published in the new york times",
        "this is in fact an estimate"]
refs = ["saudi arabia denied this week information published in the american new york times",
        "this is actually an estimate"]

hyps = [sent.split() for sent in hyps]
refs = [sent.split() for sent in refs]

cer_corpus_score = calculate_cer_corpus(hyps, refs)
cer_corpus_score
{
    'count': 2,
    'mean': 0.3127282211789254,
    'median': 0.3127282211789254,
    'std': 0.07561653111280243,
    'min': 0.25925925925925924,
    'max': 0.36619718309859156
}
```

In addition to the Python interface, a command-line entry-point is also installed, which you can use as
`calculate-cer`. Its idea is to calculate aggregate scores on the corpus-level (similar to calculate_cer_corpus)
based on two input files. One with hypotheses and one with references (one on each line). Results are written to
stdout.

```shell
usage: calculate-cer [-h] [-r] fhyp fref

CharacTER: Character Level Translation Edit Rate

positional arguments:
  fhyp                Path to file containing hypothesis sentences. One per line.
  fref                Path to file containing reference sentences. One per line.

optional arguments:
  -h, --help          show this help message and exit
  -r, --per_sentence  Whether to output CER scores per ref/hyp pair in addition to corpus-level statistics
```

## License
[GPLv3](LICENSE)

