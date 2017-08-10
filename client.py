from tkinter import *
import time
import threading
import view
import crawler


class Client(view.ClientView):
    def __init__(self, master=None):
        super(Client, self).__init__()
        self.root = master
        self.test = crawler.Test()

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
        first_time = time.time()
        if self._method == 'GET':
            # 读取参数发送
            header = self.get_dict(self._header_key, self._header_value)
            dict_result = self.test.get(url, header)
        elif self._method == 'POST':
            # 读取参数发送
            post = self.get_dict(self._key_entry, self._value_entry)
            header = self.get_dict(self._header_key, self._header_value)
            dict_result = self.test.post(url, post, header)
        else:
            self._send_button.configure(state="normal", text="提交")
            raise ValueError
        last_time = time.time()
        dict_result['errmsg'] += "\n\n请求时间：" + str(last_time - first_time) + "s"
        self.result(dict_result)
        # 启用提交按钮
        self._send_button.configure(state="normal", text="提交")

    def result(self, dict_result):
        """
        写入结果到UI
        :param dict_result: 需要写入的信息
        :return:None
        """
        self.clear_text()
        if dict_result['error'] == 0:
            pass
        elif dict_result['error'] == 1:
            self._header_text.insert(END, "错误：连接出错\n"
                                          "1.检查输入的地址是否正确\n"
                                          "2.检查输入的POST是否正确\n"
                                          "3.HEADER中不允许有中文字符\n")
        elif dict_result['error'] == 2:
            self._header_text.insert(END, "错误：解析出错\n"
                                          "1.无法解析返回的状态\n")
        elif dict_result['error'] == 3:
            self._header_text.insert(END, "错误：解析出错\n"
                                          "1.无法解析此端口")
        elif dict_result['error'] == 99:
            self._header_text.insert(END, "致命错误：程序出错\n")
        self.insert_text(dict_result)

    @staticmethod
    def get_dict(key, value):
        return dict(zip(map(lambda k: k.get(), key), map(lambda k: k.get(), value)))

    def clear_text(self):
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)

    def insert_text(self, info):

        self._header_text.insert(END, info['info'])
        self._header_text.insert(END, info['msg'] + "\n")
        self._header_text.insert(END, info['errmsg'] + "\n")
        self._body_text.insert(END, info['read'])


if __name__ == '__main__':
    root = Tk()
    root.title("Api-Client")
    Client(master=root)
    root.minsize(800, 600)
    # if platform.system() == "Windows":
    #     root.wm_state('zoomed')
    root.mainloop()
