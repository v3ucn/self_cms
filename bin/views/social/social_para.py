# -*- coding: UTF-8 -*-
####### lambda 示例: #######

# x 为由纯 int 型元素组成的集合，且不可为空
# lambda x: True if set(map(type, x)) == {int} else False

# x 为由纯 int 型元素组成的集合，可以为空
# lambda x: True if set(map(type, x)) in ({int}, set()) else False

# x 为 int 型 或 （由纯 int 型元素组成的集合，且不可为空）
# lambda x: True if isinstance(x, int) or set(map(type, x)) == {int} else False

############################
"""
@summary: 验证器
该模块提供了一个装饰器用于验证参数是否合法，使用方法为：

from validator import validParam, nullOk, multiType

@validParam(i=int)
def foo(i):
    return i+1

编写验证器：

1. 仅验证类型：
@validParam(type, ...)
例如：
检查第一个位置的参数是否为int类型：
@validParam(int)
检查名为x的参数是否为int类型：
@validParam(x=int)

验证多个参数：
@validParam(int, int)
指定参数名验证：
@validParam(int, s=str)

针对*和**参数编写的验证器将验证这些参数实际包含的每个元素：
@validParam(varargs=int)
def foo(*varargs): pass

@validParam(kws=int)
def foo7(s, **kws): pass

2. 带有条件的验证：
@validParam((type, condition), ...)
其中，condition是一个表达式字符串，使用x引用待验证的对象；
根据bool(表达式的值)判断是否通过验证，若计算表达式时抛出异常，视为失败。
例如：
验证一个10到20之间的整数：
@validParam(i=(int, '10<x<20'))
验证一个长度小于20的字符串：
@validParam(s=(str, 'len(x)<20'))
验证一个年龄小于20的学生：
@validParam(stu=(Student, 'x.age<20'))

另外，如果类型是字符串，condition还可以使用斜杠开头和结尾表示正则表达式匹配。
验证一个由数字组成的字符串：
@validParam(s=(str, '/^\d*$/'))

3. 以上验证方式默认为当值是None时验证失败。如果None是合法的参数，可以使用nullOk()。
nullOk()接受一个验证条件作为参数。
例如：
@validParam(i=nullOk(int))
@validParam(i=nullOk((int, '10<x<20')))
也可以简写为：
@validParam(i=nullOk(int, '10<x<20'))

4. 如果参数有多个合法的类型，可以使用multiType()。
multiType()可接受多个参数，每个参数都是一个验证条件。
例如：
@validParam(s=multiType(int, str))
@validParam(s=multiType((int, 'x>20'), nullOk(str, '/^\d+$/')))

5. 如果有更复杂的验证需求，还可以编写一个函数作为验证函数传入。
这个函数接收待验证的对象作为参数，根据bool(返回值)判断是否通过验证，抛出异常视为失败。
例如：
def validFunction(x):
    return isinstance(x, int) and x>0
@validParam(i=validFunction)
def foo(i): pass

这个验证函数等价于：
@validParam(i=(int, 'x>0'))
def foo(i): pass

"""

import inspect
import re


class ValidateException(Exception):
    pass


def validParam(*varargs, **keywords):
    """验证参数的装饰器。"""

    varargs = map(_toStardardCondition, varargs)
    keywords = dict((k, _toStardardCondition(keywords[k]))
                    for k in keywords)

    def generator(func):
        args, varargname, kwname = inspect.getargspec(func)[:3]
        defaults = inspect.getargspec(func)[-1]
        dctValidator = _getcallargs(args, varargname, kwname,
                                    varargs, keywords)

        def wrapper(*callvarargs, **callkeywords):
            '''
            dctCallArgs = _getcallargs(args, varargname, kwname,
                                       callvarargs, callkeywords)
            '''
            dctCallArgs = _getcallargs_1(args, varargname, kwname,
                                         callvarargs, callkeywords, defaults)
            k, item = None, None
            try:
                for k in dctValidator:
                    if k == varargname:
                        for item in dctCallArgs[k]:
                            assert dctValidator[k](item)
                    elif k == kwname:
                        for item in dctCallArgs[k].values():
                            assert dctValidator[k](item)
                    else:
                        item = dctCallArgs[k]
                        assert dctValidator[k](item)
            except:
                raise ValidateException, \
                    ('%s() parameter validation fails, param: %s, value: %s(%s)'
                     % (func.func_name, k, item, item.__class__.__name__))

            return func(*callvarargs, **callkeywords)

        wrapper = _wrapps(wrapper, func)
        return wrapper

    return generator


def _toStardardCondition(condition):
    """将各种格式的检查条件转换为检查函数"""

    if inspect.isclass(condition):
        return lambda x: isinstance(x, condition)

    if isinstance(condition, (tuple, list)):
        cls, condition = condition[:2]
        if condition is None:
            return _toStardardCondition(cls)

        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            return lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)

        return lambda x: isinstance(x, cls) and eval(condition)

    return condition


def nullOk(cls, condition=None):
    """这个函数指定的检查条件可以接受None值"""

    return lambda x: x is None or _toStardardCondition((cls, condition))(x)


def multiType(*conditions):
    """这个函数指定的检查条件只需要有一个通过"""

    lstValidator = map(_toStardardCondition, conditions)

    def validate(x):
        for v in lstValidator:
            if v(x):
                return True

    return validate


def _getcallargs(args, varargname, kwname, varargs, keywords):
    """获取调用时的各参数名-值的字典"""

    dctArgs = {}
    varargs = tuple(varargs)
    keywords = dict(keywords)

    argcount = len(args)
    varcount = len(varargs)
    callvarargs = None

    if argcount <= varcount:
        for n, argname in enumerate(args):
            dctArgs[argname] = varargs[n]

        callvarargs = varargs[-(varcount - argcount):]

    else:
        for n, var in enumerate(varargs):
            dctArgs[args[n]] = var

        for argname in args[-(argcount - varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)

        callvarargs = ()

    if varargname is not None:
        dctArgs[varargname] = callvarargs

    if kwname is not None:
        dctArgs[kwname] = keywords

    dctArgs.update(keywords)
    return dctArgs


def _getcallargs_1(args, varargname, kwname, varargs, keywords, defaults):
    """
    修改版，增加默认参数
    """

    dctArgs = {}
    varargs = tuple(varargs)
    keywords = dict(keywords)

    argcount = len(args)
    varcount = len(varargs)
    callvarargs = None

    if argcount <= varcount:
        for n, argname in enumerate(args):
            dctArgs[argname] = varargs[n]

        callvarargs = varargs[-(varcount - argcount):]

    else:
        for n, var in enumerate(varargs):
            dctArgs[args[n]] = var

        for argname in args[-(argcount - varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)

        callvarargs = ()

    if varargname is not None:
        dctArgs[varargname] = callvarargs

    if kwname is not None:
        dctArgs[kwname] = keywords

    dctArgs.update(keywords)
    # 修改部分，增加默认参数
    if defaults:
        default_dict = {}
        for i in range(len(defaults), 0, -1):
            default_dict[args[-i]] = defaults[-i]
        for k in default_dict:
            if k not in dctArgs:
                dctArgs[k] = default_dict[k]
    return dctArgs


def _wrapps(wrapper, wrapped):
    """复制元数据"""

    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    return wrapper
