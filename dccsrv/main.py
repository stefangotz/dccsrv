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

from fastapi import FastAPI

from dccsrv.config import Settings

_CFG = Settings()

app = FastAPI(
    title=_CFG.project_name,
    description=_CFG.project_description,
    version=_CFG.project_version,
    cfg=_CFG,
)


@app.get("/")
def get_root():
    return {
        "name": app.extra["cfg"].project_name,
        "description": app.extra["cfg"].project_description,
        "version": app.extra["cfg"].project_version,
        "license": app.extra["cfg"].project_license,
    }
