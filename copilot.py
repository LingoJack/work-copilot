import sys
import os
import time
import config
from urllib.parse import urlparse
from datetime import datetime, timedelta


# 判断是否为网址
def isUrl(path):
    parsed_path = urlparse(path)
    return parsed_path.scheme and parsed_path.netloc


def note_as_editor(option):
    path_list = get_path_list()
    if option not in path_list:
        print("Err: non-existent alias can not be noted as editor")
        sys.exit(1)
    path = get_path(option)
    config.write_to_config("Editor", option, path)
    print("alias {" + option + "} has been noted as editor")


def note_as_browser(option):
    path_list = get_path_list()
    if option not in path_list:
        print("Err: non-existent alias can not be noted as browser")
        sys.exit(1)
    path = get_path(option)
    config.write_to_config("Browser", option, path)
    print("alias {" + option + "} has been noted as browser")


def note_as_vpn(option):
    path_list = get_path_list()
    if option not in path_list:
        print("Err: non-existent alias can not be noted as vpn")
        sys.exit(1)
    path = get_path(option)
    config.write_to_config("Vpn", option, path)
    print("alias {" + option + "} has been noted as vpn")


def note_as_outer_url(alias):
    inner_urls = config.get_all_options(section="InnerUrl")
    outer_urls = config.get_all_options(section="OuterUrl")
    if alias in outer_urls:
        print("alias " + alias + " has been noted as outer url, value: " + get_url(alias)[0])
        sys.exit(1)
    elif alias in inner_urls:
        url = get_url(alias)[0]
        remove_url_alias(alias, False)
        write_outer_url(alias, url)
        print("alias " + alias + " has been noted as outer")
    else:
        print("alias " + alias + " does not exist, please create first")


def denote_browser(alias):
    if alias in get_browser_list():
        config.delete_option(section="Browser", option=alias)
    else:
        print("alias has not been noted as browser yet")
        sys.exit(1)


def denote_editor(alias):
    if alias in get_vpn_list():
        config.delete_option(section="Editor", option=alias)
    else:
        print("alias has not been noted as editor yet")
        sys.exit(1)


def denote_vpn(alias):
    if alias in get_vpn_list():
        config.delete_option(section="Vpn", option=alias)
    else:
        print("alias has not been noted as vpn yet")
        sys.exit(1)


def denote_outer_url(alias):
    outer_urls = config.get_all_options(section="OuterUrl")
    if alias not in outer_urls:
        print("alias " + alias + " has not been noted as outer url yet")
        sys.exit(1)
    else:
        url = get_url(alias)[0]
        remove_url_alias(alias, False)
        write_inner_url(alias, url)
        print("alias " + alias + " has been denoted from outer url")


def remove_editor_alias(alias):
    if alias in get_editor_list():
        config.delete_option(section="Editor", option=alias)
    else:
        return


def remove_browser_alias(alias):
    if alias in get_browser_list():
        config.delete_option(section="Browser", option=alias)
    else:
        return


def remove_vpn_alias(alias):
    if alias in get_vpn_list():
        config.delete_option(section="Vpn", option=alias)
    else:
        return


def get_editor_list():
    options = config.get_all_options("Editor")
    return options


def get_vpn_list():
    options = config.get_all_options("Vpn")
    return options


def get_browser_list():
    options = config.get_all_options("Browser")
    return options


def get_path_list():
    options = config.get_all_options("Path")
    return options


def get_url_list():
    inner_urls = config.get_all_options("InnerUrl")
    outer_urls = config.get_all_options("OuterUrl")
    options = inner_urls + outer_urls
    return options


# 根据option（alias）获得值
def get_path(option):
    return config.read_from_config(section="Path", option=option)


# 获取到一个数组，第一个为option对应的值，第二个为类型 0 墙内 1 墙外 0 非别名链接
def get_url(option):
    # 0国内站点的别名 1海外站点的别名 2网址访问
    inner_urls = config.get_all_options("InnerUrl")
    if option in inner_urls:
        return [config.read_from_config(section="InnerUrl", option=option), 0]
    else:
        outter_urls = config.get_all_options("OuterUrl")
        if option in outter_urls:
            return [config.read_from_config(section="OuterUrl", option=option), 1]
        else:
            return [option, 2]


# 根据option（alias）写入Path下的值，有则修改，无则增加
def write_path(option, value):
    return config.write_to_config(section="Path", option=option, value=value)


def write_inner_url(option, value):
    return config.write_to_config(section="InnerUrl", option=option, value=value)


def write_outer_url(option, value):
    return config.write_to_config(section="OuterUrl", option=option, value=value)


def is_valid_num(argNum, errInfo):
    """
        根据命令行参数个数判断
    """
    name = "l"
    if not len(sys.argv) == argNum:
        if errInfo is not None:
            print("Usage: " + name + " " + errInfo)
        return False
    return True


