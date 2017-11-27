#!/usr/bin/python3
# coding:utf-8
import sys
import io
import json
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 最终文件
save2File = []
classNames = []
result = []
# key className
Result = collections.namedtuple("Result", ["key", "define", "name"])

inPutFile = "./json.json"
outPutFile = "./model.txt"


def getJsonDic():
    with open(inPutFile, "r", encoding='utf-8') as f:
        d = json.load(f)
        return d


def wirteString(string):
    with open(outPutFile, "w", encoding='utf-8') as f:
        f.write(string)


def convetType(value, key):
    if isinstance(value, str):
        return "String"
    elif isinstance(value, float):
        return "Float"
    elif isinstance(value, bool):
        return "Bool"
    elif isinstance(value, int):
        return "Int"
    elif isinstance(value, list):
        return "[{0}]".format(key)
    elif isinstance(value, dict):
        return key
    elif not value:
        return "String"
    else:
        return "String"


def realKey(key):
    return "%s" % (key.capitalize())


def proDict(dic, name=""):
    if name != "":
        classNames.append(name)

    for (key, value) in dic.items():
        clsName = realKey(key)
        if isinstance(value, list):
            proDict(value[0], clsName)
        elif isinstance(value, dict):
            proDict(value, clsName)

        k = '    var {0}: {1}?'.format(key, convetType(value, clsName))
        result.append(Result(key, k, name))


def process(data, name):
    name = realKey(name)
    if isinstance(data, list):
        proDict(data[0], name)
    elif isinstance(data, dict):
        proDict(data, name)

    return display()


def display():
    for cls in classNames:
        save2File.append("struct %s:Decodable {" % cls)
        for r in result:
            if r.name == cls:
                save2File.append(r.define)
        save2File.append("}")
        save2File.append("")
        save2File.append("")
    return save2File


def getSaveString():
    saveString = ""
    for s in save2File:
        saveString += s + "\n"
    return saveString


jsonDic = getJsonDic()
process(jsonDic, "Model")
saveString = getSaveString()
print(saveString)
wirteString(saveString)
