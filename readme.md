

# 已经支持的网站
- acm https://dl.acm.org/action/doSearch
- IEEE https://ieeexplore.ieee.org/

# 项目流程
1.通过关键词搜索，获取doi，存储到数据库
    
2.通过数据库查询尚未获取bib的条目，通过bib查询bib信息，更新数据库

3.通过doi在scihub下载pdf

# 如何使用
1.在config.py中配置数据库。

2.安装依赖（pip install -r requirements.txt）

3.运行主函数