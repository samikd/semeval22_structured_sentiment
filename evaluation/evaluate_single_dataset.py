import os
import sys
from nltk.tokenize.simple import SpaceTokenizer
import argparse
from evaluate import convert_opinion_to_tuple, tuple_f1
import json

tk = SpaceTokenizer()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gold_file", help="gold json file")
    parser.add_argument("pred_file", help="prediction json file")

    args = parser.parse_args()

    with open(args.gold_file) as o:
        gold = json.load(o)

    with open(args.pred_file) as o:
        pred = json.load(o)

    tokenized_sent = dict(
        [(s["sent_id"], tk.tokenize(s["text"])) for s in gold])

    gold = dict([(s["sent_id"], convert_opinion_to_tuple(s)) for s in gold])
    pred = dict([(s["sent_id"], convert_opinion_to_tuple(s)) for s in pred])

    g = set(gold.keys())
    p = set(pred.keys())

    # assert g.issubset(p), f"missing some sentences: {g.difference(p)}"
    # assert p.issubset(g), f"predictions contain sentences that are not in golds: {p.difference(g)}"

    f1 = tuple_f1(gold, pred)
    print("Sentiment Tuple F1: {0:.3f}".format(f1))

    sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'viz'))
    from tikz_dependency import plot_gold_and_pred

    plot_gold_and_pred(tokenized_sent, gold, pred,
                       latex_file=os.path.join(
                           os.path.dirname(sys.path[0]), 'doc/main.tex'))


if __name__ == "__main__":
    main()
