import uiautomator2 as u2
from template import templateMatching
from time import sleep


class Automator:
    def __init__(self, devicesName):
        self.d = u2.connect(devicesName)

    def touch(self, pos):
        self.d.click(pos[0], pos[1])

    def exists(self, filename):
        pos = templateMatching(filename, self.d)
        return pos if pos else False

    def text(self, text):
        self.d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        self.d.send_keys(text)  # adb广播输入
        # self.d.clear_text()  # 清除输入框所有内容(Require android-uiautomator.apk version >= 1.0.7)
        self.d.set_fastinput_ime(False)  # 切换成正常的输入法

    # 等待模板出现，点击模板，等待模板消失
    def touchToAnotherPage(self, filename, sleepTime=0.5):
        pos = self.exists(filename)
        while not pos:
            sleep(sleepTime)
            pos = self.exists(filename)
        self.touch(pos)
        sleep(1)
        pos = self.exists(filename)
        while pos:
            self.touch(pos)
            sleep(1)
            pos = self.exists(filename)

    # 点击，直到模板出现
    def tapUntilPage(self, filename, pos, sleepTime=0.5):
        while not self.exists(filename):
            self.touch(pos)
            sleep(sleepTime)

    # 任务：完成地下城
    def dxc(self):
        # 进入冒险
        self.d.toast.show("正在进入冒险")
        self.touchToAnotherPage("tpl1592027165856.png")
        # 进入地下城
        self.d.toast.show("正在进入地下城")
        self.touchToAnotherPage("tpl1592180931022.png")
        # 剩余次数判断
        self.d.toast.show("正在判断剩余挑战次数")
        while not self.exists("tpl1592027414908.png"):
            sleep(0.5)
        if not self.exists("tpl1592103530447.png"):
            self.d.toast.show("有剩余挑战次数")
            # 进入云海的山脉
            self.d.toast.show("正在进入云海的山脉")
            self.touchToAnotherPage("tpl1592027764805.png")
            # 区域选择确认
            self.d.toast.show("正在区域选择确认")
            self.touchToAnotherPage("tpl1592028260285.png")
            # 挑战第一层
            self.d.toast.show("正在寻找第一层")
            self.touchToAnotherPage("tpl1592100695213.png")
            # 挑战
            self.d.toast.show("正在寻找挑战按钮")
            self.touchToAnotherPage("tpl1592100750643.png")
            # 选择支援
            self.d.toast.show("正在寻找支援按钮")
            self.touchToAnotherPage("tpl1592100773675.png")
            # 选择人物
            self.d.toast.show("正在选择人物")
            self.touch((112, 181))
            sleep(0.5)
            self.touch((218, 192))
            # 战斗开始
            self.d.toast.show("正在寻找战斗开始按钮")
            self.touchToAnotherPage("tpl1592101037243.png")
            # 支援角色确认
            self.d.toast.show("正在支援角色确认")
            self.touchToAnotherPage("tpl1592101770586.png")
            # 菜单
            self.d.toast.show("正在寻找菜单按钮")
            self.touchToAnotherPage("tpl1592101805349.png")
            # 放弃
            self.d.toast.show("正在寻找放弃按钮")
            self.touchToAnotherPage("tpl1592103413823.png")
            # 放弃确认
            self.d.toast.show("正在放弃确认")
            self.touchToAnotherPage("tpl1592101839055.png")
            # 撤退
            self.d.toast.show("正在寻找撤退按钮")
            self.touchToAnotherPage("tpl1592103018208.png")
            # 撤退确认
            self.d.toast.show("正在撤退确认")
            self.touchToAnotherPage("tpl1592028260285.png")
            result = True
        else:
            self.d.toast.show("无剩余挑战次数")
            result = False
        # 返回我的主页
        self.d.toast.show("正在寻找我的主页")
        self.touchToAnotherPage("tpl1592315231328.png")
        return result

    # 任务：领取每日任务
    def dailyTask(self):
        # 进入每日任务
        self.d.toast.show("正在进入每日任务")
        self.touchToAnotherPage("tpl1592315503607.png")
        # 全部领取
        self.d.toast.show("正在全部领取")
        self.touchToAnotherPage("tpl1592315550372.png")
        # 关闭
        self.d.toast.show("正在关闭")
        self.touchToAnotherPage("tpl1592315600758.png")
        # 返回我的主页
        self.d.toast.show("正在寻找我的主页")
        self.touchToAnotherPage("tpl1592315231328.png")

    # 任务：扭蛋
    def niudan(self):
        # 进入扭蛋页面
        self.d.toast.show("正在进入扭蛋页面")
        self.touchToAnotherPage("tpl1592315975347.png")
        # 进入普通扭蛋
        self.d.toast.show("正在进入普通扭蛋")
        self.touchToAnotherPage("tpl1592316033948.png")
        # 免费十次
        self.d.toast.show("正在免费十次")
        self.touchToAnotherPage("tpl1592393825804.png")
        # ok
        self.d.toast.show("正在确认")
        self.touchToAnotherPage("tpl1592028260285.png")
        # 返回我的主页
        self.d.toast.show("正在寻找我的主页")
        self.touchToAnotherPage("tpl1592315231328.png")

    # 任务：工会之家
    def zhijia(self):
        # 进入工会之家
        self.d.toast.show("正在进入工会之家")
        self.touchToAnotherPage("tpl1592316254114.png")
        # 全部获取
        self.d.toast.show("正在全部获取")
        self.touchToAnotherPage("tpl1592316304606.png")
        # 关闭
        self.d.toast.show("正在关闭")
        self.touchToAnotherPage("tpl1592315600758.png")
        # 返回我的主页
        self.d.toast.show("正在寻找我的主页")
        self.touchToAnotherPage("tpl1592315231328.png")

    # 登录至主页
    def loginToIndex(self, account):
        # 账号为account[0]，密码为account[1]
        # 登录
        self.d.toast.show("正在寻找登录框")
        self.tapUntilPage("tpl1592025729669.png", (909, 26), 0)
        self.d.toast.show("输入账号密码中")
        self.touch((484, 200))
        self.text(account[0])
        self.touch((484, 245))
        self.text(account[1])
        self.touchToAnotherPage("tpl1592026144417.png")
        # 进入我的主页
        self.d.toast.show("正在进入我的主页")
        while not self.exists("tpl1592027165856.png"):
            self.touch((5, 478))
            if self.exists("tpl1594515801792.png"):
                self.touchToAnotherPage("tpl1594515801792.png")
            elif self.exists("tpl1594515626665.png"):
                sleep(1.0)
                self.touch((413, 305))
                sleep(1.0)
                self.touchToAnotherPage("tpl1594515653971.png")
                self.touchToAnotherPage("tpl1594515801792.png")
        sleep(1.0)
        self.touch((5, 478))

    # 返回标题页面
    def returnTitle(self):
        # 主菜单
        self.d.toast.show("正在寻找主菜单")
        self.touchToAnotherPage("tpl1592028158165.png")
        # 回到标题画面
        self.d.toast.show("正在寻找回到标题画面")
        self.touchToAnotherPage("tpl1592102003131.png")
        # 确认
        self.d.toast.show("正在寻找确认按钮")
        self.touchToAnotherPage("tpl1592028260285.png")

    # 踢出主号
    def dissmiss(self, account):
        # 账号为account[0]，密码为account[1]
        # 登录至主页
        self.loginToIndex(account)
        # 进入行会页面
        self.d.toast.show("正在寻找行会")
        self.touchToAnotherPage("tpl1593393941473.png")
        # 进入成员信息
        self.d.toast.show("正在寻找成员信息")
        self.touchToAnotherPage("tpl1593393983994.png")
        # 排序
        self.d.toast.show("正在排序")
        self.touchToAnotherPage("tpl1593394033271.png")
        while not self.exists("tpl1593409464173.png"):
            sleep(0.5)
        self.touch((507, 230))
        self.touchToAnotherPage("tpl1592028260285.png")
        # 踢出
        self.d.toast.show("正在踢出")
        self.touchToAnotherPage("tpl1593394114441.png")
        self.touchToAnotherPage("tpl1593409580890.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        self.touchToAnotherPage("tpl1593394261860.png")
        # 返回标题页面
        self.returnTitle()

    # 主号加入农场
    def joinIn(self, account):
        # 登录至主页
        self.loginToIndex(account)
        # 进入行会页面
        self.d.toast.show("正在寻找行会")
        self.touchToAnotherPage("tpl1593393941473.png")
        # 加入行会
        self.d.toast.show("正在加入行会")
        self.touchToAnotherPage("tpl1593396190835.png")
        self.touchToAnotherPage("tpl1594521095752.png")
        self.touchToAnotherPage("tpl1593396230001.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        # 支援设定
        self.d.toast.show("正在支援设定")
        self.touchToAnotherPage("tpl1593396278172.png")
        while not self.exists("tpl1593393941473.png"):
            self.d.toast.show("\a")
        # 返回标题页面
        self.returnTitle()

    # 会长邀请
    def invite(self, account, id):
        # 账号为account[0]，密码为account[1]
        # 登录至主页
        self.loginToIndex(account)
        # 进入行会页面
        self.d.toast.show("正在寻找行会")
        self.touchToAnotherPage("tpl1593393941473.png")
        # 进入成员信息
        self.d.toast.show("正在寻找成员信息")
        self.touchToAnotherPage("tpl1593393983994.png")
        # 邀请
        self.d.toast.show("正在邀请")
        self.touchToAnotherPage("tpl1593395834169.png")
        self.touchToAnotherPage("tpl1593395848862.png")
        self.touchToAnotherPage("tpl1593395907168.png")
        self.text(id)
        self.touchToAnotherPage("tpl1593395098201.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        self.touchToAnotherPage("tpl1593395985041.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        # 返回标题页面
        self.returnTitle()

    # 任务：刷1-1
    def shua(self):
        # 进入冒险
        self.d.toast.show("正在进入冒险")
        self.touchToAnotherPage("tpl1592027165856.png")
        # 进入主线关卡
        self.d.toast.show("正在进入主线关卡")
        self.touchToAnotherPage("tpl1592393876870.png")
        # 进入地图
        self.d.toast.show("正在进入地图")
        self.touchToAnotherPage("tpl1592393984404.png")
        # 进入1图
        self.d.toast.show("正在进入1图")
        self.touchToAnotherPage("tpl1592394102731.png")
        # 购买扫荡券
        self.d.toast.show("购买扫荡券")
        self.tapUntilPage(
            "tpl1592394358740.png", (796, 29),
        )
        self.touchToAnotherPage("tpl1592394438890.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        self.touchToAnotherPage("tpl1592394536139.png")
        self.touchToAnotherPage("tpl1592028260285.png")
        self.touchToAnotherPage("tpl1592394569588.png")
        # 进入1-1
        self.d.toast.show("正在进入1-1")
        self.touchToAnotherPage("tpl1592394185153.png")
