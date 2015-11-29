import uncertainties

def format(row, reformat_with_exponent):
    row_reformatted = []
    for number in row:
        if isinstance(number, uncertainties.UFloat):
            n = number.n
            s = number.s
            #Ist das wohl böse? Ist mir egal!
            if n == 0:
                n = int(0)
            if s == 0:
                s = int(0)
            row_reformatted.append(n)
            row_reformatted.append(s)
        elif number == None:
            row_reformatted.append('{}')
        else:
            row_reformatted.append(number)
    if(reformat_with_exponent):
        return '& '  +  ' & '.join("{:.2e}".format(e) for e in row_reformatted) +  ' \\\\\n'
    else:
        return '& '  +  ' & '.join(str(e) for e in row_reformatted) +  ' \\\\\n'

def maketable(values, file_path, reformat_with_exponent=False):
    output = ''
    if hasattr(values[0], '__iter__'):
        for row in zip(*values):
            output += format(row, reformat_with_exponent)
    else:
        output = format(values, reformat_with_exponent)
    f = open(file_path, 'w')
    f.write(output)
    f.close()