# Path相关
def add_path_alias(alias, path):
    if alias not in config.get_all_options(section="Path"):
        write_path(alias, path)
        print("Add " + alias + " with path{" + path + "} successfully")
    else:
        print("Err: Alias has existed.Please use '-m' to modify.")


def modify_path_alias(alias, path):
    if alias in config.get_all_options(section="Path"):
        write_path(alias, path)
        print("Set " + alias + " with path{" + path + "} successfully")
    else:
        print("Err: Alias does not exist.Please use '-a' first.")


def remove_path_alias(alias):
    if alias in config.get_all_options(section="Path"):
        path = get_path(alias)
        config.delete_option(section="Path", option=alias)
        print(alias + " has been deleted from path: " + path)
    else:
        print("Err: Alias does not exist.")


def rename_path_alias(alias, new_name):
    if new_name in command:
        print("Err: new name can not be repeated with the command")
        sys.exit(1)
    config.rename_option("Path", alias, new_name)
    if alias in config.get_all_options(section="Editor"):
        config.rename_option("Editor", alias, new_name)
    if alias in config.get_all_options(section="Vpn"):
        config.rename_option("Vpn", alias, new_name)
    if alias in config.get_all_options(section="Browser"):
        config.rename_option("Browser", alias, new_name)
    print("Renamed " + alias + " by " + new_name + " successfully")


# Url相关
def add_url_alias(alias, url):
    if ((alias not in config.get_all_options(section="InnerUrl"))
            and (alias not in config.get_all_options(section="OuterUrl"))):
        write_inner_url(alias, url)
        print("Add " + alias + " with url{" + url + "} successfully")
    else:
        print("Err: Alias has existed.Please use '-m' to modify.")


def remove_url_alias(alias, feedback=True):
    if alias in config.get_all_options(section="InnerUrl"):
        config.delete_option(section="InnerUrl", option=alias)
        if feedback:
            print("Remove " + alias + " from InnerUrl successfully")
    elif alias in config.get_all_options(section="OuterUrl"):
        config.delete_option(section="OuterUrl", option=alias)
        if feedback:
            print("Remove " + alias + " from OuterUrl successfully")
    else:
        if feedback:
            print("Err:this url alias does not exist")


def rename_url_alias(alias, new_name):
    if alias in config.get_all_options(section="InnerUrl"):
        config.rename_option(section="InnerUrl", old_option=alias, new_option=new_name)
        print("Renamed inner url {" + alias + "} by" + new_name + " successfully")
    elif alias in config.get_all_options(section="OuterUrl"):
        config.rename_option(section="OuterUrl", old_option=alias, new_option=new_name)
        print("Renamed outer url {" + alias + "} by" + new_name + " successfully")
    else:
        print("Err: alias does not exist")


# 展示版本信息
def show_version_info():
    version = config.read_from_config(section="Version", option="version")
    print("work copilot version: " + version)
    print("author: " + "lingojack")
    print("email: " + "3065225677@qq.com")


# 判断是否已经存在路径别名
def has_path_alias(alias):
    if alias not in get_path_list():
        print("Alias '{}' does not exist.".format(alias))
        return False
    return True


def has_alias(section, option):
    if option not in config.get_all_options(section=section):
        return False
    return True


# 绘制分割线
def printLine():
    print("----------------------------------------")


# 展示alias
def list_all_alias():
    printLine()
    list_path_alias()
    list_url_alias()
    list_editor_alias()
    list_browser_alias()
    list_vpn_alias()


def list_editor_alias():
    options = config.get_all_options("Editor")
    if len(options) != 0:
        print("[Editor]")
        for option in options:
            print(option + "    " + get_path(option))
    else:
        print("No alias")
    printLine()


def list_browser_alias():
    options = config.get_all_options("Browser")
    if len(options) != 0:
        print("[Browser]")
        for option in options:
            print(option + "    " + get_path(option))
    else:
        print("No alias")
    printLine()


def list_vpn_alias():
    options = config.get_all_options("Vpn")
    if len(options) != 0:
        print("[Vpn]")
        for option in options:
            print(option + "    " + get_path(option))
    else:
        print("No alias")
    printLine()


def list_url_alias():
    options = config.get_all_options("InnerUrl")
    if len(options) != 0:
        print("[Url]")
        for option in options:
            print(option + "    " + get_url(option)[0])
    options = config.get_all_options("OuterUrl")
    if len(options) != 0:
        for option in options:
            print(option + "    " + get_url(option)[0])
    else:
        print("No alias")
    printLine()


def list_path_alias():
    options = config.get_all_options("Path")
    if len(options) != 0:
        print("[Path]")
        for option in options:
            print(option + "    " + get_path(option))
    else:
        print("No alias")
    printLine()


