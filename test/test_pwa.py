import pytest
import json
from cacao.core.pwa import PWASupport
from pathlib import Path

@pytest.fixture
def pwa_support():
    return PWASupport(app_name="Test App")

def test_manifest_generation(pwa_support):
    manifest_json = pwa_support.generate_manifest()
    manifest = json.loads(manifest_json)
    assert manifest["name"] == "Test App"
    assert manifest["display"] == "standalone"
    assert "icons" in manifest

def test_service_worker_generation(pwa_support):
    sw_content = pwa_support.generate_service_worker()
    assert "self.addEventListener('install'" in sw_content
    assert "self.addEventListener('fetch'" in sw_content

def test_pwa_configuration(pwa_support):
    assert pwa_support.app_name == "Test App"
    assert pwa_support.enable_offline == True
    assert pwa_support.theme_color == "#6B4226"