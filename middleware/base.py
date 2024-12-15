from typing import Any, Annotated
from enum import IntEnum

import formatters as fmt
import offer_db as db

from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
