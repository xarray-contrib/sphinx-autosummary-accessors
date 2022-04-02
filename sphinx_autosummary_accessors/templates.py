import pathlib

root = pathlib.Path(__file__).parent / "templates"

known_templates = [path.name for path in root.glob("**/*.rst")]
templates_path = str(root)
