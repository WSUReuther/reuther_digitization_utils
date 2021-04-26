import csv


def parse_csv(csv_filepath):
    data = {"collection": {}, "items": []}
    with open(csv_filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        date_headers = [header for header in headers if header.startswith("date")]
        for row in reader:
            if not data["collection"].get("collection_id"):
                if row.get("collection_id"):
                    collection_id = row["collection_id"]
                else:
                    collection_id = row["component_id"].split("_")[0]
                data["collection"]["collection_id"] = collection_id
            dates = []
            for date_header in date_headers:
                if row.get(date_header):
                    dates.append(row[date_header])
            item_metadata = {
                "item_identifier": row["component_id"],
                "title": row["title"],
                "dates": ", ".join(dates),
                "box": row["box"],
                "uri": row["uri"],
                "folder": row.get("folder")
            }
            data["items"].append(item_metadata)
    return data
