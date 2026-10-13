import argparse

parser = argparse.ArgumentParser()
parser.add_argument("workflow_url", nargs=1, type=str)
parser.add_argument("infiles", nargs="+", type=argparse.FileType("r"))
parser.add_argument("outfile", type=argparse.FileType("w"))
args = parser.parse_args()


logs = "\n".join(f.read() for f in args.infiles)
content = f"""
[Workflow Run URL]({args.workflow_url})

{logs}
""".rstrip()
args.outfile.write(content)
