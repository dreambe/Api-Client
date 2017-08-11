import json


def assemble(request_meta, response_meta):
    """
    组装结果返回，将header、body等组装到一起，输出到前端UI
    """
    data = {'errno': 0, 'rep_time': 0, 'errmsg': '', 'rep_body': '', 'request': ''}

    # Request Headers:
    data['request'] = "Request Headers: \n"
    for k in request_meta['request_headers']:
        data['request'] += k + ": " + request_meta['request_headers'][k] + "\n"
    data['request'] += "\n"

    # Response Headers:
    data['request'] += "Response Headers: \n"
    for k in response_meta['response_headers']:
        data['request'] += k + ": " + response_meta['response_headers'][k] + "\n"
    data['request'] += "\n"

    data['rep_time'] += "Response Time: \n"
    data['rep_time'] += response_meta['response_time'] + 's'
    # Response Body:
    data['rep_body'] += "Response Body: \n"
    data['rep_body'] += str(json.loads(response_meta['response_content'].decode('utf-8')))

    return data
