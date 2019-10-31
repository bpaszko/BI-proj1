def load_fasta(path):
    with open(path) as f:
        _ = f.readline()
        return f.read().replace('\n', '').strip()
