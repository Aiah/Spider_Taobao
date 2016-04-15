# Spider_Taobao

Get reviews from taobao

用来抓取淘宝某分类下的所有商品的相关评论

输出格式为：

用户昵称 等级 评论时间 评论 （追评）

nid rank time review (appenContent)

嘉***8	4	2016年04月14日 17:04	东西太棒了，物超所值啊！适合胖美美穿，没有比这再便宜的东西了！质量超棒！大爱

# 环境配置
## Python 2.7
## PhantomJS
## Selenium

与PhantomJS配合使用

from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get(url)

## BeautifulSoup
## requests
