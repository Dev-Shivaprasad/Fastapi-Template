from os import getenv
from dotenv import load_dotenv
import re
from bcrypt import gensalt, hashpw, checkpw

# Load environment variables from the .env file
load_dotenv()


def is_valid_email(email: str) -> bool:
    """
    Validate whether the provided email address matches a basic pattern.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email matches the pattern, False otherwise.

    Notes:
        - The regex pattern checks for:
            - Alphanumeric characters, dots, or hyphens before the '@'
            - Alphanumeric domain name parts
            - A dot followed by a valid TLD (e.g., .com, .org)
        - Does not perform deep validation (e.g., MX record lookup).
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def get_env_var(varname: str, default: str = "") -> str:
    """
    Retrieve the value of an environment variable.

    Args:
        varname (str): The name of the environment variable to fetch.
        default (str, optional): A fallback value if the variable is not set. Defaults to "".

    Returns:
        str: The value of the environment variable or the default value if not found.

    Example:
        ```python
        db_url = get_env_var("DATABASE_URL", "sqlite:///default.db")
        ```
    """
    return getenv(varname, default=default)


def is_development():
    """
    Check if the application is running in development mode.

    Returns:
        str | None:
            - Returns `"/docs"` (enabling FastAPI docs) if `DEVELOPMENT` env variable is set to "true".
            - Returns `None` otherwise.

    Example:
        ```python
        # Conditionally expose docs in main.py
        docs_url = is_development()
        app = FastAPI(docs_url=docs_url)
        ```
    """
    return "/docs" if get_env_var("DEVELOPMENT").lower() == "true" else None


async def hashpassword(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    bytepassword = password.encode("utf-8")
    hashedpassword = hashpw(password=bytepassword, salt=gensalt())
    return hashedpassword.decode("utf-8")


async def verifypassword(password: str, hashedpassword: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return checkpw(password.encode("utf-8"), hashedpassword.encode("utf-8"))
