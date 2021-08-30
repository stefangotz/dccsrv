# Copyright 2021 Stefan Götz <github.nooneelse@spamgourmet.com>

# This file is part of dccsrv.

# dccsrv is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# dccsrv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with dccsrv. If not, see <https://www.gnu.org/licenses/>.

import json

from fastapi.testclient import TestClient
from fastapi import status

from dccsrv.main import app

client = TestClient(app)


def test_get_characters():
    response = client.get(
        "/v0/characters", headers={"access_token": app.extra["cfg"].api_key}
    )
    assert response.status_code == 200
    assert response.json() == {
        "mediocremel": {"name": "Mediocre Mel", "user": "Misha", "init": 0}
    }


def test_get_character():
    response = client.get(
        "/v0/characters/mediocremel", headers={"access_token": app.extra["cfg"].api_key}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Mediocre Mel", "user": "Misha", "init": 0}


def test_create_character():
    character: dict = {"name": "Average Alex", "user": "Avi", "init": 0}
    response = client.post(
        "/v0/characters/",
        headers={"access_token": app.extra["cfg"].api_key},
        data=json.dumps(character),
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert (
        response.headers.get("Location")
        == client.base_url + "/v0/characters/averagealex"
    )

    response = client.get(
        "/v0/characters/", headers={"access_token": app.extra["cfg"].api_key}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "mediocremel": {"name": "Mediocre Mel", "user": "Misha", "init": 0},
        "averagealex": character,
    }

    response = client.get(
        "/v0/characters/averagealex", headers={"access_token": app.extra["cfg"].api_key}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == character
