from django.http import JsonResponse

def api_response(data=None, message=None, status=200, errors=None):
    response = {
        'status': 'success' if status < 400 else 'error',
        'message': message,
        'data': data,
        'errors': errors
    }
    return JsonResponse(response, status=status)