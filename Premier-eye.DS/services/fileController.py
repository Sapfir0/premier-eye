def writeInFile(filename: str, *args):
    with open(filename, 'w') as f:
        for params in args:
            f.write(params + " ")
