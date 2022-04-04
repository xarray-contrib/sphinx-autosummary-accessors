import pathlib

root = pathlib.Path(__file__).parent / "templates"

known_templates = [str(path.relative_to(root)) for path in root.glob("**/*.rst")]
templates_path = str(root)
