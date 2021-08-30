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

from typing import Dict

from fastapi import APIRouter
from fastapi import Response
from fastapi import Request
from fastapi import status
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security.api_key import APIKey
from pydantic import BaseModel

from ...dependencies import get_api_key, get_character_id

router = APIRouter(prefix="/v0/characters")


class Character(BaseModel):
    name: str
    user: str
    init: int = -99


_CHARACTERS: Dict[str, Character] = {
    "mediocremel": Character(**{"name": "Mediocre Mel", "user": "Misha", "init": 0})
}


@router.get("/")
def get_characters(
    api_key: APIKey = Depends(get_api_key),
):  # pylint: disable=unused-argument
    return _CHARACTERS


@router.get("/{cid}")
def get_character(
    cid: str, api_key: APIKey = Depends(get_api_key)
):  # pylint: disable=unused-argument
    return _CHARACTERS[cid]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_character(character: Character, request: Request, response: Response):
    cid: str = get_character_id(character.name)
    response.headers["Location"] = str(request.url) + cid
    _CHARACTERS[cid] = character


@router.put("/{cid}", response_model=Character)
def update_character(cid: str, character: Character):
    encoded = jsonable_encoder(character)
    _CHARACTERS[cid] = encoded
    return encoded
