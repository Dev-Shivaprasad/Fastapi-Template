import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = str(os.getenv("JWT_SECRET_PHRASE"))


# Function to generate a JWT
async def generate_jwt(payload, expiration_minutes: int = 30):
    """
    Generates a JSON Web Token (JWT) from a payload.

    Args:
        payload: A dictionary containing the data to be encoded in the token.
        expiration_minutes: The duration in minutes for the token to expire.

    Returns:
        A string representing the JWT, or None if an error occurs.
    """
    try:
        # Add expiration time to the payload
        payload["exp"] = datetime.datetime.now() + datetime.timedelta(
            minutes=expiration_minutes
        )

        # Encode the payload into a JWT
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return None


# Function to verify and decode a JWT
def verify_jwt(token):
    """
    Verifies and decodes a JWT.

    Args:
        token: The JWT string to verify and decode.

    Returns:
        A dictionary containing the decoded payload if successful, or None if an error occurs.
    """
    try:
        # Decode the JWT
        decoded_payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["Ed25519"],
            options={"verify_signature": True, "verify_exp": True},
        )
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidSignatureError:
        print("Invalid token signature")
        return None
    except Exception as e:
        print(f"Error verifying/decoding JWT: {e}")
        return None


# Example Usage
if __name__ == "__main__":
    # Example payload
    payload_data = {
        "user_id": 123,
        "username": "testuser",
        "roles": ["admin", "editor"],
    }

    # Generate the JWT
    jwt_token = generate_jwt(payload_data, expiration_minutes=60)

    if jwt_token:
        print(f"Generated JWT: {jwt_token}")

        # Simulate verifying the token
        decoded_data = verify_jwt(jwt_token)

        if decoded_data:
            print(f"Decoded JWT payload: {decoded_data}")
