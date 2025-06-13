# 一个轻量、实用的 Python 项目框架（uv 版本）

本项目是一个轻量实用的 Python 项目脚手架，集成了简单的日志，配置文件管理，处理了 python 脚本间的依赖关系，避免重复导入等问题。适用于各种 Python 项目（例如数据科学，web 服务器等）。

项目配置完毕后，你只需要在 src 目录下写代码即可。

之前的 poetry 版本在：[hansenz42/python-project-starter: 一个在 poetry 基础上的 Python 项目脚手架，自带配置文件管理和日志管理功能](https://github.com/hansenz42/python-project-starter)。

针对 poetry 版本，uv 版本更新了：
- 使用 uv 代替 poetry 管理依赖，速度更快！
- 舍弃了将 src 目录视为模块的方式，因为在 pytest 调用时会出现一些错误。为了更好的兼容性，还是使用 src 作为根目录引入代码

# 功能

- 依赖管理：uv
- 日志管理：统一化日志格式，支持正常日志和错误日志的分割，分别输出到 stdout 和 stderr
- 配置文件管理：区分多个配置文件，根据当前运行的环境加载
- 测试管理：pytest

# 使用方法

## 1 安装 uv 依赖管理器：

macOS, Linux, Windows(WSL)：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

其他平台的 uv 安装方式见：[Installation | uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)

## 2 clone 本项目到本地
```bash
git clone git@github.com:hansenz42/python-starter-uv.git
```

## 3 （可选）修改 pyproject 的配置

修改 `pyproject.toml`
```toml
[project]
name = "python-starter-uv"   # 修改项目名称
version = "0.1.0"
description = ""
authors = [{ name = "Hansen", email = "xxxx@xxxx.com" }]    # 填写你的名字和邮箱
requires-python = "~=3.12"    # 修改 python 版本 
readme = "README.md"
dependencies = ["pyyaml", "pytest"] 
```


## 4 切换到项目根目录下，安装依赖，修改项目基本信息
```bash
uv sync
```

## 5 添加项目变量

项目变量的配置在 `res` 目录下，默认提供了三个环境：
- `config_dev.yml` 开发环境：在开发时使用
- `config_test.yml` 测试环境：在测试时使用
- `config_prod.yml` 生产环境：在正式环境中使用

变量可以写到对应环境的配置文件中，如开发环境的变量写到， `res/config_dev.yml`。

`config.yml` 文件是所有环境共用的配置，如果在特定环境中配置了相同名称的变量，则会覆盖 `config.yml` 中的配置。

## 6 开始写代码！

- 你自己的代码可以放在 `src` 目录下。
- 测试用例可以统一放在 `test` 目录下。

### 6.1 引入自己写的模块

引入自己编写的模块时，使用 `src` 作为根目录起始的路径，如：
```python
from src.server.demo_service import foo
```

### 6.2 在代码中引入项目变量

在 `config_xxx.yml` 设置一个项目变量 （xxx 为你要配置的环境）

```yaml
foo: 
  bar: 'test_paramter'
```

可在代码中使用以下方式引入，yaml 中的层级用字符串列表表示：

```python
# 引入 ConfigManager
from src.common.config import config_manager

# 获取 yaml 中配置的变量 foo.bar
try:
    config_str = config_manager.get_value('foo', 'bar')
    # > test_paramter
    print(config_str)
except KeyError:
    # 如未找到该变量，抛出 KeyError 异常
    print('foo.bar 不存在')
```

### 6.3 使用日志

在代码中引入日志：

```python
from src.common.log import log_manager

# 定义一个 Tag
TAG = 'main'

# 使用 Tag 生成一个 logger
log = log_manager.get_logger(TAG)

# 输出日志
log.debug('debug log')
log.info('info log')
log.warning('warning log')
log.error('error log')
```

debug 和 info level 的日志将输出到 stdout，warning 和 error level 的日志将输出到 stderr。

### 6.4 示例

使用了以上功能的示例在 `src/demo.py`。

## 7. 运行

程序将按照顺序指定运行环境： 
1. 环境变量：`PYTHON_SERVICE_ENV` ，如 `PYTHON_SERVICE_ENV=dev uv run python3 main.py`
2. 命令行实参：如 `uv run python3 main.py -e dev`

如果程序没有接收到任何参数，或接受了 dev/test/prod 以外的参数，则默认使用 `dev` 环境。

# 高级使用

## 安装依赖
直接用 uv 安装，会自动修改 `pyproject.toml` 文件

```bash
uv add <package-name>
```

## 修改日志打印到控制台的输出 Level
在 res 文件夹中配置各个环境的日志输出等级（可选）
```yaml
# 配置为 INFO 级别
log_level: INFO  # 支持 DEBUG, INFO, WARNING, ERROR, CRITICAL 不同等级
```

## 加入更多的运行环境

如果运行环境无法满足你的需求，可以在 `src/common/env.py` 文件中的 `VALID_ENVS` 变量中加入你需要的环境名称。

环境名称加入后，在 `res` 目录下新建一个环境配置文件 yaml

## 写测试

测试文件统一放在 test 目录下，文件名以 `test_` 开头，如 `test_main.py`

# 写在最后

该脚手架是我在写 Python 项目时，为了方便自己管理代码而整理的，如果你有更好的建议，欢迎提 issue 或 PR。
