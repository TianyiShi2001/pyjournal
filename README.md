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

目前这个项目仍处于起步阶段。如果你发现任何地方可以用更好的方法实现，请直接邮件联系我（ tianyi.shi@oriel.ox.ac.uk ).

当此项目的基础框架成熟后，主要有两种方式可以帮助推进这个项目。

1. 在AUTH.py文件中，添加你的单位的登录方法。
2. 添加更多的期刊支持。（创建新的`<期刊>.py`模块）

### 登录方法

使用Selenium模拟登陆。

每种期刊的网页有不同的布局。每个`<期刊>`类要至少要有跳转登录，下载pdf和下载citation这三种方法。根据用户的配置文件，可以决定登录方式是OpenAthens, Shibboleth, 还是直接登录（个人订阅）。随后，通过Selenium找到对应的登录窗口（尤其对于机构登录，selenium是不可或缺的，因为经常需要填搜索框，而且有各种跳转），然后通过登录函数登录。

这些登录函数保存在`AUTH.py`模块中。当用户第一次使用时，或者更新配置文件时，根据用户提供的机构信息，选择出对应的登录函数，并通过用户提供的用户名和密码实例化登录函数，并通过`dill`序列化保存到本地。随后，每次需要登录以取得cookie时，只需要读取这个实例化的登录函数即可。

首先确定你所在的单位的验证方式（OpenAthens还是Shibboleth），并添加到`AUTH.py`的末尾的`AUTH`字典中。每个键值对的格式为`'<单位全称>': {'<shibboleth/openathens>', <对应的登录函数>}`.

然后写登录函数。

https://login.openathens.net


