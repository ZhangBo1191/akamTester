# akamTester

批量测试B站海外CDN（upos-hz-mirrorakam.akamaized.net）节点延迟，找出最低延迟的节点，并将其添加至hosts *(可选)* 。

P.S.  ```ip_list.txt``` 文件用于保存解析出来的ip列表, 当正常解析完成时, 该文件会刷新, 当解析失败时, 会读取该文件中的ip列表。

:warning: 在Win7上需要使用管理员权限运行! :warning:

## 运行

### EXE文件运行

不熟悉Python的用户直接从 [releases](https://github.com/miyouzi/akamTester/releases/latest) 下载exe文件使用。

### 源码运行

安装依赖:

```shell
pip3 install requests beautifulsoup4 lxml termcolor pythonping dnspython
```

执行 ```akamTester.py```

```shell
python3 akamTester.py
```

## 命令行选项

### 指定测试域名

从v3.2开始, 用户可以通过```-u```参数指定测试域名.

举例:

```shell
python3 akamTester.py -u upos-sz-mirrorks3.bilivideo.com
```

### 写入至hosts

从v5.0开始，用户可以通过```-t```或```--to_hosts```参数来决定是否将最快的解析结果写入到hosts里

用例：

```shell
python3 akamTester.py -t
```

## 关于轮子

### GlobalDNS

```GlobalDNS``` 是个对域名进行全球解析的类, 使用 www.whatsmydns.net 的 API 进行解析，额外包含本地、谷歌、腾讯、阿里 DNS 的解析结果。

#### 导入

```python
from GlobalDNS import GlobalDNS
```

#### 例子

```python
akam = GlobalDNS('upos-hz-mirrorakam.akamaized.net')
ip_list = akam.get_ip_list()  # 取得全球解析结果, 返回一个 set
akam.renew()  # 重新解析
ip_list = akam.get_ip_list()  # 将返回最近一次全球解析的结果
```

### ColorPrinter

```ColorPrinter``` 染色输出工具, 可输出红绿及默认颜色(一般终端为白色), 可跨平台, 包括pyCharm中的运行窗口

#### 如何导入

```python
from ColorPrinter import color_print
```

#### 使用

```python
color_print('Hello World')  # 默认输出颜色
color_print('Hello World', status=1)  # 输出红色
color_print('Hello World', status=2)  # 输出绿色
```
