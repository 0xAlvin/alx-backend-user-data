#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> str:
    """a function that takes in a password string arguments and returns
    bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """a function that expects 2 arguments and returns a boolean."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
