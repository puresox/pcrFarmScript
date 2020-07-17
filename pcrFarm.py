import subprocess
import multiprocessing
import os
from progress.bar import Bar
import json
from mutiprocessFunc import worker


if __name__ == "__main__":
    # pyinstaller: When using the multiprocessing module, you must call
    multiprocessing.freeze_support()
    version = "1.1.0"
    print("当前版本：%s" % (version))

    """获取设备列表"""
    print("正在获取模拟器列表")
    subprocess.check_output("./adb/adb.exe kill-server")
    subprocess.check_output("./adb/adb.exe start-server")
    lines = (
        subprocess.check_output("./adb/adb.exe devices")
        .decode("utf-8")
        .splitlines()[1:-1]
    )  # 获取设备列表
    devicesNames = []  # 获取设备名称列表
    for line in lines:
        lineSplit = line.split("\t")
        if lineSplit[1] == "device":
            devicesNames.append(lineSplit[0])
    deviceNum = len(devicesNames)
    print("发现如下%d个模拟器:" % (deviceNum))
    for devicesName in devicesNames:
        print(devicesName)

    """获取配置"""
    config, configPath = {}, "config/config.json"
    with open(configPath, encoding="utf-8-sig") as configStr:
        config = json.load(configStr)
        farmNum, kickedOut, mainAccountName, mainAccountPassword, id = (
            config["farmNum"],
            config["kickedOut"],
            config["mainAccountName"],
            config["mainAccountPassword"],
            config["id"],
        )
    print("农场数量：%d" % (farmNum))
    if kickedOut:
        print("请注意：执行完后将被踢出工会！")

    """读取账号信息"""
    # lines:账号字符串行列表
    # accounts:账号列表 账号为account[0]，密码为account[1]
    # accountsNum1, accountsNum2:账号数量
    lines, accounts = ([], [])
    with open("config/farm01.txt") as f:
        lines1 = f.readlines()
        accountsNum1 = len(lines1)
        lines += lines1
    with open("config/farm02.txt") as f:
        lines2 = f.readlines()
        accountsNum2 = len(lines2)
        lines += lines2
    for line in lines:
        accounts.append(line.strip("\n").split(" "))

    """进程通信"""
    accountQueue = multiprocessing.Queue()
    finishQueue = multiprocessing.Queue()

    """多进程完成农场"""
    dxcFinAccount = 0
    processBar = Bar("初始化子进程", max=deviceNum)
    farmBar = Bar("运行中", max=accountsNum1 + accountsNum2)
    processList = []  # 进程列表
    for devicesName in devicesNames:
        processBar.next()
        p = multiprocessing.Process(
            target=worker, args=(devicesName, accountQueue, finishQueue)
        )
        p.start()
        processList.append(p)
    processBar.finish()
    # 账号队列accountQueue: "account","exit","firstFin","secondFin"
    # 账号完成队列finishQueue: "accountFin","firstFin","secondFin"
    # 输入第一个农场的账号
    for i in range(accountsNum1):
        accountQueue.put({"info": "account", "data": accounts[i]})
    # 完成第一个农场的账号
    for i in range(accountsNum1):
        recv = finishQueue.get()
        farmBar.next()
        if recv["data"] == "dxc":
            dxcFinAccount += 1
    # 换农场
    accountQueue.put(
        {"info": "firstFin", "data": [config, accounts[0], accounts[accountsNum1]]}
    )
    # 完成换农场
    recv = finishQueue.get()
    if farmNum == 2:
        # 输入第二个农场的账号
        for i in range(accountsNum2):
            accountQueue.put({"info": "account", "data": accounts[accountsNum1 + i]})
        # 完成第二个农场的账号
        for i in range(accountsNum2):
            recv = finishQueue.get()
            farmBar.next()
            if recv["data"] == "dxc":
                dxcFinAccount += 1
        # 换农场
        accountQueue.put(
            {"info": "secondFin", "data": [config, accounts[0], accounts[accountsNum1]]}
        )
        # 完成换农场
        recv = finishQueue.get()
    # 完成
    for i in range(deviceNum):
        accountQueue.put({"info": "exit"})
    for p in processList:
        p.join()
    farmBar.finish()
    print("运行结束：账号总计 %d 个，完成地下城总计 %d 个" % (accountsNum1 + accountsNum2, dxcFinAccount))
    os.system("pause")
