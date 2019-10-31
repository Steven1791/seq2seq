#!/usr/bin/env python3
# coding=utf-8

import numpy as np
import argparse
import random
from nltk.translate.bleu_score import corpus_bleu


parser = argparse.ArgumentParser(description='Calculates WER on each Line from the provided two text files')
parser.add_argument('input_1', help="Hypotheses, your Text to evaluate against ground truth (input 2), with one sentence per line")
parser.add_argument('input_2', help="Ground truth text file, with one sentence per line")
args = parser.parse_args()

hypotheses_input = open(args.input_1,'r').readlines()
references_input = open(args.input_2,'r').readlines()
print("The hypotheses file has %s Lines" % len(hypotheses_input))
print("The target file has %s Lines" % len(references_input))

''' Format must be:
references = [[['this', 'is', 'a', 'test'], ['this', 'is' 'test']]] # there can be multiple references
candidates = [['this', 'is', 'a', 'test']] '''

candidates = [s.split() for s in hypotheses_input]
references = [[s.split()] for s in references_input] # note the extra square brackets
score = corpus_bleu(references, candidates)
print(score, " # <--BLEU score (corpus)")



# From Bérards Code
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


#------------WER print:----------
eval = corpus_wer(hypotheses_input, references_input)
wer, evalText = eval
print(wer, " # <--WER score")




