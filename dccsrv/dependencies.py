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

import re

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from .config import get_cfg


# API key authentication as per
# https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680

COOKIE_DOMAIN = "127.0.0.1"
API_KEY_NAME = "access_token"

_API_KEY_QUERY = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
_API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
_API_KEY_COOKIE = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(_API_KEY_QUERY),
    api_key_header: str = Security(_API_KEY_HEADER),
    api_key_cookie: str = Security(_API_KEY_COOKIE),
):
    if api_key_query == get_cfg().api_key:
        return api_key_query
    if api_key_header == get_cfg().api_key:
        return api_key_header
    if api_key_cookie == get_cfg().api_key:
        return api_key_cookie
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


def get_character_id(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "", name).lower()
