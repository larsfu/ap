import uncertainties

def maketable(values, file_path):
    output = ''
    for row in zip(*values):
        row_reformatted = []
        for number in row:
            if isinstance(number, uncertainties.UFloat):
                row_reformatted.append(number.n)
                row_reformatted.append(number.s)
            else:
                row_reformatted.append(number)
        output += '& ' #Extra row for siunitx
        output += ' & '.join(str(e) for e in row_reformatted)
        output += ' \\\\\n'
    f = open(file_path, 'w')
    f.write(output)
    f.close()
