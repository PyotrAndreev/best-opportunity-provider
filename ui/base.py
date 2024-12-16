from typing import Annotated, Any
from enum import IntEnum

from config import (
    app, templates, RequestValidationErrorHandler, HttpMethod,
)
import offer_db as db
import middleware as mw

from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from fastapi import Cookie, Path, Query


def embedded_json(json: str, *, _id: str | None = None, _class: str | None = None) -> str:
    _id = f'id={_id} ' if _id is not None else ''
    _class = f'class={_class} ' if _class is not None else ''
    return f'<script {_id}{_class}type="application/json">{json}</script>'


def get_user_dict(user: db.User) -> dict[str, Any]:
    return {
        'email': user.email,
        'avatar_url': user.user_info.avatar_url,
    }
