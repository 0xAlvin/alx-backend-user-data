#!/usr/bin/env python3
"""basic auth class"""
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except (Exception):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        details = decoded_base64_authorization_header.split(':')
        return (details[0], details[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users_with_email = User.search({'email': user_email})

        if not users_with_email:
            return None

        if not users_with_email[0].is_valid_password(user_pwd):
            return None

        return users_with_email[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        if request is None:
            return None

        user = super().current_user(request)

        if user is not None:
            return user

        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        base64_credentials = self.extract_base64_authorization_header(
            auth_header)

        if base64_credentials is None:
            return None

        credentials = self.decode_base64_authorization_header(
            base64_credentials)

        if credentials is None:
            return None

        username, password = self.extract_user_credentials(credentials)

        if username is None or password is None:
            return None

        user = self.user_object_from_credentials(username, password)

        return user
