def get_environment_variable(key):
    """Get environment variable or return None if not found."""
    import os
    import dotenv
    value = os.getenv(key)
    if value is not None:
        return value
    value = dotenv.get_key(dotenv.find_dotenv(), key)
    return value
