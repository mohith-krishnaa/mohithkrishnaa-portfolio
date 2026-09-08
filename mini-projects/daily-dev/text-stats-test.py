"""Small smoke tests for text-stats.py."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("text-stats.py")
spec = spec_from_file_location("text_stats", MODULE_PATH)
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)


assert module.text_stats("hello world") == {
    "words": 2,
    "lines": 1,
    "characters": 11,
    "non_whitespace": 10,
}
assert module.text_stats("one\ntwo\n")["lines"] == 2
assert module.text_stats("hello\tworld")["words"] == 2
assert module.text_stats("   \n\t")["words"] == 0
assert module.text_stats("") == {
    "words": 0,
    "lines": 0,
    "characters": 0,
    "non_whitespace": 0,
}

print("text-stats smoke tests passed")
