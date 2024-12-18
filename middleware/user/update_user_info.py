from ..base import *


def update_user_info(user_info: db.UserInfo, fields: db.serializers.UserInfo.Update) -> None:
    user_info.update(fields)
