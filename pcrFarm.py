import subprocess
import multiprocessing
from Automator import *
from Farm import *
import os


def finishFarm(automator, upperLimit, farm):
    # 完成一个农场
    while True:
        farm.accountIndexLock.acquire()  # 上锁
        if farm.accountIndex >= upperLimit:
            farm.accountIndexLock.release()  # 解锁
            break
        account = farm.accounts[farm.accountIndex]
        farm.accountIndex += 1
        farm.accountIndexLock.release()  # 解锁
        # 登录至主页
        automator.loginToIndex(account)
        # 任务：完成地下城
        if automator.dxc():
            farm.goodAccountsLock.acquire()  # 上锁
            farm.goodAccounts += 1
            farm.goodAccountsLock.release()  # 解锁
        # 返回标题页面
        automator.returnTitle()
        # 进度更新
        farm.barLock.acquire()  # 上锁
        farm.bar.next()
        farm.barLock.release()  # 解锁
    # 等待其他进程
    farm.barrier.wait()


# 进程函数
def worker(devicesName, farm):
    automator = Automator(devicesName)
    # 返回首页
    automator.keyevent("home")
    # 关闭公主连结
    pcrName = "com.bilibili.priconne"
    apps = automator.listRunningApps()
    if pcrName in apps:
        automator.stopApp(pcrName)
    # 打开公主连结APP
    automator.touchToAnotherPage("tpl1592013602699.png")
    # 完成一个农场
    finishFarm(automator, farm.accountsNum1, farm)

    if farm.farmNum == 1:
        if automator.devicesName == devicesNames[0]:
            # print("账号总计 %d 个，完成地下城总计 %d 个" % (accountsNum1, goodAccounts))
            if farm.kickedOut:
                # 踢出主号
                automator.dissmiss(farm.accounts[0])
    elif farm.farmNum == 2:
        if automator.devicesName == devicesNames[0]:
            # 踢出主号
            automator.dissmiss(farm.accounts[0])
            # 会长邀请
            automator.invite(farm.accounts[farm.accountsNum1], farm.id)
            # 主号加入第二个农场
            automator.joinIn([farm.mainAccountName, farm.mainAccountPassword])
        # 等待其他进程
        farm.barrier.wait()
        # 完成一个农场
        finishFarm(automator, farm.accountsNum1 + farm.accountsNum2, farm)

        if automator.devicesName == devicesNames[0]:
            # 踢出主号
            automator.dissmiss(farm.accounts[farm.accountsNum1])
            if not farm.kickedOut:
                # 会长邀请
                automator.invite(farm.accounts[0], farm.id)
                # 主号加入第1个农场
                automator.joinIn([farm.mainAccountName, farm.mainAccountPassword])


if __name__ == "__main__":
    version = "1.0.0"
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
    print("发现%d个模拟器,列表如下:" % (deviceNum))
    for devicesName in devicesNames:
        print(devicesName)

    """初始化农场类"""
    farm = Farm(deviceNum)
    print("农场数量：%d" % (farm.farmNum))
    if farm.kickedOut:
        print("请注意：执行完后将被踢出工会！")

    """多进程完成农场"""
    print("正在初始化子进程")
    processList = []  # 进程列表
    for devicesName in devicesNames:
        p = multiprocessing.Process(target=worker, args=(devicesName, farm,))
        p.start()
        processList.append(p)
    for p in processList:
        p.join()
    farm.bar.finish()
    print(
        "运行结束：账号总计 %d 个，完成地下城总计 %d 个"
        % (farm.accountsNum1 + farm.accountsNum2, farm.goodAccounts)
    )
    os.system("pause")
