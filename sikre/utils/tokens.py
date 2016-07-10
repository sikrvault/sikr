"""Invitation token generator.

This module generrate the invitation tokens based off a uuid4 web-safe
function.
"""

import uuid

from sikre.models.shares import ShareToken


def generate_token():
    """Generate a unique token.

    Generate a new token based of the HEX version of a UUID and check if it
    already exists. If that's the case generate a new one.
    """
    duplicated = True

    while duplicated:
        try:
            token = uuid.uuid4().hex
            share_token = ShareToken.get(token=token)
            duplicated = True
        except ShareToken.DoesNotExist:
            duplicated = False
            return token
