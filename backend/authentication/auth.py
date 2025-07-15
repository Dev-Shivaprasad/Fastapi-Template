import jwt
import datetime
from utils.helperfunctions import GetEnvVar

SECRET_KEY = str(GetEnvVar("JWT_SECRET_PHRASE"))


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
def verify_jwt(token: str) -> dict:
    """
    A dictionary containing the status and statement on both success or unsuccess
    """
    try:
        # Decode the JWT
        decoded_payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_signature": True, "verify_exp": True},
        )
        return {
            "status": True,
            "statement": "Token is valid",
            "payload": decoded_payload,
        }
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return {"status": False, "statement": "Token has expired"}
    except jwt.InvalidSignatureError:
        print("Invalid token signature")
        return {"status": False, "statement": "Invalid token signature"}
    except Exception as e:
        print(f"Error verifying/decoding JWT: {e}")
        return {"status": False, "statement": f"Error verifying/decoding JWT: {e}"}


# # Example Usage
# if __name__ == "__main__":
#     # Example payload
#     payload_data = {
#         "user_id": 123,
#         "username": "testuser",
#         "roles": ["admin", "editor"],
#     }

#     # Generate the JWT
#     jwt_token = generate_jwt(payload_data, expiration_minutes=60)

#     if jwt_token:
#         print(f"Generated JWT: {jwt_token}")

#         # Simulate verifying the token
#         # decoded_data = verify_jwt(jwt_token)

#         if decoded_data:
#             print(f"Decoded JWT payload: {decoded_data}")
