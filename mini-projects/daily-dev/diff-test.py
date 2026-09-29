"""Smoke tests for the text diff utility."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory

MODULE_PATH = Path(__file__).with_name("diff.py")
spec = spec_from_file_location("daily_dev_diff", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load diff.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

with TemporaryDirectory() as directory:
    root = Path(directory)
    first = root / "first.txt"
    second = root / "second.txt"
    first.write_text("alpha\nbeta\n", encoding="utf-8")
    second.write_text("alpha\ngamma\n", encoding="utf-8")

    result = module.diff_files(str(first), str(second))
    assert "-beta" in result
    assert "+gamma" in result

print("diff.py smoke tests passed")
