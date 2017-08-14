import json


def assemble(request_meta, response_meta):
    """
    组装结果返回，将header、body等组装到一起，输出到前端UI
    """
    data = {'errno': 0, 'rep_time': '', 'status': '', 'errmsg': '', 'rep_body': object, 'request': ''}

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

    # Response status code:
    data['status'] += "Status: " + str(response_meta['status_code']) + "    "

    # Response Time:
    data['rep_time'] += "Time: "
    data['rep_time'] += str(response_meta['response_time']) + " ms \n\n"

    # Response Body:
    try:
        data['rep_body'] = json.loads(response_meta['response_content'].decode('utf-8'))
    except ValueError as e:
        data['rep_body'] = response_meta['response_content'].decode('utf-8')
    except AttributeError as e:
        data['errno'] = 801
        data['rep_body'] = "请求地址有误!"
    # else:
    #     data['errno'] = 1000
    data['rep_body'] = format_json(data['rep_body'])
    return data


def format_json(content):
    jsoninfo = json.dumps(content, ensure_ascii=False, indent=2)
    print(jsoninfo)
    return jsoninfo
