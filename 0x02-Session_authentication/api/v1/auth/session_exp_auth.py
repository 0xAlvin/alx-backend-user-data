#!/usr/bin/env python3
"""Session Authentication class"""

from datetime import datetime, timedelta
from auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""

    session_dictionary = {}

    def __init__(self) -> None:
        """
        Initialize SessionExpAuth.

        Inherits from SessionAuth and sets session_duration attribute based on
        the SESSION_DURATION environment variable.

        :return: None
        """
        super().__init__()

        self.session_duration
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
        try:
            session_id = super().create_session(user_id)
            user_id = self.user_id_for_session_id(session_id)
            self.session_dictionary['user_id'] = user_id
            self.session_dictionary['created_at'] = datetime.now()
            self.user_id_by_session_id[session_id] = self.session_dictionary
            return session_id
        except (Exception):
            return None

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
        if not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.session_dictionary.get('user_id')
        if not self.session_dictionary.get('created_at'):
            return None
        created_at = datetime(self.session_dictionary.get('created_at'))
        session_dur = timedelta(seconds=self.session_duration)
        if created_at + session_dur < datetime.now():
            return None
        return super().user_id_by_session_id(session_id)
