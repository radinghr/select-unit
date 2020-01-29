from rest_framework.authentication import get_authorization_header
from api.jwt_utils import extract_jwt_payload


def get_token(request):
    try:
        auth_keyword, token = get_authorization_header(request).split()
        extracted_token = extract_jwt_payload(token)[0]
        error = extracted_token.get("err")
        if error is not None:
            return None, error
        return extracted_token.get("username"), None
    except Exception as e:
        return None, str(e)
