#!/usr/bin/env python3
"""auth class"""

from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if path is excluded"""
        if path is None or excluded_paths is None:
            return True
        path_with_slash = path if path.endswith('/') else path + '/'

        return path_with_slash not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """checks authorization from header"""
        if request is None or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """checks current user access"""
        return None
