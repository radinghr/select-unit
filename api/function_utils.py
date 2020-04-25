# from rest_framework.authentication import get_authorization_header
from api.jwt_utils import extract_jwt_payload


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_TOKEN', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode()
    return auth


def get_token(request):
    try:
        token = get_authorization_header(request)
        extracted_token = extract_jwt_payload(token)[0]
        error = extracted_token.get("err")
        if error is not None:
            return None, error
        return extracted_token.get("username"), None
    except Exception as e:
        return None, str(e)
