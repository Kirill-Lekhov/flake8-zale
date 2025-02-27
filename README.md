# flake8-zale [![codecov](https://codecov.io/gh/Kirill-Lekhov/flake8-zale/graph/badge.svg?token=6T2V5MTDA7)](https://codecov.io/gh/Kirill-Lekhov/flake8-zale)

This is a plugin for flake8 that allows you to check a lot of things.

## Installation
1. Install from pypi
```shell
pip install flake8-zale
```
2. Validate installation
```shell
flake8 --version
```
You should see `flake8-zale` in the list of installed plugins:
```
<flake8-version> (..., flake8-zale: <version>, ...) CPython 3.8.10 on Linux
```

## Error codes
| Code     | Description                                                    |
|----------|----------------------------------------------------------------|
| `EZL100` | Spaces are used as indents                                     |
| `EZL101` | Parameter indents should be no more than 1 level               |
| `EZL200` | Missing trailing comma in multiline collection                 |
| `EZL300` | Invalid package import order                                   |
| `EZL301` | Invalid formatting of one-line docstring                       |
| `EZL900` | Invalid package import order                                   |
| `EZL900` | Libraries from different sources are imported in one statement |

## Usage
* After installation, the plugin will be automatically applied at each launch;
* If you want to check code only using the plugin, then you should use the `--select` option;
```shell
flake8 --select=EZL
# OR
flake8 --select=EZL100,...,EZL301
```
* If you want to ignore certain errors, then you should use the `--ignore` option;
```shell
flake8 --ignore=EZL
# OR
flake8 --ignore=EZL100,...,EZL301
```
