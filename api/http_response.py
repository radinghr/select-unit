import json
from django.http import HttpResponse
from . import utils


def bad_request_response(message="Bad request", status=False, code=400):
    data = {
        'success': status,
        'err_msg': message,
    }
    content = {
        'data': data,
        'StatusCode': code,
    }
    return HttpResponse(json.dumps(content),
                        content_type="application/json",
                        status=code)


def not_found_response(message="Not found", status=False, code=404):
    data = {
        'success': status,
        'err_msg': message,
    }
    content = {
        'data': data,
        'StatusCode': code,
    }
    return HttpResponse(json.dumps(content),
                        content_type="application/json",
                        status=code)


def un_auth_response(message="Authentication failed", status=False, code=403):
    data = {
        'success': status,
        'err_msg': message,
    }
    content = {
        'data': data,
        'StatusCode': code,
    }
    return HttpResponse(json.dumps(content),
                        content_type="application/json",
                        status=code)


def not_acceptable_response(message="Not Acceptable", status=False, code=406):
    data = {
        'success': status,
        'err_msg': message,
    }
    content = {
        'data': data,
        'StatusCode': code,
    }
    return HttpResponse(json.dumps(content),
                        content_type="application/json",
                        status=code)


def success_response(data):
    result = dict()
    result['data'] = data
    result['StatusCode'] = 200
    json_data = json.dumps(result)
    return HttpResponse(json_data,
                        content_type='application/json',
                        status=200)


def error_response(st_code):
    if st_code == utils.NOT_MATCH_ERR:
        return not_acceptable_response(message="Sent data does not match.")
    if st_code == utils.MAJOR_NOT_FOUND:
        return not_acceptable_response(message="Major id you are given is not found.", code=404)

    else:
        return not_acceptable_response("Oops. Something went wrong.")
