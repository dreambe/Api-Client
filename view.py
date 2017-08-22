from tkinter import *
from tkinter.ttk import *
from sys import platform as _platform


class ClientView(Frame):
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
        Frame.__init__(self, master)
        self.root = master
        self.root.title("Api-Client")
        center_window(self.root, 800, 600)
        self.root.minsize(600, 400)
        self.root.resizable(True, True)

        # Linux
        if _platform == "linux" or _platform == "linux2":
            self.root.iconbitmap('./img/Api-Client.xbm')
        # MAC OS X
        elif _platform == "darwin":
            self.root.iconbitmap('./img/Api-Client.xbm')
            # 解决MAC OS 最小化无法打开问题
            self.root.createcommand('tk::mac::ReopenApplication', self.root.deiconify)
        # Windows
        elif _platform == "win32" or _platform == "win64":
            self.root.iconbitmap('./img/Api-Client.ico')
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
        self._url_entry.focus()
        self._url_entry.bind('<Return>', lambda event: self.send())

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
            send_frame, text="Send", width=10, command=(lambda: self.send()))
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
            result_frame, state="normal", width=1,)
        self._body_text = Text(
            result_frame, state="normal", width=1)
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
        self._method = method_value
        if self._method == 'GET':
            self.remove_block(payload_frame, self.method_row)
        elif self._method in {'POST', 'PUT', 'DELETE'}:
            if not payload_frame.children:
                self.create_block(payload_frame, self._method, self.method_row)
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
        self.button_status(
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
        self.button_status(
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
        self._url_entry.focus()

    def button_status(self, payload_frame, row):
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

    def send(self):
        """
        点击提交调用，仅供改写使用
        :return:
        """
        print([self._method, len(self._key_entry), len(self._value_entry), len(self._value_del_button),
               self._check_status, len(self._header_key), len(self._header_value), len(self._header_del_button)])

    @staticmethod
    def remove_block(frame, row):
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

    def start(self):
        self.root.mainloop()


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - width) / 2 - 6
    y = (sh - height) / 2 - 15
    size = '%dx%d+%d+%d' % (width, height, x, y)
    root.geometry(size)


if __name__ == '__main__':
    ClientView(Tk()).start()