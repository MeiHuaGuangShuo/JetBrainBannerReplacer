# JetBrainBannerReplacer
A python script to auto replace the starting banner of the JetBrains IDEA / 一个Python的自动化脚本，方便地替换JetBrains的启动图


# Feature / 特点
基本自动地替换启动图，不需要再麻烦的一个一个搞

理论上支持全部JetBrains IDEA (2024.1+)版本，但是懒得做，搜索过滤只有PyCharm, Clion, RustRover，在PyCharm2024.1上测试成功


# Usage / 使用

**重要：需要含有java环境，因为涉及jar命令的操作**

**IDE 安装位置文件夹深度不能超过4级，否则扫不到（性能考虑）**

1. 安装依赖
```shell
pip install pywin32 rich pillow
```
2. 启动程序
```shell
python replace_jb.py
```
3. 根据提示输入对应数据

输出示例
```shell
$ python replace_jb.py
Scan                           ━━━━━━━━━━━━━━━━━━━ 6/6     100% Used 0:00:00 Remain 0:00:00
C:\Windows.new.001             ━━━━━━━━━━━━━━━━━━━ 8/8     100% Used 0:00:00 Remain 0:00:00
D:\百度网盘.lnk                ━━━━━━━━━━━━━━━━━━━ 2/2     100% Used 0:00:00 Remain 0:00:00
E:\高考倒计时                  ━━━━━━━━━━━━━━━━━━━ 25/25   100% Used 0:00:00 Remain 0:00:00
F:\本地磁盘 (D).lnk            ━━━━━━━━━━━━━━━━━━━ 7/7     100% Used 0:00:00 Remain 0:00:00
G:\                           ━━━━━━━━━━━━━━━━━━━ 7/7     100% Used 0:00:00 Remain 0:00:00
H:\高清动漫图片                ━━━━━━━━━━━━━━━━━━━ 118/118 100% Used 0:00:00 Remain 0:00:00
1. H:\Program Files\JetBrains\CLion 2023.1.3
2. H:\Program Files\JetBrains\PyCharm Professional
3. H:\Program Files\JetBrains\RustRover 233.14015.147
Select Current Dir no: 2
Selected dir 'H:\Program Files\JetBrains\PyCharm Professional'
Replace image locate(absolute): H:\Users\Admin\Desktop\Python.png  
jar 17.0.10
jar -xvf H:\Program Files\JetBrains\PyCharm Professional\lib\.ReplaceLogo\app.jar  0:00:13 
jar -cfM0 H:\Program Files\JetBrains\PyCharm Professional\lib\.ReplaceLogo\app.jar 0:01:57 
Auto deleted cache.
```

