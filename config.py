# 配置文件
import configparser
import os

# 获取环境变量 COPILOT_HOME 的值
copilot_home = os.getenv('COPILOT_HOME')

if copilot_home is None:
    raise EnvironmentError("Environment variable COPILOT_HOME is not set.")

# 拼接配置文件路径
config_file = os.path.join(copilot_home, 'conf.ini')
if not os.path.exists(config_file):
    raise FileNotFoundError(f"Configuration file 'conf.ini' not found in the directory specified by COPILOT_HOME "
                            f"environment variable: {copilot_home}")


# 从配置文件动态获取信息
def read_from_config(section, option):
    config = configparser.ConfigParser()
    config.read(config_file)
    res = config.get(section, option)
    return res


def write_to_config(section, option, value):
    config = configparser.ConfigParser()

    # 读取现有的配置文件，以便我们可以修改它
    if os.path.exists(config_file):
        config.read(config_file)

    # 确保 section 存在，如果不存在则创建它
    if not config.has_section(section):
        config.add_section(section)
    # 写入值到指定的 section 和 option
    config.set(section, option, str(value))
    # 将修改后的配置写回到文件
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def get_all_options(section):
    config = configparser.ConfigParser()
    config.read(config_file)
    if config.has_section(section):
        return config.options(section)
    else:
        return []


def delete_option(section, option):
    config = configparser.ConfigParser()

    # 读取现有的配置文件，以便我们可以修改它
    if os.path.exists(config_file):
        config.read(config_file)

    # 确保 section 存在，如果不存在则创建它
    if not config.has_section(section):
        config.add_section(section)

    # 删除指定的 option
    if config.has_option(section, option):
        config.remove_option(section, option)

    # 将修改后的配置写回到文件
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def rename_option(section, old_option, new_option):
    config = configparser.ConfigParser()

    # 读取现有的配置文件，以便我们可以修改它
    if os.path.exists(config_file):
        config.read(config_file)

    # 确保 section 存在，如果不存在则创建它
    if not config.has_section(section):
        config.add_section(section)

    # 获取旧的值
    if config.has_option(section, old_option):
        old_value = config.get(section, old_option)
    else:
        raise ValueError(f"Option '{old_option}' does not exist in section '{section}'")

    # 删除旧的 option
    config.remove_option(section, old_option)

    # 设置新的 option
    config.set(section, new_option, old_value)

    # 将修改后的配置写回到文件
    with open(config_file, 'w') as configfile:
        config.write(configfile)
