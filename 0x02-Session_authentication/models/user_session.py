#!/usr/bin/env python3
""" session module
"""
from models.base import Base


class UserSession(Base):
    """usersession class"""

    def __init__(self, *args: list, **kwargs: dict):
        """initailizes a session instance"""
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.session_id = None
