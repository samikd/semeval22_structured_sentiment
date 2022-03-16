import random


def _get_latex_doc(content):
    doc = fr"""
    \documentclass{{article}}

    \usepackage{{tikz-dependency}}
    \usepackage{{caption}}
    \usepackage[landscape]{{geometry}}
    \usepackage{{cprotect}}
    \usepackage{{listings}}

    \begin{{document}}
    {content}
    \end{{document}}
    """

    return doc


def _get_tikz_dependency_inner_content(holder, target, exp, pol, serial, is_gold=True):
    pol_color = 'blue' if 'Positive' == pol else 'red'

    # FIXME indent the generated latex doc properly
    content = ''

    if len(holder) > 0:
        holder_begin_word_idx = min(holder) + 1
        holder_end_word_idx = max(holder) + 1

        if is_gold:
            content += (
                fr'\wordgroup[group style = {{fill = orange!40, draw = brown}}]{{1}}{{{holder_begin_word_idx}}}{{{holder_end_word_idx}}}{{holder-gold-{serial}}}\n')
        else:
            content += \
                fr'\wordgroup{{2}}{{{holder_begin_word_idx}}}{{{holder_end_word_idx}}}{{holder-pred-{serial}}}\n'

    if len(target) > 0:
        target_begin_word_idx = min(target) + 1
        target_end_word_idx = max(target) + 1

        if is_gold:
            content += \
                fr"""\wordgroup[group style = {{fill = orange!40, draw = brown}}]{{1}}{{{target_begin_word_idx}}}{{{target_end_word_idx}}}{{target-gold-{serial}}}
                """
        else:
            content += \
                fr"""\wordgroup{{2}}{{{target_begin_word_idx}}}{{{target_end_word_idx}}}{{target-pred-{serial}}}
                """

    exp_begin_word_idx = min(exp) + 1
    exp_end_word_idx = max(exp) + 1

    if is_gold:
        content += \
            fr"""\wordgroup[group style = {{fill = orange!40, draw = {pol_color}, ultra thick}}]{{1}}{{{exp_begin_word_idx}}}{{{exp_end_word_idx}}}{{exp-gold-{serial}}}
            """
    else:
        content += \
            fr"""\wordgroup[group style = {{draw = {pol_color}, ultra thick}}]{{2}}{{{exp_begin_word_idx}}}{{{exp_end_word_idx}}}{{exp-pred-{serial}}}
            """

    if len(holder) > 0:
        if is_gold:
            content += fr"""
                \groupedge[edge style = {{draw = brown}}, label style = {{circle, fill = orange!40, draw = brown}}]{{exp-gold-{serial}}}{{holder-gold-{serial}}}{{holder}}{{4ex}}
                """
        else:
            content += fr"""
                \groupedge[edge below, label style = {{circle}}]{{exp-pred-{serial}}}{{holder-pred-{serial}}}{{holder}}{{4ex}}
                """

    if len(target) > 0:
        if is_gold:
            content += fr"""
                \groupedge[edge style = {{draw = brown}}, label style = {{fill = orange!40, draw = brown}}]{{exp-gold-{serial}}}{{target-gold-{serial}}}{{target}}{{6ex}}
                """
        else:
            content += fr"""
                \groupedge[edge below]{{exp-pred-{serial}}}{{target-pred-{serial}}}{{target}}{{6ex}}
                """

    return content


def plot_gold_and_pred(tokenized_sent, gold, pred, latex_file):
    """Visualize gold and predicted spans/deps with tikz-dependency."""

    latex_tikz_dependency_content = ''

    for sent_idx in pred.keys():
        if random.random() > 0.1:
            continue

        sent = r' \& '.join(tokenized_sent[sent_idx]) + r' \\'

        gtuples = gold[sent_idx]
        gold_inner_content = ''
        for i, (holder, target, exp, pol) in enumerate(gtuples):
            gold_inner_content += _get_tikz_dependency_inner_content(
                holder, target, exp, pol, serial=i, is_gold=True)

        ptuples = pred[sent_idx]
        pred_inner_content = ''
        for i, (holder, target, exp, pol) in enumerate(ptuples):
            pred_inner_content += _get_tikz_dependency_inner_content(
                holder, target, exp, pol, serial=i, is_gold=False)

        # latex_tikz_dependency_content += fr"""
        # \begin{{figure}}
        # \begin{{adjustwidth*}}{{-2cm}}{{-2cm}}

        # \begin{{dependency}}
        # \begin{{deptext}}[column sep=.1cm, row sep=1ex]
        # {sent}
        # {sent}
        # \end{{deptext}}
        # {gold_inner_content}
        # {pred_inner_content}
        # \end{{dependency}}
        # \caption{{gold and predicted spans/deps: }}
        # \end{{adjustwidth*}}
        # \end{{figure}}
        # """

        esc_sent_idx = sent_idx.replace('_', '\_')

        latex_tikz_dependency_content += (fr"""
        \section{{Sentence}}

        \begin{{figure}}
        \begin{{adjustwidth*}}{{-2cm}}{{-2cm}}
        \begin{{dependency}}
        \begin{{deptext}}[column sep=.1cm, row sep=1ex]
        {sent}
        {sent}
        \end{{deptext}}
        {gold_inner_content}
        {pred_inner_content}
        \end{{dependency}}
        \end{{adjustwidth*}}
        \end{{figure}}

        \begin{{listing}}
        {gtuples}
        {ptuples}
        \end{{listing}}
        """

    with open(latex_file, "w") as f:
        f.write(_get_latex_doc(latex_tikz_dependency_content))
