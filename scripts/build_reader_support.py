"""Build subscription language pages; payment configuration has a separate gate."""
import json

def support_data(public):
    data = json.loads((public / "content/reader-support.json").read_text())
    for row in data.values():
        if "/" in row["file"] or not row["file"].startswith("support"):
            raise ValueError("Invalid support page filename")
    return data

def build_reader_support(public):
    from build_subscription_pages import build
    return build(public, support_data(public))
