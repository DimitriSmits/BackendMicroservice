"""
This module contains functions for performing the env files checks.
"""

import json
import os
from typing import Any, Optional


def get_json_env(name: str, default: Optional[Any] = None) -> Any:
    try:
        value = os.environ[name]
    except KeyError:
        if default is not None:
            value = json.dumps(default)
        else:
            raise KeyError(f'Could not find env variable "{name}" and no default was provided')

    try:
        return json.loads(value)
    except json.decoder.JSONDecodeError:
        # Since Docker Compose v1.26, strings are interpreted so quotes are no longer maintained
        value = value.replace('\n', '\\n').replace('\r', '\\r')
        return json.loads(f'"{value}"')
