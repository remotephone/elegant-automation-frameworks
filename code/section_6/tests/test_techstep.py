import requests


def test_get_successful_response():
    resp = requests.get("https://techstepacademy.com/training-ground")
    assert resp.status_code == 200


def test_get_content_in_response():
    resp = requests.get("https://techstepacademy.com/training-ground")
    assert "twitter" in resp.text
