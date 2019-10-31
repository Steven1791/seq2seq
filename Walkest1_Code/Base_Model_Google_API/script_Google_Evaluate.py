#!/usr/bin/env python3

import numpy as np
import argparse
import random
import os
from collections import Counter
import math

parser = argparse.ArgumentParser(description='Calculates WER on each Line from the provided two text files')
parser.add_argument('input_1', help="Hypotheses, your Text to evaluate against ground truth (input 2), with one sentence per line")
parser.add_argument('input_2', help="Ground truth text file, with one sentence per line")
args = parser.parse_args()

wer_score_file = os.path.dirname(args.input_1) + "/" + os.path.splitext(os.path.basename(args.input_1))[0] + "_evaluated_WER_and_BLEU.txt"
hypotheses = args.input_1
target = args.input_2

import nltk
from nltk.translate.bleu_score import corpus_bleu

corpus_tokenized = [s.split() for s in reference_input]
references = [[['this', 'is', 'a', 'test'], ['this', 'is' 'test']]]

candidates = [['this', 'is', 'a', 'test']]

score = corpus_bleu(references, candidates)

print(score)






def levenshtein(src, trg, sub_cost=1.0, del_cost=1.0, ins_cost=1.0, randomize=True):
    DEL, INS, KEEP, SUB  = range(4)
    op_names = 'delete', 'insert', 'keep', 'sub'

    costs = np.zeros((len(trg) + 1, len(src) + 1))
    ops = np.zeros((len(trg) + 1, len(src) + 1), dtype=np.int32)

    costs[0] = range(len(src) + 1)
    costs[:,0] = range(len(trg) + 1)
    ops[0] = DEL
    ops[:,0] = INS

    if randomize:
        key = lambda p: (p[0], random.random())
    else:
        key = None

    for i in range(1, len(trg) + 1):
        for j in range(1, len(src) + 1):
            c, op = (sub_cost, SUB) if trg[i - 1] != src[j - 1] else (0, KEEP)
            costs[i,j], ops[i,j] = min([
                (costs[i, j - 1] + del_cost, DEL),
                (costs[i - 1, j] + ins_cost, INS),
                (costs[i - 1, j - 1] + c, op),
            ], key=key)

    # backtracking
    i, j = len(trg), len(src)
    cost = costs[i, j]

    res = []

    while i > 0 or j > 0:
        op = ops[i, j]
        op_name = op_names[op]

        if op == DEL:
            res.append(op_name)
            j -= 1
        else:
            res.append((op_name, trg[i - 1]))
            i -= 1
            if op != INS:
                j -= 1

    return cost, res[::-1]

def corpus_wer(hypotheses, references, char_based=False, **kwargs):
    def split(s):
        return tuple(s) if char_based else tuple(s.split())

    scores = [
        levenshtein(split(hyp), split(ref))[0] / len(split(ref))
        for hyp, ref in zip(hypotheses, references)
    ]

    score = 100 * sum(scores) / len(scores)

    hyp_length = sum(len(hyp.split()) for hyp in hypotheses)
    ref_length = sum(len(ref.split()) for ref in references)

    return score, 'ratio={:.3f}'.format(hyp_length / ref_length)


def sentence_bleu(hypothesis, reference, smoothing=True, order=4, **kwargs):
    """
    Compute sentence-level BLEU score between a translation hypothesis and a reference.

    :param hypothesis: list of tokens or token ids
    :param reference: list of tokens or token ids
    :param smoothing: apply smoothing (recommended, especially for short sequences)
    :param order: count n-grams up to this value of n.
    :param kwargs: additional (unused) parameters
    :return: BLEU score (float)
    """

    def divide(x, y):
        with np.errstate(divide='ignore', invalid='ignore'):
            z = np.true_divide(x, y)
            z[~ np.isfinite(z)] = 0
        return z

    log_score = 0

    if len(hypothesis) == 0:
        return 0

    for i in range(order):
        hyp_ngrams = Counter(zip(*[hypothesis[j:] for j in range(i + 1)]))
        ref_ngrams = Counter(zip(*[reference[j:] for j in range(i + 1)]))

        numerator = sum(min(count, ref_ngrams[bigram]) for bigram, count in hyp_ngrams.items())
        denominator = sum(hyp_ngrams.values())

        if smoothing:
            numerator += 1
            denominator += 1

        score = numerator / denominator

        if score == 0:
            log_score += float('-inf')
        else:
            log_score += math.log(score) / order

    bp = min(1, math.exp(1 - len(reference) / len(hypothesis)))

    return math.exp(log_score) * bp


#------------My Code:----------
lines_src = open(hypotheses,'r').readlines()
lines_trg = open(target,'r').readlines()
print("The hypotheses file has %s Lines" % len(lines_src))
print("The target file has %s Lines" % len(lines_trg))



with open(wer_score_file, 'w') as output:
    bleu_corpus_avg = 0
    bleu_score_list = []
    for sentence_hyp,sentence_ref in zip(lines_src, lines_trg):
        bleu_score_list.append(sentence_bleu(sentence_hyp, sentence_ref))
    
    bleu_score = np.mean(bleu_score_list)  # <---  MEAN of bleu scores
    print(bleu_score, " # <--bleu score")
    output.writelines(str(bleu_score))
    output.writelines(" #bleu score\n")

    eval = corpus_wer(lines_src, lines_trg)
    wer, evalText = eval
    print(wer, " # <--WER score")
    output.writelines(str(wer))
    output.writelines(" # <--WER score\n")




