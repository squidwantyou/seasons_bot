for line in open( 'pnbs2.txt'):
    a,b = line.split()
    a = a.lstrip().strip()
    b = b.lstrip().strip()
    if a==b:
        pass
    else:
        print(f"{a} {b}")
