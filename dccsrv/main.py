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

from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse, JSONResponse

from dccsrv.config import Settings
from dccsrv.routers import main
from dccsrv.routers.v0 import characters
from dccsrv.dependencies import get_api_key, COOKIE_DOMAIN, API_KEY_NAME

# API key authentication as per
# https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
# Other bits and pieces
# https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/

_CFG = Settings()


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
        API_KEY_NAME,
        value=_CFG.api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@app.get("/logout")
async def logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response
