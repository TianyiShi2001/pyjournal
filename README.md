# pyjournal — Journal Article Automatic Download & Management

## Why pyjournal?

Have you been annoyed about...

- logging in journal sites again and again (due to cookie expiry)
- redundant login procedures (find login button (some are hard to find) => find your institution => institution login)
- the links (login, pdf download, citation record) that are hard to find. Consider [JBC](http://www.jbc.org/content/early/2019/10/30/jbc.RA119.009424.abstract). Can you find the citation link?
- new tabs that are forced to open
- renaming downloaded pdfs with readable names

The mission of pyjournal is to subdue these distractions and allow users to focus on their research.

to be completed...

## Availability

### Supported Journals

- Nature (all Journals under Nature Research)
- Elsevier (all Journals under Elsevier)

### Supported Institutions

- University of Oxford

## Contributing

主要有两种方式可以帮助推进这个项目。

1. 在AUTH.py文件中，添加你的单位的登录方法
2. 添加更多的期刊支持。

### 登录方法

首先确定你所在的单位的验证方式（OpenAthens还是Shibboleth），并添加到`AUTH.py`的末尾的`AUTH`字典中。每个键值对的格式为`'<单位全称>': {'<shibboleth/openathens>', <对应的登录函数>}`.

然后写登录函数。
首先确定你所在的单位的验证方式（OpenAthens还是Shibboleth），并添加到`AUTH.py`的末尾的`AUTH`字典中。每个键值对的格式为`'<单位全称>': {'<shibboleth/openathens>', <对应的登录函数>}`.
https://login.openathens.net

一般，要用Selenium模拟登陆。
