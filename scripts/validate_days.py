"""Validate the `days/` folders for required files and uniqueness.

Checks performed:
- Every `days/dayNN_*` folder contains `challenge.md`.
- Day numbers (NN) are unique.
- If `meta.yaml` exists, it's valid YAML and `difficulty` (if present) is 1-5.

Exit codes:
 0 on success, 1 on validation failures.
"""
import os
import re
import sys
import yaml


def validate_days(days_root):
    if not os.path.isdir(days_root):
        print(f"Days directory not found: {days_root}")
        return 1

    day_nums = {}
    errors = 0

    for entry in sorted(os.listdir(days_root)):
        entry_path = os.path.join(days_root, entry)
        if not os.path.isdir(entry_path):
            continue

        m = re.match(r'day(\d+)_?(.*)', entry, re.IGNORECASE)
        if not m:
            print(f"Skipping non-conforming folder: {entry}")
            continue

        day_num = int(m.group(1))
        if day_num in day_nums:
            print(f"Duplicate day number: {day_num} in {entry} and {day_nums[day_num]}")
            errors += 1
        else:
            day_nums[day_num] = entry

        # check challenge.md
        md_path = os.path.join(entry_path, 'challenge.md')
        if not os.path.isfile(md_path):
            print(f"Missing challenge.md in {entry}")
            errors += 1

        # validate meta.yaml if present
        meta_path = os.path.join(entry_path, 'meta.yaml')
        if os.path.isfile(meta_path):
            try:
                with open(meta_path, 'r', encoding='utf-8') as mf:
                    meta = yaml.safe_load(mf) or {}
                diff = meta.get('difficulty')
                if diff is not None:
                    d = int(diff)
                    if d < 1 or d > 5:
                        print(f"Invalid difficulty in {entry}/meta.yaml: {diff}")
                        errors += 1
            except Exception as e:
                print(f"Error parsing meta.yaml in {entry}: {e}")
                errors += 1

    if errors:
        print(f"Validation failed with {errors} errors")
        return 1

    print(f"Validated {len(day_nums)} day folders successfully")
    return 0


if __name__ == '__main__':
    # days root relative to repo root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    days_root = os.path.join(repo_root, 'days')
    rc = validate_days(days_root)
    sys.exit(rc)
