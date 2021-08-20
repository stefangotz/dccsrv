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

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

from dccsrv.config import Settings
from dccsrv.routers import main
from dccsrv.routers.v0 import characters

# API key authentication as per
# https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
# Other bits and pieces
# https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/

_CFG = Settings()
_API_KEY_NAME = "access_token"
_COOKIE_DOMAIN = "127.0.0.1"

_API_KEY_QUERY = APIKeyQuery(name=_API_KEY_NAME, auto_error=False)
_API_KEY_HEADER = APIKeyHeader(name=_API_KEY_NAME, auto_error=False)
_API_KEY_COOKIE = APIKeyCookie(name=_API_KEY_NAME, auto_error=False)


app = FastAPI(
    title=_CFG.project_name,
    description=_CFG.project_description,
    version=_CFG.project_version,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    cfg=_CFG,
)
app.include_router(main.router)
app.include_router(characters.router)


async def get_api_key(
    api_key_query: str = Security(_API_KEY_QUERY),
    api_key_header: str = Security(_API_KEY_HEADER),
    api_key_cookie: str = Security(_API_KEY_COOKIE),
):
    if api_key_query == _CFG.api_key:
        return api_key_query
    if api_key_header == _CFG.api_key:
        return api_key_header
    if api_key_cookie == _CFG.api_key:
        return api_key_cookie
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(
    api_key: APIKey = Depends(get_api_key),
):  # pylint: disable=unused-argument
    response = JSONResponse(
        get_openapi(
            title=_CFG.project_name, version=_CFG.project_version, routes=app.routes
        )
    )
    return response


@app.get("/docs", tags=["documentation"])
async def get_docs(
    api_key: APIKey = Depends(get_api_key),
):  # pylint: disable=unused-argument
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        _API_KEY_NAME,
        value=_CFG.api_key,
        domain=_COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@app.get("/logout")
async def logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(_API_KEY_NAME, domain=_COOKIE_DOMAIN)
    return response
