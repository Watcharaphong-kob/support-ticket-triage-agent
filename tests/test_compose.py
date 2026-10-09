import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(shutil.which("docker") is None, reason="Compose config is checked on the host")
def test_compose_requires_ready_database_and_isolated_persistent_storage():
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        ["docker", "compose", "config", "--format", "json"],
        cwd=root,
        env={**os.environ, "POSTGRES_PASSWORD": "test-placeholder-not-a-real-secret"},
        capture_output=True,
        text=True,
        check=True,
    )
    config = json.loads(completed.stdout)
    db = config["services"]["db"]
    assert "latest" not in db["image"]
    assert db["healthcheck"]["test"]
    assert db["ports"][0]["host_ip"] == "127.0.0.1"
    assert db["volumes"][0]["type"] == "volume"
    assert config["services"]["migrate"]["depends_on"]["db"]["condition"] == "service_healthy"
    assert (
        config["services"]["app"]["depends_on"]["migrate"]["condition"]
        == "service_completed_successfully"
    )
    api = config["services"]["api"]
    assert api["ports"][0]["host_ip"] == "127.0.0.1"
    assert api["depends_on"]["migrate"]["condition"] == "service_completed_successfully"
    assert api["image"] == config["services"]["app"]["image"]
