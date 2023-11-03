"""Generate the confusables.rs file from the VS Code ambiguous.json file."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

CONFUSABLES_RS_PATH = "crates/ruff_linter/src/rules/ruff/rules/confusables.rs"
AMBIGUOUS_JSON_URL = "https://raw.githubusercontent.com/hediet/vscode-unicode-data/main/out/ambiguous.json"

prelude = """
//! This file is auto-generated by `scripts/update_ambiguous_characters.py`.

/// Via: <https://github.com/hediet/vscode-unicode-data/blob/main/out/ambiguous.json>
/// See: <https://github.com/microsoft/vscode/blob/095ddabc52b82498ee7f718a34f9dd11d59099a8/src/vs/base/common/strings.ts#L1094>
pub(crate) fn confusable(c: u32) -> Option<u8> {
  let result = match c {

""".lstrip()

postlude = """_ => return None, }; Some(result)}"""


def get_mapping_data() -> dict:
    """
    Get the ambiguous character mapping data from the vscode-unicode-data repository.

    Uses the system's `curl` command to download the data,
    instead of adding a dependency to a Python-native HTTP client.
    """
    content = subprocess.check_output(
        ["curl", "-sSL", AMBIGUOUS_JSON_URL],
        encoding="utf-8",
    )
    # The content is a JSON object literal wrapped in a JSON string, so double decode:
    return json.loads(json.loads(content))


def format_number(number: int) -> str:
    """Underscore-separate the digits of a number."""
    # For unknown historical reasons, numbers greater than 100,000 were
    # underscore-delimited in the generated file, so we now preserve that property to
    # avoid unnecessary churn.
    if number > 100000:
        number = str(number)
        number = "_".join(number[i : i + 3] for i in range(0, len(number), 3))
        return f"{number}_u32"

    return f"{number}u32"


def format_confusables_rs(raw_data: dict[str, list[int]]) -> str:
    """Format the downloaded data into a Rust source file."""
    # The input data contains duplicate entries
    flattened_items: set[tuple[int, int]] = set()
    for _category, items in raw_data.items():
        assert len(items) % 2 == 0, "Expected pairs of items"
        for i in range(0, len(items), 2):
            flattened_items.add((items[i], items[i + 1]))

    tuples = [
        f"    {format_number(left)} => {right},\n"
        for left, right in sorted(flattened_items)
    ]

    print(f"{len(tuples)} confusable tuples.")

    return prelude + "".join(tuples) + postlude


def main() -> None:
    print("Retrieving data...")
    mapping_data = get_mapping_data()
    formatted_data = format_confusables_rs(mapping_data)
    confusables_path = Path(__file__).parent.parent / CONFUSABLES_RS_PATH
    confusables_path.write_text(formatted_data, encoding="utf-8")
    print("Formatting Rust file with cargo fmt...")
    subprocess.check_call(["cargo", "fmt", "--", confusables_path])
    print("Done.")


if __name__ == "__main__":
    main()
