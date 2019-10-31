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

传统的下载/整理期刊文章的方法有不少麻烦事儿，它们使我写作业的体验变得很不愉快：

- 当cookie过期时，要重新手动登录。这可能会很麻烦，尤其是对于机构登录（你经常需要跳转两三次，然后填一个机构名称搜索框，再跳转到机构的登录页面登录）。
- 有些网站的pdf/citation的下载链接藏得很深。看看[JBC](http://www.jbc.org/content/early/2019/10/30/jbc.RA119.009424.abstract)文章的界面，你能找到它的citation下载吗？
- 有些网站下载pdf是右键直接保存，有些必须要打开一个新页面，然后另存为。这经常很烦。
- 下载的pdf文件名通常是一堆毫无意义的数字。你经常需要为它们重命名一个正常的名字——如果你用bibtex，你一定会使它的名字和cite-key一样，方便查找。然后，你需要一个个把它们移到你当前项目的工作文件夹。
- 你需要把citation文件一个个拖到你的citation管理应用中。然后删除它们。

为了能够愉快的写作业，我开发了`pyjournal`来解决这些问题。

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


