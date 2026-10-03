# --- Tests de l'export JSON. ---

import json 
from pathlib import Path 

from network_toolkit.output import export_to_json


def test_export_to_json_creates_file(tmp_path):
    results = [
        {"port": 80, "protocol": "TCP", "state": "open", "banner": ""},
        {"port": 3306, "protocol": "TCP", "state": "open", "banner": "MariaDB"},
    ]
    metadata = {
        "target": "127.0.0.1",
        "protocol": "tcp",
        "port_range": "20-100",
        "threads": 100,
        "started_at": "2026-10-03T17:40:26",
        "finished_at": "2026-10-03T17:40:29",
        "duration_seconds": 2.31,
        "total_ports": 81,
    }
    output_file = tmp_path / "result.json"

    export_to_json(results, metadata, str(output_file))

    assert output_file.exists()
    with open(output_file, encoding="utf-8") as f:
        payload = json.load(f)

    assert payload["scan"]["target"] == "127.0.0.1"
    assert payload["scan"]["protocol"] == "tcp"
    assert payload["summary"]["total_ports"] == 81
    assert len(payload["results"]) == 2
    assert payload["results"][0]["port"] == 80
    assert payload["results"][1]["banner"] == "MariaDB"

def test_export_to_json_empty_results(tmp_path):
    output_file = tmp_path / ("empty.json")
    metadata = {
        "target": "127.0.0.1",
        "protocol": "tcp",
        "port_range": "20-100",
        "threads": 100,
        "started_at": "2026-10-03T17:40:26",
        "finished_at": "2026-10-03T17:40:29",
        "duration_seconds": 1.0,
        "total_ports": 81,
    }
    export_to_json([], metadata, str(output_file))

    with open(output_file, encoding="utf-8") as f:
        payload =json.load(f)

    assert payload["summary"]["open_ports"] == 0
    assert payload["results"] == []