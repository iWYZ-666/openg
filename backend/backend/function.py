import json
from django.http.response import JsonResponse



def check_method(method):
    def check_method_decorator(fn):
        def wrap(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({
                    'message': '无法访问此网页',
                }, status=404)
            return fn(request, *args, **kwargs)
        return wrap
    return check_method_decorator


def get_post_json(request):
    json_data = {}
    if request.content_type == 'application/json':
        temp_json_data = json.loads(request.body)
        if temp_json_data:
            json_data = temp_json_data
    elif request.content_type == 'multipart/form-data':
        temp_json_data = request.POST
        if temp_json_data:
            json_data = temp_json_data
    else:
        temp_json_data = json.loads(request.body)
        if temp_json_data:
            json_data = temp_json_data

    return json_data
