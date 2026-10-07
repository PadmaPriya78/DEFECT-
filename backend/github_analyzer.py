import os
import shutil
import tempfile
from git import Repo

from feature_extractor import extract_features, is_source_file, EXCLUDE_DIRS
from ml_predictor import predict_probability, probability_to_risk, generate_flag_reason

CLONE_DIR = os.getenv("CLONE_DIR", "./tmp_repos")
MAX_FILE_BYTES = 500_000  # skip absurdly large generated files


def clone_repo(repo_url: str) -> str:
    os.makedirs(CLONE_DIR, exist_ok=True)
    target = tempfile.mkdtemp(dir=CLONE_DIR)
    Repo.clone_from(repo_url, target, depth=1)
    return target


def iter_source_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fname in filenames:
            full = os.path.join(dirpath, fname)
            if is_source_file(full) and os.path.getsize(full) <= MAX_FILE_BYTES:
                yield full


def analyze_repository(repo_url: str) -> list[dict]:
    """
    Clones repo_url, extracts features per source file, runs the model,
    returns a list of module result dicts. Always cleans up the clone.
    """
    target_dir = clone_repo(repo_url)
    results = []
    try:
        for filepath in iter_source_files(target_dir):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
            except OSError:
                continue

            features = extract_features(code)
            prob = predict_probability(features)
            risk = probability_to_risk(prob)

            rel_path = os.path.relpath(filepath, target_dir)
            results.append({
                "file_path": rel_path,
                **features,
                "defect_probability": round(prob, 4),
                "risk_level": risk,
                "flag_reason": generate_flag_reason(features, prob),
            })
    finally:
        import stat
        def remove_readonly(func, path, excinfo):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass
        shutil.rmtree(target_dir, onerror=remove_readonly)

    return results
