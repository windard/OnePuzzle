# A Puzzle A Day

[![Build Status](https://img.shields.io/travis/windard/OnePuzzle)](https://travis-ci.com/github/windard/OnePuzzle)
[![Total Lines](https://img.shields.io/tokei/lines/github/windard/OnePuzzle)](https://github.com/windard/OnePuzzle)
[![codecov](https://codecov.io/gh/windard/OnePuzzle/branch/master/graph/badge.svg?token=JKFqVmzvLm)](https://codecov.io/gh/windard/OnePuzzle)
[![MIT](https://img.shields.io/github/license/windard/OnePuzzle)](https://github.com/windard/OnePuzzle/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/OnePuzzle)](https://pypi.org/project/OnePuzzle/)
[![Author](https://img.shields.io/badge/author-windard-359BE1)](https://windard.com)

一天一个谜，一个谜一天

## install

```
pip install OnePuzzle
```

## usage

```
$ one_puzzle -h
Usage: one_puzzle [OPTIONS] MONTH DAY

Options:
  -h, --help         Show this message and exit.
  -v, --version      Show the version and exit.
  -d, --debug        show debug message.
  -a, --all          get all result.
  -n, --nox          no screen show.
  -c, --color        colorful cli show.
  -r, -u, --urandom  random calculate.
```

## example

**Qt 打印结果**

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/uTools_1633677947082.png)

**Rich 打印结果**

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/1638323759327.png)

**命令行输出结果**

```
$ one_puzzle 12 1 -n
 +  +  +  +  $  $
 *  *  *  +  $
    #  *  $  $  %  %
 #  #  *  ^  ^  ^  %
 #  #  ^  ^  &  %  %
 @  @  @  &  &  &  &
 @  @  @
```

## changelog

- 0.1.0: 功能基本完成
- 0.1.1: 小的修复升级
- 0.2.0: 减少遍历次数，加快解谜速度
- 0.2.1: 增加测试，删减无用代码
- 0.2.2: 增加随机参数
- 0.2.3: 新增命令行模式打印
