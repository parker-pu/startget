# StartGet
下载软件

### 打包
- 单个文件
```
# 这一般用来添加exe的图标
pyinstaller -F -i someicon.ico cron_transfer_v2.py

# 图片变成代码
pyside6-rcc image.qrc -o src/utils/images.py

# auto-py-to-exe
# 或者
pyinstaller --noconfirm --onefile --windowed --icon "E:/code/qt_transfer/static/favicon.ico" --name "QtTransfer"  "E:/code/qt_transfer/start.py"
```