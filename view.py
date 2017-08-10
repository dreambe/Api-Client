from tkinter import *
from tkinter.ttk import *


class ClientView(object):
    _method = 'GET'
    _check_status = False

    # payload 区域
    _key_entry = []
    _value_entry = []
    _value_del_button = []
    method_row = (_key_entry, _value_entry, _value_del_button)

    # header 区域
    _header_key = []
    _header_value = []
    _header_del_button = []
    header_row = (_header_key, _header_value, _header_del_button)

    _url_entry = object
    _send_button = object
    _header_text = object
    _body_text = object

    def __init__(self, master=None):
        self.root = master
        # 生成控制框架
        self.control_frame()
        # 生成结果框架
        self.result_frame()

    def control_frame(self):
        """
        生成界面上部的控制区域
        """
        url_frame = Frame(self.root)
        method_label = Label(url_frame, text='请求方式：')
        method = Combobox(url_frame, width=5, values=[
                          "GET", "POST", "PUT", "DELETE"], state="readonly")
        method.set("GET")
        url_label = Label(url_frame, text='请求地址：')
        self._url_entry = Entry(url_frame)
        url_frame.pack(side=TOP, fill=X)
        method_label.pack(side=LEFT)
        method.pack(side=LEFT)
        url_label.pack(side=LEFT)
        self._url_entry.pack(side=RIGHT, expand=YES, fill=X)

        # POST参数行
        payload_frame = Frame(self.root)
        payload_frame.pack(side=TOP, fill=X)
        # HEADER参数行
        header_frame = Frame(self.root)
        header_frame.pack(side=TOP, fill=X)
        # 提交按钮行
        send_frame = Frame(self.root)
        check_status = IntVar()
        header = Checkbutton(send_frame, variable=check_status, text="HEADER头信息", width=15,
                             command=(lambda: self.select_header(check_status.get(), header_frame)))
        send_frame.pack(side=TOP, fill=X)
        header.pack(side=LEFT)
        self._send_button = Button(
            send_frame, text="Send", width=10, command=(lambda: self.submit()))
        self._send_button.pack(side=RIGHT)
        # 动作
        method.bind('<<ComboboxSelected>>', (lambda event: self.switch_method(
            method.get(), payload_frame)))

    def result_frame(self):
        """
        生成位于下部的结果区域
        """
        result_frame = Frame(self.root)
        self._header_text = Text(
            result_frame, state="normal", width=1, bg="grey")
        self._body_text = Text(
            result_frame, state="normal", width=1, bg="grey")
        result_frame.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self._header_text.pack(side=LEFT, expand=YES, fill=BOTH)
        self._body_text.pack(side=RIGHT, expand=YES, fill=BOTH)
        # 禁止文本框输入
        self._header_text.bind("<KeyPress>", lambda e: "break")
        self._body_text.bind("<KeyPress>", lambda e: "break")

    def switch_method(self, method_value, payload_frame):
        """
        切换请求方式
        """
        self._method_value = method_value
        if self._method_value == 'GET':
            self.remove_block(payload_frame, self.method_row)
        elif self._method_value == 'POST':
            if not payload_frame.children:
                self.create_block(payload_frame, "POST:", self.method_row)
        else:
            raise ValueError
        # To do
        # 增加其他方法

    def select_header(self, check_status, header_frame):
        """
        选择header 框
        """
        self._check_status = check_status
        if not self._check_status:
            self.remove_block(header_frame, self.header_row)
        elif self._check_status:
            if not header_frame.children:
                self.create_block(header_frame, "HEADER:", self.header_row)

    def add_row(self, payload_frame, row):
        """
        增加一行
        """
        key_entry, value_entry, delete_button = row
        row_value = Frame(payload_frame)
        row_value.pack(side=TOP, fill=X)
        key_label = Label(row_value, text="key:")
        key_label.pack(side=LEFT)
        key = Entry(row_value)
        key.pack(side=LEFT, expand=YES, fill=X)
        value_label = Label(row_value, text="value:")
        value_label.pack(side=LEFT)
        value = Entry(row_value)
        value.pack(side=LEFT, expand=YES, fill=X)
        del_button = Button(row_value, text="删除", width=5, state="disabled")
        del_button.pack(side=RIGHT)
        key_entry.append(key)
        value_entry.append(value)
        delete_button.append(del_button)
        del_button.bind('<ButtonRelease>', (lambda event: self.del_row(payload_frame, event.widget,
                                                                       (key_entry, value_entry, delete_button))))
        self.button_disable(
            payload_frame, (key_entry, value_entry, delete_button))

    def del_row(self, payload_frame, button, row):
        """
        删除一行
        """
        key_entry, value_entry, delete_button = row
        for widget in button.master.children.values():
            widget in key_entry and key_entry.remove(widget)
            widget in value_entry and value_entry.remove(widget)
            widget in delete_button and delete_button.remove(widget)
        button.master.destroy()
        self.button_disable(
            payload_frame, (key_entry, value_entry, delete_button))

    def create_block(self, frame, text, row):
        """
        增加一块区域包括输入框、按钮等
        """
        row_value = Frame(frame)
        row_value.pack(side=TOP, fill=X)
        post_label = Label(row_value, text=text)
        post_label.pack(side=LEFT)
        add_button = Button(row_value, text="增加", width=5,
                            command=(lambda: self.add_row(frame, row)))
        add_button.pack(side=RIGHT)
        self.add_row(frame, row)

    # @staticmethod
    def remove_block(self, frame, row):
        """
        删除一整块区域包括输入框、按钮等
        """
        for v in row:
            v.clear()
        while 1:
            if frame.children:
                frame.children.popitem()[1].destroy()
            else:
                break
        frame.configure(height=1)

    def button_disable(self, payload_frame, row):
        """
        判断删除按钮是否应该禁用
        """
        key_entry, value_entry, delete_button = row
        if len(delete_button) > 1:
            for button in delete_button:
                button.configure(state="normal")
                button.bind('<ButtonRelease>',
                            (lambda event: self.del_row(payload_frame, event.widget,
                                                        (key_entry, value_entry, delete_button))))
        else:
            delete_button[0].configure(state="disabled")
            # 如果不解绑的话，就算禁用也是可以点击。使用按钮的command参数无法返回是哪个按钮点击的。
            delete_button[0].unbind('<ButtonRelease>')

    def submit(self):
        """
        点击提交调用，仅供改写使用
        :return:
        """
        print([self._method, len(self._key_entry), len(self._value_entry), len(self._value_del_button),
               self._check_status, len(self._header_key), len(self._header_value), len(self._header_del_button)])


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


if __name__ == '__main__':

    root = Tk()
    root.title("Api-Client")
    ClientView(master=root)
    center_window(root, 400, 300)
    root.maxsize(1200, 900)
    root.minsize(600, 400)
    root.resizable(True, True)
    root.mainloop()
