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

from typing import Optional

from fastapi import APIRouter

router = APIRouter(prefix="/v0/characters")


_FIXED_CHARACTER = {"name": "Mediocre Mel", "user": "Misha", "init": 0}


@router.get("/")
def get_characters(_: Optional[str] = None):
    return _FIXED_CHARACTER
