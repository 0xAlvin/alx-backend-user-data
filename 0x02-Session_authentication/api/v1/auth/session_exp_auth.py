#!/usr/bin/env python3
"""Session Authentication class"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""

    def __init__(self) -> None:
        """
        Initialize SessionExpAuth.

        Inherits from SessionAuth and sets session_duration attribute based on
        the SESSION_DURATION environment variable.

        :return: None
        """
        super().__init__()

        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (Exception):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session and add it to the user_id_by_session_id dictionary.

        :param user_id: User ID associated with the session.
        :type user_id: str
        :return: Session ID created.
        :rtype: str
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user ID associated with a session ID, considering expiration.

        :param session_id: Session ID to retrieve user ID for.
        :type session_id: str
        :return: User ID associated with the session (if valid), else None.
        :rtype: str
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at_date = session_dict.get('created_at')
        if created_at_date is None:
            return None

        expiration_time = created_at_date + \
            timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get('user_id')
