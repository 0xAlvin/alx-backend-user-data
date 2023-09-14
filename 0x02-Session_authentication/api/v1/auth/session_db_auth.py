#!/usr/bin/env python3
"""Session module."""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User


class SessionDBAuth(SessionExpAuth):
    """User Session Database Authentication Class."""

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new user session.

        Args:
            user_id (str): The user's ID.

        Returns:
            str: The created session ID, or None if unsuccessful.
        """
        if user_id is None:
            return None
        if not User.search({'id': user_id}):
            return None

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        new_session = UserSession()
        new_session.user_id = user_id
        new_session.session_id = session_id
        new_session.created_at = datetime.now()
        new_session.updated_at = datetime.now()
        try:
            new_session.save()
        except (Exception):
            raise ('session not created')
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user ID associated with a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID, or None if not found or expired.
        """
        sessions = UserSession.search({'session_id': session_id})
        if self.session_duration <= 0:
            return sessions[0].user_id

        created_at_date = sessions[0].created_at
        if created_at_date is None:
            return None

        expiration_time = created_at_date + \
            timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Remove a user's session object.

        Args:
            request: The user's request.

        Returns:
            bool: True if the session was successfully removed,
            False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id:
            session = UserSession.search({'session_id': session_id})
            session.remove()
            return True
        else:
            return False
