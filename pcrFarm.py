import subprocess
import json
import threading
from Automator import *
from progress.bar import Bar

"""获取设备列表"""
subprocess.check_output("./adb/adb.exe kill-server")  # killing...
subprocess.check_output("./adb/adb.exe start-server")  # killing...
lines = (
    subprocess.check_output("./adb/adb.exe devices").decode("utf-8").splitlines()[1:-1]
)  # 获取设备列表
devicesNames = []  # 获取设备名称列表
for line in lines:
    lineSplit = line.split("\t")
    if lineSplit[1] == "device":
        devicesNames.append(lineSplit[0])
automators = []  # Automator对象列表
for devicesName in devicesNames:
    automators.append(Automator(devicesName))  # connect to device

"""多线程执行任务"""
# 获取配置
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
deviceNum = len(automators)
print("农场数量：%d\n模拟器数量：%d" % (farmNum, deviceNum))
if kickedOut:
    print("请注意：执行完后将被踢出工会！")

# 读取账号信息
# lines:账号字符串行列表
# accounts:账号列表 账号为account[0]，密码为account[1]
# accountsNum1, accountsNum2:账号数量
lines, accounts, accountsNum1, accountsNum2 = (
    [],
    [],
    0,
    0,
)
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

# 线程变量
goodAccounts = 0  # 有剩余次数的账号(互斥访问)
goodAccountsLock = threading.Lock()  # 线程锁
accountIndex = 0  # 账号索引值(互斥访问)
accountIndexLock = threading.Lock()  # 线程锁
barrier = threading.Barrier(deviceNum)  # 栅栏
bar = Bar("loading", max=accountsNum1 + accountsNum2)
barLock = threading.Lock()  # 线程锁

# 线程函数
def worker(automator):
    global accountIndex, goodAccounts, bar
    # 返回首页
    automator.keyevent("home")
    # 打开公主连结APP
    automator.touchToAnotherPage("tpl1592013602699.png")
    # 完成一个农场
    while True:
        accountIndexLock.acquire()  # 上锁
        if accountIndex >= accountsNum1:
            accountIndexLock.release()  # 解锁
            break
        account = accounts[accountIndex]
        accountIndex += 1
        accountIndexLock.release()  # 解锁
        # 登录至主页
        automator.loginToIndex(account)
        # 任务：完成地下城
        if automator.dxc():
            goodAccountsLock.acquire()  # 上锁
            goodAccounts += 1
            goodAccountsLock.release()  # 解锁
        # 返回标题页面
        automator.returnTitle()
        # 进度更新
        barLock.acquire()  # 上锁
        bar.next()
        barLock.release()  # 解锁

    # 等待其他进程
    barrier.wait()

    if farmNum == 1:
        if automator.devicesName == devicesNames[0]:
            # print("账号总计 %d 个，完成地下城总计 %d 个" % (accountsNum1, goodAccounts))
            if kickedOut:
                # 踢出主号
                automator.dissmiss(accounts[0])
    elif farmNum == 2:
        if automator.devicesName == devicesNames[0]:
            # 踢出主号
            automator.dissmiss(accounts[0])
            # 会长邀请
            automator.invite(accounts[accountsNum1], id)
            # 主号加入第二个农场
            automator.joinIn([mainAccountName, mainAccountPassword])
        # 等待其他进程
        barrier.wait()
        # 完成一个农场
        while True:
            accountIndexLock.acquire()  # 上锁
            if accountIndex >= accountsNum1 + accountsNum2:
                accountIndexLock.release()  # 解锁
                break
            account = accounts[accountIndex]
            accountIndex += 1
            accountIndexLock.release()  # 解锁
            # 登录至主页
            automator.loginToIndex(account)
            # 任务：完成地下城
            if automator.dxc():
                goodAccountsLock.acquire()  # 上锁
                goodAccounts += 1
                goodAccountsLock.release()  # 解锁
            # 返回标题页面
            automator.returnTitle()
            # 进度更新
            barLock.acquire()  # 上锁
            bar.next()
            barLock.release()  # 解锁

        # 等待其他进程
        barrier.wait()

        if automator.devicesName == devicesNames[0]:
            # print(
            #     "账号总计 %d 个，完成地下城总计 %d 个" % (accountsNum1 + accountsNum2, goodAccounts)
            # )
            # 踢出主号
            automator.dissmiss(accounts[accountsNum1])
            if not kickedOut:
                # 会长邀请
                automator.invite(accounts[0], id)
                # 主号加入第1个农场
                automator.joinIn([mainAccountName, mainAccountPassword])


# 启动多线程完成一个农场
threadList = []  # 线程列表
for i in range(deviceNum):
    threadList.append(threading.Thread(target=worker, args=(automators[i],)))
    threadList[i].start()
for i in range(deviceNum):
    threadList[i].join()
bar.finish()
