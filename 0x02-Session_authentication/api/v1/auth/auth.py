#!/usr/bin/env python3
"""Authentication class"""

from typing import List, TypeVar


class Auth:
    """
    Authentication class.

    This class provides basic authentication functionality, including methods
    for checking if authentication is required, extracting the authorization
    header from an HTTP request, and checking the current user's access.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for a given path.

        Args:
            path (str): The path of the resource being accessed.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication.

        Returns:
            bool: True if authentication is required, False if the path
            is excluded.
        """
        if path is None or excluded_paths is None:
            return True
        path_with_slash = path if path.endswith('/') else path + '/'
        excluded_path = [x.rstrip('*')
                         for x in excluded_paths if x.endswith('*')]
        for exclude in excluded_path:
            if path.startswith(exclude):
                return False

        return path_with_slash not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Extract the Authorization header from an HTTP request.

        Args:
            request: The HTTP request object.

        Returns:
            str: The value of the Authorization header, or None if not found.
        """
        if request is None or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Check the access of the current user based on an HTTP request.

        Args:
            request: The HTTP request object.

        Returns:
            TypeVar('User'): The User object if authenticated, or None if
            not authenticated.
        """
        return None
