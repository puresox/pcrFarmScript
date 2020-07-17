from Automator import *


def finishTheAccount(automator, account):
    dxcFin = False
    # 登录至主页
    automator.loginToIndex(account)
    # 任务：完成地下城
    if automator.dxc():
        dxcFin = True
    # 返回标题页面
    automator.returnTitle()
    return dxcFin


# 进程函数
def worker(devicesName, accountQueue, finishQueue):
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
    while True:
        recv = accountQueue.get()
        if recv["info"] == "exit":
            break
        elif recv["info"] == "account":
            res = finishTheAccount(automator, recv["data"])
            finishQueue.put({"info": "accountFin", "data": "dxc" if res else None})
        elif recv["info"] == "firstFin":
            config, account1, account2 = recv["data"]
            if config["farmNum"] == 1 and config["kickedOut"]:
                automator.dissmiss(account1)
            elif config["farmNum"] == 2:
                # 踢出主号
                automator.dissmiss(account1)
                # 会长邀请
                automator.invite(account2, config["id"])
                # 主号加入第二个农场
                automator.joinIn(
                    [config["mainAccountName"], config["mainAccountPassword"]]
                )
            finishQueue.put({"info": "firstFin"})
        elif recv["info"] == "secondFin":
            config, account1, account2 = recv["data"]
            # 踢出主号
            automator.dissmiss(account2)
            if not config["kickedOut"]:
                # 会长邀请
                automator.invite(account1, config["id"])
                # 主号加入第1个农场
                automator.joinIn(
                    [config["mainAccountName"], config["mainAccountPassword"]]
                )
            finishQueue.put({"info": "secondFin"})
        else:
            break
