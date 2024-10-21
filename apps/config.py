# config.py

def load_config():
    """
    This function loads the configuration settings for the application.
    You can modify it to load from a file (e.g., JSON, YAML) or environment variables.
    """
    config = {
        'db_host': 'localhost',
        'db_port': 5432,
        'debug_mode': True,
        'max_retries': 5,
    }
    print("Configuration loaded:", config)
    return config