# handle
def handle_other(arg1):
    if is_valid_num(2, "alias") and has_path_alias(arg1):
        path = get_path(arg1)
        print("start application : {" + path + "}")
        os.system("start " + path)


def handle_editor(arg1):
    if is_valid_num(3, None):
        path = get_path(arg1)
        argv2 = sys.argv[2]
        os.system("start " + path + " " + argv2)
        print("start application : {" + path + "}")
    else:
        if is_valid_num(2, "alias") and has_path_alias(arg1):
            path = get_path(arg1)
            print("start application : {" + path + "}")
            os.system("start " + path)


def handle_browser(arg1):
    if is_valid_num(2, None):
        path = get_path(arg1)
        print("start application : {" + path + "}")
        os.system("start " + path)
    elif is_valid_num(3, "bs url"):
        path = get_path(arg1)
        arg2 = sys.argv[2]
        url_info = get_url(arg2)
        url = url_info[0]
        url_type = url_info[1]
        # 0 国内 1 海外 3 链接
        if url_type == 1:
            vpn_list = get_vpn_list()
            vpn_alias = vpn_list[0]
            vpn_path = get_path(vpn_alias)
            print("opening VPN...")
            os.system("start " + vpn_path)
            time.sleep(2)
        elif url_type == 2:
            os.system("start " + path + " " + url)
        print("start {" + url + "} with application : {" + path + "}")
        os.system("start " + path + " " + url)


def handle_remove_path():
    if is_valid_num(3, "-r alias path"):
        alias = sys.argv[2]
        if has_alias("Path", alias):
            remove_path_alias(alias)
            remove_editor_alias(alias)
            remove_browser_alias(alias)
            remove_vpn_alias(alias)
        else:
            remove_url_alias(alias)


def handle_modify_path():
    if is_valid_num(4, "-m alias path"):
        alias = sys.argv[2]
        path = sys.argv[3]
        modify_path_alias(alias, path)


def handle_show_version():
    if is_valid_num(2, "-v"):
        show_version_info()


def handle_list():
    if is_valid_num(2, "-l"):
        list_all_alias()


def handle_set():
    if is_valid_num(4, "set alias path"):
        alias = sys.argv[2]
        if alias in command:
            print("set alias fail: alias can not be the same as command")
            sys.exit(1)
        path = sys.argv[3]
        # 判断是否为网址
        if isUrl(path):
            # 如果存在 scheme 和 netloc，说明是一个网址
            add_url_alias(alias, path)
        else:
            # 否则，认为是本地路径
            add_path_alias(alias, path)


def handle_exit():
    if is_valid_num(2, "exit"):
        print("Bye~")
        sys.exit(0)


def handle_help():
    try:
        # 获取 COPILOT_HOME 环境变量
        copilot_home = os.getenv("COPILOT_HOME")

        # 检查环境变量是否存在
        if copilot_home is None:
            print("COPILOT_HOME 环境变量未设置。")
            return

        # 生成 help.txt 的完整路径
        help_file_path = os.path.join(copilot_home, "help.txt")

        # 打开并读取 help.txt 文件
        with open(help_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"help.txt 文件未找到: {help_file_path}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")


def handle_denote_path():
    if is_valid_num(4, "dnt alias category(browser,editor,vpn,outer-url)"):
        alias = sys.argv[2]
        category = sys.argv[3]
        if category == "browser":
            denote_browser(alias)
        elif category == "editor":
            denote_editor(alias)
        elif category == "vpn":
            denote_vpn(alias)
        elif category == "outer-url":
            denote_outer_url(alias)
        else:
            print("Usage: l note alias category(browser,editor,vpn)")


def handle_note_path():
    if is_valid_num(4, "nt alias category(browser,editor,vpn,outer-url)"):
        alias = sys.argv[2]
        category = sys.argv[3]
        if category == "browser":
            note_as_browser(alias)
        elif category == "editor":
            note_as_editor(alias)
        elif category == "vpn":
            note_as_vpn(alias)
        elif category == "outer-url":
            note_as_outer_url(alias)
        else:
            print("Usage: l nt alias category(browser,editor,vpn,outer-url)")


def handle_rename_path():
    if is_valid_num(4, "rename alias new_name"):
        alias = sys.argv[2]
        new_name = sys.argv[3]
        if alias in get_path_list():
            rename_path_alias(alias, new_name)
        elif alias in get_url_list():
            rename_url_alias(alias, new_name)


def get_fixed_dates():
    """获取固定的开始和结束日期"""
    # 获取当前日期
    current_date = datetime.now()
    start_date = current_date
    end_date = start_date + timedelta(days=6)  # 往后六天

    # 将日期格式化为"YYYY.MM.DD"
    start_date_str = start_date.strftime('%Y.%m.%d')
    end_date_str = end_date.strftime('%Y.%m.%d')

    return start_date_str, end_date_str


