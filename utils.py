import json
import io
import sys

# 设置python默认编码为 utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def parse(request_meta, response_meta):
    """
    解析、组装结果返回，将header、body等组装到一起，输出到前端UI
    """
    data = {'errno': 0, 'host_info': '', 'rep_time': '', 'status': '',
            'content_size': '', 'errmsg': '', 'rep_body': object, 'request': ''}

    if request_meta is None:
        data['errno'] = 803
        return data

    # Host Info:
    data['host_info'] = "Host: " + request_meta['host'] + "\n" + "Host-ip: " + request_meta['host-ip'] + "\n\n"

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
    data['rep_time'] += str(response_meta['response_time']) + " ms    "

    # Response Body Size:
    size = round(float(request_meta['content_size']) / 1000, 3)
    data['content_size'] += "Size: " + str(size) + " KB  \n\n"

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
    data['rep_body'], data['errno'] = parse_json(data['rep_body'])

    return data


def parse_json(content):
    try:
        jsoninfo = json.dumps(content, ensure_ascii=False, indent=2)
        errno = 0
    except "UnicodeEncodeError":
        jsoninfo = "解析出错！"
        errno = 802

    return jsoninfo, errno
