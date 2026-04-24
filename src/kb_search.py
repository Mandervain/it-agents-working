import re
from pathlib import Path

KB_ROOT = Path("knowledge_base")


def read_kb_article(article_path: Path) -> str:
    with article_path.open() as f:
        return f.read()


def find_kb_article(category: str) -> str | None:
    exact = KB_ROOT / f"{category}.md"
    if exact.exists():
        return read_kb_article(exact)

    words = [w for w in re.split(r"[_\s]+", category.lower()) if len(w) > 2]
    for kb_file in sorted(KB_ROOT.glob("*.md")):
        if any(word in kb_file.stem for word in words):
            return read_kb_article(kb_file)

    return None
