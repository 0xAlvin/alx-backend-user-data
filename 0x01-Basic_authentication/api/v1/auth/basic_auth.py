#!/usr/bin/env python3
"""This module defines the BasicAuth class for basic authentication."""

from typing import TypeVar
from .auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication class.

    This class provides methods for basic authentication, including extracting
    and decoding authorization headers, extracting user credentials, and
    retrieving user objects based on credentials.
    """

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """Extract the base64 portion of an authorization header.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The extracted base64 authorization string,
            or None if not found.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decode a base64 authorization header into a UTF-8 string.

        Args:
            base64_authorization_header (str):
            The base64 authorization header string.

        Returns:
            str: The decoded authorization string, or None if decoding fails.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header
                                    ).decode('utf-8')
        except (Exception):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extract user credentials (username and password)
        from a decoded authorization header.

        Args:
            decoded_base64_authorization_header (str):
            The decoded authorization string.

        Returns:
            tuple: A tuple containing username and password,
            or (None, None) if not found.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        details = decoded_base64_authorization_header.split(':')
        return (details[0], details[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Retrieve a User object based on user credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The User object if found and
            credentials are valid, or None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # Search for users with the provided email
        users_with_email = User.search({'email': user_email})

        if not users_with_email:
            return None

        # Check if the password is valid for the user
        if not users_with_email[0].is_valid_password(user_pwd):
            return None

        return users_with_email[0]  # Return the first user found

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user based on an HTTP request.

        Args:
            request: The HTTP request object.

        Returns:
            TypeVar('User'): The User object if authenticated,
            or None otherwise.
        """
        if request is None:
            return None

        # Call the parent class's current_user method
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

        # Get the user based on the credentials
        user = self.user_object_from_credentials(username, password)

        return user
