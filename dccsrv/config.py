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

from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "dccsrv"
    project_description: str = "A REST API server for Dungeon Crawl Classics characters"
    project_license: str = """dccsrv is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

dccsrv is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with dccsrv. If not, see <https://www.gnu.org/licenses/>."""
    project_version: str = "0.1.0"
    api_versions: List[str] = ["v0"]
    api_key: str


CFG = Settings()


def get_cfg() -> Settings:
    return CFG
