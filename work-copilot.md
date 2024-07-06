`cli`使用方式：work-copilot即为l（字母L的小写）

~~~lcmd
l <option> <neccessary_arguments>
~~~

`option`有如下选项：

- 退出：`exit`，`-exit`，`-quit`，`quit`，`-q`

  ~~~bash
  l exit
  ~~~

- 增加别名：`set`，`-set`，`s`

  ~~~bash
  l set <alias> <path>
  ~~~

- 列举所有别名：`ls`，`list`，`-list`

  ~~~bash
  l ls
  ~~~

- 查看版本信息：`-version`，`version`，`v`

  ~~~bash
  l version
  ~~~

- 修改别名的路径：`mf`，`-modify`，`modify`

  ~~~bash
  l mf <alias> <new_path>
  ~~~

- 移除别名：`rm`，`-remove`，`remove`

  ~~~bash
  l rm <alias>
  ~~~

- 标记为（浏览器，编辑器或VPN）：`nt`，`note`，`-note`

  ~~~bash
  l nt <alias> <category(browser,editor,vpn,outer-url)>
  ~~~

- 解除标记（浏览器，编辑器或VPN）：`dnt`，`denote`，`-denote`

  ~~~bash
  l dnt <alias> <category(browser,editor,vpn,outer-url)>
  ~~~

- 重命名别名：`rename`，`-rename`，`rn`

  ~~~bash
  l rename <alias> <new_name>
  ~~~

除了通过命名操作别名和路径外，还可以直接在文件`conf.ini`内修改，需要注意的是key-value形式的别名-路径配置中路径不应该带引号

1. 【Path】存储的所有key-value形式的别名-路径键值对
2. 【Version】版本信息
3. 【InnerUrl】国内网站别名-网址的键值对，打开国内网站不会自动打开VPN
4. 【OutterUrl】国外网站别名-网址键值对，打开国外网站会自动先打开VPN，别名被标记为OutterUrl后会加入到这里
5. 【Editor】编辑器，在别名被标记为编辑器后可以通过追加参数来选择打开的文件/目录
6. 【Browser】浏览器，只有在把别名标记为浏览器之后才可以通过网址别名来快速打开网址，bs为默认浏览器
7. 【Vpn】打开国外网站时会先打开VPN，此时需要有预先的别名被标记为VPN

**使用的前置条件：**

1. 具有python环境，并配置了python环境变量
2. 在系统环境变量中新建变量为COPILOT_HOME，值为work_copilot文件夹路径，并且写到PATH环境变量中



**注意**：所有别名对应的路径不应该带有空格，否则会被命令行错误识别，建议的解决方案是为路径有空格的应用创建快捷方式，剪切快捷方式到一个没有空格的路径下然后复制快捷方式文件地址到`conf.ini`下，值得一提的是复制的路径会带有引号，粘贴到`conf.ini`时注意删除引号





