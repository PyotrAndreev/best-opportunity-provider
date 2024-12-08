from datetime import datetime, timedelta, UTC
from ipaddress import IPv4Address

from ..base import *


def authorize_user(
    session: Session, credentials: db.serializers.User.Credentials, 
    *, ip: IPv4Address, remember_me: bool,
) -> db.PersonalAPIKey | None:
    """
    :param session: Database session to perform operation on. 
                    If authorization fails, `session` don't have to be rolled back.
    :param credentials: Credentials to perform authorization with.
    :param ip: IP address, from which the authorization request was sent from.
    :param remember_me: Boolean, that impacts an expiry date.

    :returns: `PersonalAPIKey` instance, if authorization succeeded, `None` otherwise.
    """

    user = db.User.login(session, credentials)
    if user is None:
        return
    expiry_date = datetime.now(UTC) + (timedelta(days=365) if remember_me else timedelta(hours=2))
    return db.PersonalAPIKey.generate(session, user, ip, expiry_date)
