import uncertainties

def format(row, reformat_with_exponent):
    row_reformatted = []
    for number in row:
        if isinstance(number, uncertainties.UFloat):
            row_reformatted.append(number.n)
            row_reformatted.append(number.s)
        else:
            row_reformatted.append(number)
    if(reformat_with_exponent):
        return '& '  +  ' & '.join("{:.2e}".format(e) for e in row_reformatted) +  ' \\\\\n'
    else:
        return '& '  +  ' & '.join(str(e) for e in row_reformatted) +  ' \\\\\n'

def maketable(values, file_path, reformat_with_exponent):
    output = ''
    if hasattr(values[0], '__iter__'):
        for row in zip(*values):
            output += format(row, reformat_with_exponent)
    else:
        output = format(values, reformat_with_exponent)
    f = open(file_path, 'w')
    f.write(output)
    f.close()
