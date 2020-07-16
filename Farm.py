import json
import multiprocessing
from progress.bar import Bar


class Farm:
    def __init__(self, deviceNum):
        """获取配置"""
        config, configPath = {}, "config/config.json"
        with open(configPath, encoding="utf-8-sig") as configStr:
            config = json.load(configStr)
        (
            self.farmNum,
            self.kickedOut,
            self.mainAccountName,
            self.mainAccountPassword,
            self.id,
        ) = (
            config["farmNum"],
            config["kickedOut"],
            config["mainAccountName"],
            config["mainAccountPassword"],
            config["id"],
        )

        """读取账号信息"""
        # lines:账号字符串行列表
        # accounts:账号列表 账号为account[0]，密码为account[1]
        # accountsNum1, accountsNum2:账号数量
        lines, self.accounts = ([], [])
        with open("config/farm01.txt") as f:
            lines1 = f.readlines()
            self.accountsNum1 = len(lines1)
            lines += lines1
        with open("config/farm02.txt") as f:
            lines2 = f.readlines()
            self.accountsNum2 = len(lines2)
            lines += lines2
        for line in lines:
            self.accounts.append(line.strip("\n").split(" "))

        """进程变量"""
        self.goodAccounts = 0  # 有剩余次数的账号(互斥访问)
        self.goodAccountsLock = multiprocessing.Lock()  # 进程锁
        self.accountIndex = 0  # 账号索引值(互斥访问)
        self.accountIndexLock = multiprocessing.Lock()  # 进程锁
        self.barrier = multiprocessing.Barrier(deviceNum)  # 栅栏
        self.barLock = multiprocessing.Lock()  # 进程锁

        self.bar = Bar("运行中", max=self.accountsNum1 + self.accountsNum2)
