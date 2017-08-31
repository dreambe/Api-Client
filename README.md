# Api-Client

<!-- BADGES/ -->
![Python Version](https://img.shields.io/badge/python-3.3%2C%203.4%2C%203.5-blue.svg)

<!-- /BADGES -->
## 简介
python3编写的API测试工具。第三方库用到requests
这次httpclient的设计是参考了locust，在读locust源码的时候，发现它对HTTP客户端的封装方式非常棒，将请求时间、log等封装进去，给我留下了深刻的印象。它主要是，继承第三方库requests，requests.Session类，在子类HttpSession中重新封装了request方法

## 安装
$ pip install requests


## 功能
- 请求
 - [X] get
 - [X] post
 - [X] header
 - [X] put
 - [X] delete

## 特点
 - 允许输入的url带有中文
 - 返回的结果如果是json，格式化输出
 - 返回的结果开头出现BOM、结束出现空格和回车时，提出警告

## 界面
待补充


## 许可
The MIT License (MIT) http://opensource.org/licenses/MIT