from tkinter import *
import threading
import json

import utils
import view
import httpclient


class Client(view.ClientView):
    """docstring for  Client"view.ClientView def __init__(self, arg):
        super( Client,view.ClientView.__init__()
        self.arg = arg
    """

    def __init__(self, master=None):
        super(Client, self).__init__()
        self.root = master
        self.test = httpclient.HttpSession()

    def submit(self):
        """
        点击提交按钮创建新线程
        :return:None
        """
        # 禁用提交按钮
        self._send_button.configure(state="disabled", text="提交中")
        # 启动线程
        t = threading.Thread(target=self.submit_event)
        t.setDaemon(True)
        t.start()

    def submit_event(self):
        """
        提交请求
        :return:None
        """
        url = self._url_entry.get()
        # 地址开头没有http:自动加上http://
        if url.find("http"):
            self._url_entry.insert(0, "http://")
            url = "http://" + url

        request_meta, response_meta = self.test.request("get", url)

        print('request_headers \n', request_meta['request_headers'])
        print('request_body \n', request_meta['request_body'])
        # print('request_content \n', request_meta['request_content'])

        print('response_time \n', response_meta['response_time'])
        print('status_code \n', response_meta['status_code'])
        print('response_headers \n', response_meta['response_headers'])
        print('response_content \n', response_meta['response_content'])

        # response_meta['response_content']['errmsg'] += "\n\n请求时间：" + str(response_meta['response_time']) + "s"
        # result_data = json.loads(response_meta['response_content'].decode('utf-8'))
        result_data = utils.assemble(request_meta, response_meta)
        self.result(result_data)
        # 启用提交按钮
        self._send_button.configure(state="normal", text="提交")

    def result(self, result_data):
        """
        写入结果到UI
        :param result_data: 需要写入的信息
        :return:None
        """
        print(result_data)
        self.clear_text()
        if result_data['errno'] == 0:
            pass
        elif result_data['errno'] == 1:
            self._header_text.insert(END, "错误：连接出错\n"
                                          "1.检查输入的地址是否正确\n"
                                          "2.检查输入的POST是否正确\n"
                                          "3.HEADER中不允许有中文字符\n")
        elif result_data['errno'] == 2:
            self._header_text.insert(END, "错误：解析出错\n"
                                          "1.无法解析返回的状态\n")
        elif result_data['errno'] == 3:
            self._header_text.insert(END, "错误：解析出错\n"
                                          "1.无法解析此端口")
        elif result_data['errno'] == 99:
            self._header_text.insert(END, "致命错误：程序出错\n")
        self.insert_text(result_data)

    @staticmethod
    def get_dict(key, value):
        return dict(zip(map(lambda k: k.get(), key), map(lambda k: k.get(), value)))

    def clear_text(self):
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)

    def insert_text(self, result_data):

        self._header_text.insert(END, result_data['request'])
        # self._header_text.insert(END, result_data['msg'] + "\n")
        self._header_text.insert(END, result_data['errmsg'] + "\n")
        # self._body_text.insert(END, result_data['read'])
        self._body_text.insert(END, result_data['rep_body'])


if __name__ == '__main__':
    root = Tk()
    root.title("Api-Client")
    Client(master=root)
    root.minsize(800, 600)
    # if platform.system() == "Windows":
    #     root.wm_state('zoomed')
    root.mainloop()