def handle_report():
    # 从配置文件读取路径和周数，使用 'utf-8' 编码
    try:
        path = config.read_from_config("Report", "week-report").encode('utf-8').decode('utf-8', errors='replace')
        week_num = int(config.read_from_config("Report", "week_num").encode('utf-8').decode('utf-8', errors='replace'))
    except Exception as e:
        print(f"Error: 读取配置时出错: {e}")
        return

    # 输出路径检查
    print(f"从配置文件读取到的路径: {path}")

    # 规范化路径
    path = os.path.normpath(path)

    # 检查路径是否存在
    if not os.path.exists(os.path.dirname(path)):
        print(f"Error: 路径不存在，未创建目录: {os.path.dirname(path)}")
        return

    # 获取命令行的第2个参数作为要写入的内容
    if len(sys.argv) > 2:
        content = sys.argv[2].strip()
    else:
        print("Error: 请提供需要写入的内容。")
        return

    # 判断参数是否为"new"
    if content.lower() == "new":
        start_date_str, end_date_str = get_fixed_dates()
        report_content = f"# Week{week_num}[{start_date_str}-{end_date_str}]\n"
        config.write_to_config("Report", "last_day", end_date_str)

        # 更新周数并写回配置
        try:
            config.write_to_config("Report", "week_num", str(week_num + 1))
            print(f"已将周数更新为 {week_num + 1} 并写回配置文件。")
        except Exception as e:
            print(f"Error: 无法更新配置: {e}")
    else:
        # 获取当前日期，并格式化为"YYYY/MM/DD"
        now = datetime.now()
        last_day_str = config.read_from_config("Report", "last_day")
        last_day = datetime.strptime(last_day_str, "%Y.%m.%d")
        if now > last_day:
            start_date_str, end_date_str = get_fixed_dates()
            report_content = f"# Week{week_num}[{start_date_str}-{end_date_str}]\n"
            config.write_to_config("Report", "last_day", end_date_str)
            # 更新周数并写回配置
            try:
                config.write_to_config("Report", "week_num", str(week_num + 1))
                print(f"已将周数更新为 {week_num + 1} 并写回配置文件。")
            except Exception as e:
                print(f"Error: 无法更新配置: {e}")
            write_to_markdown(path, report_content)
        current_date = now.strftime('%Y/%m/%d')
        report_content = f"- {current_date} {content}\n"

    # 调用写入函数，将内容写入指定路径
    write_to_markdown(path, report_content)


def write_to_markdown(file_path, content):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)  # 直接写入内容
        print(f"已成功将内容写入 {file_path}")
    except Exception as e:
        print(f"Error: 无法写入文件: {e}")


exitCommands = ["exit", "-q", "quit", "-quit", "-exit"]
addCommands = ["set", "-set", "s"]
listCommands = ["ls", "list", "-list"]
versionCommands = ["-version", "version", "v"]
modifyCommands = ["mf", "-modify", "modify"]
removeCommands = ["rm", "-remove", "remove"]
noteCommands = ["nt", "-note", "note"]
denoteCommands = ["dnt", "denote", "-denote"]
renameCommands = ["rename", "-rename", "rn"]
helpCommands = ["help", "-help", "-h"]
reportCommands = ["-r", "report", "-report", "r"]
command = (exitCommands + addCommands + listCommands + versionCommands + modifyCommands + removeCommands + noteCommands
           + denoteCommands + renameCommands + helpCommands + reportCommands)
# todo 增加一个翻译的后台命令
translate = []


def main():
    # 检查参数数量
    if not (len(sys.argv) == 4 or len(sys.argv) == 2 or len(sys.argv) == 3):
        print("Usage: wrong arguments~  now argument number:{}".format(len(sys.argv)))
        sys.exit(1)

    # 获取参数
    arg1 = sys.argv[1]

    if arg1 in exitCommands:
        handle_exit()
    if arg1 in helpCommands:
        handle_help()
    elif arg1 in addCommands:
        handle_set()
    elif arg1 in listCommands:
        handle_list()
    elif arg1 in versionCommands:
        handle_show_version()
    elif arg1 in modifyCommands:
        handle_modify_path()
    elif arg1 in removeCommands:
        handle_remove_path()
    elif arg1 in noteCommands:
        handle_note_path()
    elif arg1 in denoteCommands:
        handle_denote_path()
    elif arg1 in reportCommands:
        handle_report()
    elif arg1 in renameCommands:
        handle_rename_path()
    elif arg1 in get_browser_list():
        handle_browser(arg1)
    elif arg1 in get_editor_list():
        handle_editor(arg1)
    else:
        handle_other(arg1)


if __name__ == "__main__":
    main()
