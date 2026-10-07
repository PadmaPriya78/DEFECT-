"""
Regex/heuristic feature extractor.
Language-agnostic pass: works reasonably for C-like languages (Java, JS, TS, C#, C++, Go).
Swap in tree-sitter/AST parsers later for higher accuracy — keep the same
output schema so the trained model doesn't need retraining.
"""

import re

COMMENT_LINE_RE = re.compile(r"^\s*(//|#|\*|/\*)")
FUNCTION_RE = re.compile(
    r"\b(public|private|protected|static|def|function|func|fn)\b[^\n{;]*\([^)]*\)\s*\{?"
)
CLASS_RE = re.compile(r"\b(class|interface|struct)\s+\w+")
IMPORT_RE = re.compile(r"^\s*(import|using|require|include|from)\b", re.MULTILINE)

# crude cyclomatic-complexity proxy: count branching keywords + 1
BRANCH_KEYWORDS = re.compile(
    r"\b(if|else if|elif|for|foreach|while|case|catch|except|&&|\|\|)\b"
)


def extract_features(source_code: str) -> dict:
    lines = source_code.splitlines()
    loc = len([l for l in lines if l.strip()])

    comment_lines = len([l for l in lines if COMMENT_LINE_RE.match(l)])
    comment_ratio = comment_lines / loc if loc else 0.0

    num_functions = len(FUNCTION_RE.findall(source_code))
    num_classes = len(CLASS_RE.findall(source_code))
    num_imports = len(IMPORT_RE.findall(source_code))
    complexity = 1 + len(BRANCH_KEYWORDS.findall(source_code))

    return {
        "loc": loc,
        "complexity": float(complexity),
        "num_functions": num_functions,
        "num_classes": num_classes,
        "num_imports": num_imports,
        "comment_ratio": round(comment_ratio, 4),
    }


SOURCE_EXTENSIONS = {
    ".java", ".py", ".js", ".jsx", ".ts", ".tsx",
    ".go", ".cs", ".cpp", ".c", ".h", ".hpp", ".rb", ".php",
}

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "venv", ".venv",
    "__pycache__", "target", "vendor", ".next", "coverage",
}


def is_source_file(path: str) -> bool:
    import os
    _, ext = os.path.splitext(path)
    return ext.lower() in SOURCE_EXTENSIONS
