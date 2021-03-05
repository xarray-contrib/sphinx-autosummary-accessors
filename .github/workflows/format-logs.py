import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infiles", nargs="+", type=argparse.FileType("r"))
parser.add_argument("outfile", type=argparse.FileType("w"))
args = parser.parse_args()


content = "\n".join(f.read() for f in args.infiles)
args.outfile.write(content)
