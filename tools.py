import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
import itertools

round_figures = 3
round_figures_error = 1
max_magnitude = 6
min_magnitude = -4

def format_row(row, reformat_list, is_uncertain_list):
    row_reformatted = []
    for number in zip(row, reformat_list, is_uncertain_list):
        number, reformat, is_uncertain = number
        if number == None:
            row_reformatted.append('{}')
        elif is_uncertain:
            n = number.n
            s = number.s
            if n == 0:
                n = int(0)
            if s == 0:
                s = int(0)
            if not reformat:
                row_reformatted.append(str(n))
                row_reformatted.append(str(s))
            else:
                row_reformatted.append("{:.2e}".format(n))
                row_reformatted.append("{:.2e}".format(s))
        else:
            if number == 0:
                number = "0"
            if not reformat:
                row_reformatted.append(str(number))
            else:
                row_reformatted.append("{:.2e}".format(number))

    return '& '  +  ' & '.join(row_reformatted) +  ' \\\\\n'

def get_format_string(set, precision):
    mag = np.ceil(np.log10(set)).astype(int)

    if mag.max() > max_magnitude or mag.min() < min_magnitude:
        reformat = True
        string = "{}.{}".format(1, precision-1)
        string += "e{}".format(np.ceil(np.log10(abs(mag).max())).astype(int) + (1 if mag[abs(mag).max()] < 0 else 0))
    else:
        reformat = False
        pre = mag.max()
        if pre < 1: pre = 1
        post = -mag.min()+precision
        if post < 0: post = 0
        string = "{}.{}".format(pre, post)
    return (string, reformat)

def table(values, names, file, label, caption, split=1, footer=None):
    result = r"""\begin{table}
        \caption{"""+caption+"""}
        \centering
        \label{"""+label+r"""}
        \begin{tabular}{l@{}"""

    reformat_list = list()
    unc_list = list()
    columns = ""
    for s in values:
        if isinstance(s[0], unc.UFloat):
            unc_list.append(True)
            number_format, reformat = get_format_string(unp.nominal_values(s[s!=0]), round_figures)
            error_format, reformat_ = get_format_string(unp.std_devs(s[s!=0]), round_figures_error)
            columns += "S[table-format="+number_format+r", round-precision="+str(round_figures)+", round-mode=figures] @{${}\pm{}$} S[table-format="+error_format+", round-precision="+str(round_figures_error)+", round-mode=figures] "
        else:
            unc_list.append(False)
            number_format, reformat = get_format_string(s[s!=0], round_figures)
            columns += "S[table-format="+number_format+r", round-precision="+str(round_figures)+", round-mode=figures] "
        reformat_list.append(reformat)

    result += '|'.join([columns] * split) + r"} \toprule "

    headers = ""
    for l in zip(names, unc_list):
        l, uncertain = l
        l = l.split("/")
        unit = ""
        if len(l) > 1:
            unit = r"/\si{"+l[1]+"}"
        if not uncertain:
            headers += r"& {$"+l[0]+unit+"$}"
        else:
            headers += r"& \multicolumn{2}{c}{$"+l[0]+unit+"$}"

    result += headers * split + r"\\\midrule"

    length = np.ceil(len(max(values,key=len))/split).astype(int)
    final = list()

    for i in range(0, split):
        for v in values:
            final.append(v[i*length:(i+1)*length])

    for row in itertools.zip_longest(*final):
        print(row)
        result += format_row(row, reformat_list*split, unc_list*split)

    if footer != None:
        result += r"\midrule" + footer

    result += r" \bottomrule \end{tabular} \end{table}"
    with open(file, 'w') as f:
        f.write(result)
