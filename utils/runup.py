
def get_version():
    """Simple function to read RunUp's version"""
    with open('.version') as f:
        return f.read()