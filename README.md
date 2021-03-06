# pcrFarmScript
使用简单的公主连结40对1**自动化**农场脚本

## 特点

- 支持模拟器多开。
- 使用简单，开袋即食，不需要安装环境，但是需要配置账号信息。
- 40对1，自动切换农场。
- 自动记录支援人物并且自动设置支援人物。

## 注意
该脚本只能用于成品农场号的日常维护（农场号借用大号人物打地下城），并不能养成一个农场号，农场号的养成请参考[《农场号的养成》](https://github.com/puresox/pcrFarmScript/wiki/农场号的养成)。请确保：

- 使用脚本之前不能提前进入地下城，不然会有逻辑错误。
- 只要出现可可罗或流程以外的弹窗就会出错，可以手动把可可罗点掉或把弹窗关掉，脚本会继续执行。
- 大号的支援角色等级不能超过小号30级。

使用过程中有问题可以发[issue](https://github.com/puresox/pcrFarmScript/issues)。

## 使用说明

1. 使用雷电模拟器4（不能是3），设置->性能设置->分辨率改为960*540（dpi 160），设置->其他设置中关闭自动旋转屏幕。

2. 前往[Releases](https://github.com/puresox/pcrFarmScript/releases/latest)下载软件`pcrFarm.rar`。

3. 解压缩。

4. 配置账号信息：

   - 打开`pcrFarm/config/config.json`，修改信息：

     | 名称                | 备注                                                         |
     | ------------------- | ------------------------------------------------------------ |
     | farmNum             | 农场数量，1或2，只有当数量为2时才需要填写其他信息            |
     | mainAccountName     | 大号的账号                                                   |
     | mainAccountPassword | 大号的密码                                                   |
     | kickedOut           | 农场号捐完mana后是否将大号踢出农场，1代表踢出，0代表呆在农场 |
     | id                  | 大号的id，在游戏里的简介中可以查看，是一长串的数字           |

   - 配置账号信息。在`pcrFarm/config`文件夹中的`farm01.txt`和`farm02.txt`文件中写入第一个农场的29个账号的信息和第二个农场的11个账号的信息（如果只有一个农场就只写`farm01.txt`，有多少个就写多少个），每个账号一行，账号和密码用一个空格分开，最后一个账号之后不要回车。**会长的账号放在第一行！！！**
   
5. 打开模拟器，然后双击运行`pcrFarm.exe`文件。第一次运行可能会卡一会儿。


## 开发

`setuptools`<45.0.0
