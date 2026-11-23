#!/usr/bin/env python3
"""Stream a GeoJSON FeatureCollection into small, individually named GeoJSON files.

Original geometry and properties are retained; oversized features are skipped and
logged so they can be processed separately. Designed for GEOlayers GitHub Browser.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import ijson
except ImportError:
    sys.exit("Install dependencies: py -m pip install -r requirements.txt")


def slugify(value):
    cleaned = unicodedata.normalize("NFKD", str(value))
    cleaned = cleaned.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", cleaned).strip("_")[:75] or "feature"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--category", required=True)
    parser.add_argument("--name-field", default="name")
    parser.add_argument("--max-features", type=int, default=100)
    parser.add_argument("--start-after", type=int, default=0,
                        help="Skip the first N input features")
    parser.add_argument("--max-file-mib", type=float, default=1.5)
    parser.add_argument("--contains", default="",
                        help="Export only features whose names contain this text")
    args = parser.parse_args()
    if args.max_features < 1 or args.start_after < 0 or args.max_file_mib <= 0:
        parser.error("--max-features and --max-file-mib must be positive; --start-after >= 0")
    if not args.input.exists():
        parser.error("Input file not found: " + str(args.input))

    target = args.output / slugify(args.category)
    target.mkdir(parents=True, exist_ok=True)
    reports = Path("reports")
    reports.mkdir(exist_ok=True)
    report = reports / (slugify(args.category) + "_export.csv")
    max_bytes = int(args.max_file_mib * 1024 * 1024)
    exported = 0
    scanned = 0
    last_index = args.start_after

    with args.input.open("rb") as source, report.open("w", newline="", encoding="utf-8") as log:
        writer = csv.writer(log)
        writer.writerow(["source_index", "name", "status", "output", "bytes"])
        # ijson streams one FeatureCollection feature at a time rather than
        # loading the entire GeoJSON into memory.
        for index, feature in enumerate(ijson.items(source, "features.item", use_float=True), start=1):
            scanned = index
            if index <= args.start_after:
                continue
            last_index = index
            if not isinstance(feature, dict) or feature.get("type") != "Feature":
                writer.writerow([index, "", "invalid_feature", "", 0])
                continue
            name = feature.get("properties", {}).get(args.name_field)
            if not name:
                name = feature.get("id", "feature_" + str(index))
            name = str(name)
            if args.contains and args.contains.casefold() not in name.casefold():
                continue

            payload = {
                "type": "FeatureCollection",
                "features": [feature],
            }
            # ijson may yield Decimal numbers; use_float=True below to
            # ensure JSON-compatible coordinate numbers.
            data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            if len(data) > max_bytes:
                writer.writerow([index, name, "oversized", "", len(data)])
                continue
            filename = slugify(name) + "_" + str(index).zfill(8) + ".geojson"
            output = target / filename
            output.write_bytes(data)
            writer.writerow([index, name, "exported", str(output), len(data)])
            exported += 1
            if exported >= args.max_features:
                break

    print("Scanned through feature index:", last_index or scanned)
    print("Exported:", exported)
    print("Output directory:", target)
    print("Report:", report)
    print("Next batch: --start-after", last_index)


if __name__ == "__main__":
    main()
