from os import getenv
from dotenv import load_dotenv
import re

load_dotenv()


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def GetEnvVar(varname: str, default: str = "") -> str:
    return getenv(varname, default=default)


def IsDevelopment():
    return "/docs" if GetEnvVar("DEVELOPMENT").strip().lower() == "true" else None
