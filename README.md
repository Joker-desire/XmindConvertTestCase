 
 > # 项目名：XmindConvertTestCase
> ###### *Author：Desire*
 
> ### 简介：
 **此项目是把用XMind写的测试用例，转成Excel，然后就可以导入到所使用的bug管理工具.**
 
 > ### XMind模板([模板](./data/case.xmind))：
 #### 把用例步骤和预期结果都拼接到了用例上
 ![XMind模板](http://desireyang.gitee.io/publicimg/Snipaste_2020-11-15_15-26-37.png)
 > > ### XMind2.0模板([模板](./data/case2.xmind))：
 #### pyxMind2.0 思维导图中格式定义：
- 步骤：step>
- 前置条件：pt>    
- 预期结果：er>

 ![XMind2.0模板](http://desireyang.gitee.io/publicimg/Snipaste_2020-11-23_13-56-00.png)
 ---
 > ### 使用到的技术
```
Python GUI
```

 > ### 使用到的库
 - xmindparser：读取XMind数据
 - jsonpath：处理json数据
 - openpyxl：操作Excel数据
 - pyqt5：桌面应用

 
> ### 项目结构
```text
├─common
│  └─ExcelData.py  操作Excel数据
│  │ └─create_excel_and_set_title
│  │ └─write_excel_data
│  └─XMindData.py  读取XMind数据，并做数据处理
│  │ └─read_XMind_to_list
│  │ └─get_lists_data
│  │ └─clear_init_list_data
├─data
│  └─case.xmind    xmind用例模板
│  └─case2.xmind   xmind2.0用例模板
├─dist
│  └─pyXmind.exe   打包后的可执行文件
├─Icon
│  └─window.ico    窗口的图标
└─install.py       打包执行文件
└─pyxMind.py       项目入口(把步骤预期结果全部拼接到用例后面了)
└─pyxMind2.0.py       项目2.0入口(单独把步骤，预期结果，前置条件，剔出来单独存放在单元格中)
└─README.md        README
```


