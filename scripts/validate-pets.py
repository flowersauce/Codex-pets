#!/usr/bin/env python3
"""Validate the repository's Codex pet packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image


EXPECTED_SIZE = (1536, 1872)
REQUIRED_SUBMISSION_FIELDS = ("schemaVersion", "petId", "name", "author", "description", "tags", "license")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_pet(pet_dir: Path) -> list[str]:
    errors = []
    pet_json = pet_dir / "pet.json"
    submission_json = pet_dir / "submission.json"

    if not pet_json.exists():
        return [f"{pet_dir}: missing pet.json"]
    if not submission_json.exists():
        errors.append(f"{pet_dir}: missing submission.json")

    pet = read_json(pet_json)
    pet_id = pet.get("id")
    if pet_id != pet_dir.name:
        errors.append(f"{pet_dir}: pet.json id must match directory name ({pet_dir.name})")

    spritesheet = pet_dir / pet.get("spritesheetPath", "")
    if not spritesheet.exists():
        errors.append(f"{pet_dir}: missing spritesheet {pet.get('spritesheetPath')}")
    else:
        with Image.open(spritesheet) as image:
            if image.size != EXPECTED_SIZE:
                errors.append(f"{pet_dir}: spritesheet must be {EXPECTED_SIZE}, got {image.size}")

    if submission_json.exists():
        submission = read_json(submission_json)
        for field in REQUIRED_SUBMISSION_FIELDS:
            if field not in submission:
                errors.append(f"{pet_dir}: submission.json missing {field}")
        if submission.get("petId") != pet_id:
            errors.append(f"{pet_dir}: submission petId must match pet.json id")
        author = submission.get("author", {})
        if not author.get("name"):
            errors.append(f"{pet_dir}: submission author.name is required")

    return errors


def main() -> int:
    root = repo_root()
    pet_dirs = sorted(path for path in (root / "pets").iterdir() if path.is_dir())
    all_errors = []
    for pet_dir in pet_dirs:
        all_errors.extend(validate_pet(pet_dir))

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(pet_dirs)} pet package(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
