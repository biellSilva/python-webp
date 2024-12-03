def get_version() -> str:
    from pathlib import Path

    version_path = Path(__file__).parent / "VERSION"

    return version_path.read_text().strip() if version_path.exists() else "0.0.1alpha"
