from os import getenv
from dotenv import load_dotenv

load_dotenv()


def GetEnvVar(varname: str, default: str = "") -> str:
    return getenv(varname, default=default)


def IsDevelopment():
    return "/docs" if GetEnvVar("DEVELOPMENT").strip().lower() == "true" else None
