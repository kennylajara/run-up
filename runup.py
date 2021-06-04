
class Config(object):
    """Default config of the "Global" args and kwargs."""

    context = '.'
    verbose = False


class DotRunup:
    """
    Handle the `.runup` files.
    
    The `.runup` files are CSV-formated files containeing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """
    pass
