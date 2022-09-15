from functools import lru_cache
from itertools import product
from statistics import mean, median, stdev
from typing import Dict, Generator, List, Sequence, Tuple, Union

import Levenshtein


AddableStrSequence = Union[Tuple[str], List[str]]


@lru_cache(maxsize=1024)
def calculate_levenshtein(hyp_words: Tuple[str], ref_words: Tuple[str], *, do_norm=False) -> float:
    """Calculates and caches Levenshtein distance between two tuples of words (str).

    :param hyp_words: a tuple of words from the hypothesis. A tuple so that it is hashable
    :param ref_words: a tuple of words from the reference. A tuple so that it is hashable
    :param do_norm: whether or not to normalize by the number of reference words
    :return: the (potentially normalized) Levenshtein distance as a float
    """
    if do_norm:
        return Levenshtein.distance(hyp_words, ref_words) / len(ref_words)
    else:
        return Levenshtein.distance(hyp_words, ref_words)


def calculate_cer_corpus(hyps: Sequence[AddableStrSequence], refs: Sequence[AddableStrSequence]) -> Dict[str, float]:
    """Given a corpus of hypotheses and references (both sequences of sequences of strings (e.g. tokenized sentences))
    this function will calculate mean, median, std, min and max CER scores.

    :param hyps: corpus of hypotheses; sequences of sequences of words (str)
    :param refs: corpus of references; sequences of sequences of words (str)
    :return: a dictionary of mean, median, std, min and max CER scores, and the number of sentences (count)
    """
    cers = [calculate_cer(hyp, ref) for hyp, ref in zip(hyps, refs)]

    return {
        "count": len(cers),
        "mean": mean(cers),
        "median": median(cers),
        "std": stdev(cers),
        "min": min(cers),
        "max": max(cers),
        "cer_scores": cers,
    }


def calculate_cer(hyp_words: AddableStrSequence, ref_words: AddableStrSequence) -> float:
    """Calculates CharacTER (or cer, for short) between two sequences of words

    :param hyp_words: a sequence of words from the hypothesis
    :param ref_words: a sequence of words from the reference
    :return: the cer score
    """
    hyp_backup = hyp_words
    pre_score = calculate_levenshtein(tuple(hyp_words), tuple(ref_words), do_norm=True)

    if pre_score == 0:
        return 0.0

    # Shifting phrases of the hypothesis sentence until the edit distance from he reference sentence is minimized
    while True:
        diff, new_words = shifter(hyp_words, ref_words, pre_score)
        if diff <= 0:
            break

        hyp_words = new_words
        pre_score = pre_score - diff

    shift_cost = _shift_cost(hyp_words, hyp_backup)
    shifted_chars = " ".join(hyp_words)
    ref_chars = " ".join(ref_words)

    if len(shifted_chars) == 0:
        return 1.0

    edit_cost = calculate_levenshtein(tuple(shifted_chars), tuple(ref_chars)) + shift_cost

    return min(1.0, edit_cost / len(shifted_chars))


def shifter(
    hyp_words: AddableStrSequence, ref_words: AddableStrSequence, pre_score: float
) -> Tuple[float, AddableStrSequence]:
    """Some phrases in hypothesis sentences will be shifted, in order to minimize edit distances from reference
    sentences. As input the hypothesis and reference word lists as well as the cached edit distance calculator are
    required. It will return the difference of edit distances between before and after shifting, and the shifted
    version of the hypothesis sentence.

    :param hyp_words: a sequence of words from the hypothesis
    :param ref_words: a sequence of words from the reference
    :param pre_score: previously calculated "naive" Levenshtein distance
    :return: the difference of edit distances between before and after shifting, and the shifted version of the
    hypothesis sentence
    """
    scores = []
    # Changing the phrase order of the hypothesis sentence
    for hyp_start, ref_start, length in couple_discoverer(hyp_words, ref_words):
        shifted_words = hyp_words[:hyp_start] + hyp_words[hyp_start + length :]
        shifted_words[ref_start:ref_start] = hyp_words[hyp_start : hyp_start + length]
        shift_score = calculate_levenshtein(tuple(shifted_words), tuple(ref_words), do_norm=True)
        scores.append((pre_score - shift_score, shifted_words))

    # The case that the phrase order has not to be changed
    if not scores:
        return 0.0, hyp_words

    scores.sort()
    return scores[-1]


def couple_discoverer(
    sentence_1: AddableStrSequence, sentence_2: AddableStrSequence
) -> Generator[Tuple[int, int, int], None, None]:
    """This function will find out the identical phrases in sentence_1 and sentence_2, and yield the corresponding
    begin positions in both sentences as well as the maximal phrase length. Both sentences are represented
    as word (str) sequences.

    :param sentence_1: a sentence represented as a sequence of strings
    :param sentence_2: a sentence represented as a sequence of strings
    :return: a generator that yields tuples of ints: start index for sentence 1, start index for s. 2, and phrase
    length
    """
    # Applying the cartesian product to traversing both sentences
    for start_1, start_2 in product(range(len(sentence_1)), range(len(sentence_2))):
        # No need to shift if the positions are the same
        if start_1 == start_2:
            continue

        # If identical words are found in different positions of two sentences
        if sentence_1[start_1] == sentence_2[start_2]:
            length = 1

            # Go further to next positions of sentence_1 to learn longer phrase
            for step in range(1, len(sentence_1) - start_1):
                end_1, end_2 = start_1 + step, start_2 + step

                # If the new detected phrase is also contained in sentence_2
                if end_2 < len(sentence_2) and sentence_1[end_1] == sentence_2[end_2]:
                    length += 1
                else:
                    break

            yield start_1, start_2, length


def _shift_cost(shifted_words: AddableStrSequence, original_words: AddableStrSequence):
    """Calculate the shift cost on the hypothesis
    :param shifted_words: a sequence of words (str) in the shifted hypothesis sequence
    :param original_words: a sequence of words (str) in the original hypothesis sequence
    :return: the shift cost (the average word length of the shifted phrase)
    """
    shift_cost = 0.0
    original_start = 0

    # Go through all words in the shifted hypothesis sequence
    while original_start < len(shifted_words):
        avg_shifted_charaters = 0
        original_index = original_start

        # Avoid costs created by unnecessary shifts
        if original_words[original_start] == shifted_words[original_start]:
            original_start += 1
            continue

        # Go through words with larger index in original hypothesis sequence
        for shift_start in range(original_start + 1, len(shifted_words)):
            # Check whether there is word matching
            if original_words[original_start] == shifted_words[shift_start]:
                length = 1

                # Go on checking the following word pairs to find the longest matched phrase pairs
                for pos in range(1, len(original_words) - original_index):
                    original_end, shift_end = original_index + pos, shift_start + pos

                    # Check the next word pair
                    if shift_end < len(shifted_words) and original_words[original_end] == shifted_words[shift_end]:
                        length += 1

                        # Skip the already matched word pairs in the next loop
                        if original_start + 1 < len(original_words):
                            original_start += 1
                    else:
                        break

                shifted_charaters = 0

                # Sum over the lengths of the shifted words
                for index in range(length):
                    shifted_charaters += len(original_words[original_index + index])

                avg_shifted_charaters = float(shifted_charaters) / length
                break

        shift_cost += avg_shifted_charaters
        original_start += 1

    return shift_cost
