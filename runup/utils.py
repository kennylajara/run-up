# Built-in
from typing import Any, Optional

# 3rd party
from click import echo


def vInfo(verbose:bool, msg:str) -> None:
    """Print verbose Info"""
    if verbose:
        echo(f'Info: {msg}')


def vCall(verbose:bool, func:str) -> None:
    """Print verbose Call"""
    if verbose:
        echo(f'Call: {func}')


def vResponse(verbose:bool, func:str, res:Optional[Any]) -> None:
    """Print verbose Response"""
    if verbose:
        echo(f'Response: {func} => {res}')
