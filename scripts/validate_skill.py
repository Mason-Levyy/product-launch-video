"""Validate every */SKILL.md frontmatter against the Agent Skills rules."""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def read_frontmatter(skill_file: Path) -> dict:
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter delimited by ---")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter is not a mapping")
    return frontmatter


def validate(skill_file: Path) -> list[str]:
    try:
        frontmatter = read_frontmatter(skill_file)
    except (ValueError, yaml.YAMLError) as error:
        return [str(error)]

    problems = []
    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not NAME_PATTERN.match(name):
        problems.append("name must be lowercase letters, digits and single hyphens")
    elif len(name) > MAX_NAME_LENGTH:
        problems.append(f"name exceeds {MAX_NAME_LENGTH} characters")
    elif name != skill_file.parent.name:
        problems.append(f"name '{name}' does not match folder '{skill_file.parent.name}'")

    if not isinstance(description, str) or not description.strip():
        problems.append("description is required")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        problems.append(f"description exceeds {MAX_DESCRIPTION_LENGTH} characters")

    return problems


def main() -> int:
    skill_files = sorted(REPO_ROOT.glob("*/SKILL.md"))
    if not skill_files:
        print("no */SKILL.md found")
        return 1

    failed = False
    for skill_file in skill_files:
        relative_path = skill_file.relative_to(REPO_ROOT).as_posix()
        problems = validate(skill_file)
        if problems:
            failed = True
            for problem in problems:
                print(f"FAIL {relative_path}: {problem}")
        else:
            print(f"ok   {relative_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
