import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
import itertools

round_figures_error = 1
max_magnitude = 6
min_magnitude = -4

def table(values, names, file, caption, label, split=1, footer=None, round_figures=None, interrows=None):
    result = r"""\begin{table}
        \caption{"""+caption+"""}
        \centering
        \label{"""+label+r"""}
        \begin{tabular}{l@{}"""

    reformat_list = list()
    unc_list = list()
    columns = ""
    for s in values if round_figures == None else zip(values, round_figures):
        if round_figures != None:
            round_figures_here = s[1]
            s = s[0]
        else:
            round_figures_here = 4
        if isinstance(s, np.ndarray) and s.dtype == 'object' and not isinstance(s[0], unc.UFloat):
            number_format = get_format_string_bytes(s)
            reformat = False
            unc_list.append(False)
            columns += "S[round-mode=off, table-format="+number_format+"]"
        elif isinstance(s[0], unc.UFloat):
            unc_list.append(True)
            number_format, reformat = get_format_string(unp.nominal_values(s[s!=0]), round_figures_here)
            error_format, reformat_ = get_format_string(unp.std_devs(s[s!=0]), round_figures_error)
            if True:
                columns += "S[table-format="+number_format+r", round-precision="+str(round_figures_here)+", round-mode=figures] @{${}\pm{}$} S[table-format="+error_format+", round-precision="+str(round_figures_error)+", round-mode=figures] "
            else:
                columns += "S[table-format="+number_format+r", round-mode=off] @{${}\pm{}$} S[table-format="+error_format+", round-mode=off] "
        else:
            unc_list.append(False)
            number_format, reformat = get_format_string(s[s!=0], round_figures_here)
            if True:
                columns += "S[table-format="+number_format+r", round-precision="+str(round_figures_here)+", round-mode=figures] "
            else:
                columns += "S[table-format="+number_format+r", round-mode=off] "
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

    i = 0
    for row in itertools.zip_longest(*final):
        if interrows != None and i in interrows:
            result += r" \multicolumn{{{}}}{{c}}{{{}}} \rule{{0pt}}{{3ex}}\\".format(len(row)+unc_list.count(True)+1, interrows[i])
        result += format_row(row, reformat_list*split, unc_list*split)
        i+=1

    if footer != None:
        result += r"\midrule \multicolumn{{{}}}{{c}}{{{}}}\\".format(len(row)+unc_list.count(True)+1, footer)

    result += r" \bottomrule \end{tabular} \end{table}"
    with open(file, 'w') as f:
        f.write(result)

def format_row(row, reformat_list, is_uncertain_list):
    row_reformatted = []
    for number in zip(row, reformat_list, is_uncertain_list):
        number, reformat, is_uncertain = number
        if number == None:
            row_reformatted.append('{}')
        elif isinstance(number, bytes):
            row_reformatted.append(number.decode('utf-8'))
        elif is_uncertain:
            n = number.n
            s = number.s
            if n == 0:
                n = int(0)
            if s == 0:
                s = int(0)
            if not reformat:
                row_reformatted.append("{:.20f}".format(n))
                row_reformatted.append("{:.20f}".format(s))
            else:
                row_reformatted.append("{:.2e}".format(n))
                row_reformatted.append("{:.2e}".format(s))
        else:
            if number == 0:
                number = "0"
            if not reformat:
                row_reformatted.append("{:.20f}".format(number))
            else:
                row_reformatted.append("{:.2e}".format(number))

    return '& '  +  ' & '.join(row_reformatted) +  ' \\\\\n'

def get_format_string(set, precision):
    mag = np.ceil(np.log10(np.absolute(set))).astype(int)

    if mag.max() > max_magnitude or mag.min() < min_magnitude:
        reformat = True
        string = "{}.{}".format(1, precision-1)
        string += "e{}".format(np.ceil(np.log10(abs(mag).max())).astype(int) + (1 if mag[abs(mag).argmax()] < 0 else 0))
    else:
        reformat = False
        pre = mag.max()
        if pre < 1: pre = 1
        post = -mag.min()+precision
        if post < 0: post = 0
        string = "{}.{}".format(pre, post)
    return (string, reformat)

def get_format_string_bytes(set):
    pre = 0
    post = 0
    for s in set:
        k = s.decode('utf-8').split('.')
        if len(k) == 1:
            if len(k[0]) > pre:
                pre = len(k[0])
        else:
            if len(k[0]) > pre:
                pre = len(k[0])
            if len(k[1]) > post:
                post = len(k[1])

    return str(pre) + '.' + str(post)
