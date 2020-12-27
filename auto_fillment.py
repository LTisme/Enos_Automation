from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui, pyperclip
import openpyxl
from time import sleep
import re

wb = openpyxl.load_workbook('data.xlsx')
sht = wb['Sheet1']

URL = 'https://portal-lywz1.eniot.io/configuration/addstation.html?locale=zh-CN&siteid='
ACCOUNT = 'TSKJ'
PASSWORD = '5PcvJBNj'
STATION = sht['A2'].value
SITEID = sht['B2'].value     # 测试场站的siteid
KitName = sht['C2'].value       # 设备名
Capacity = sht['E2'].value      # 容量
Rated_Current = sht['F2'].value     # 额定电流
PORT_NUM = sht['G2'].value      # 端口号
REGX = "a[href *='%s']" % SITEID      # 选到特定的带siteid的配置连接按钮

browser = webdriver.Firefox()
browser.get('https://portal-lywz1.eniot.io/portal/#platform-asset-conf//')
try:
    elem_account = browser.find_element_by_css_selector("input[type='text']").send_keys(ACCOUNT)    # 这种方法可以避免输入法冲突
    elem_password = browser.find_element_by_css_selector("input[type='password']").send_keys(PASSWORD)
    elem_button = browser.find_element_by_css_selector("button[class='index_submit_2OPCK']").click()
    sleep(6)
    elem_span = browser.find_element_by_css_selector("span[class='icon-CloseModuleSelection']").click()     # 这个都可
    # 以click了，那说明不是句柄切换的问题啊
    sleep(12)

    sleep(1)
    # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
    REAL_URL = URL + SITEID
    js = '''window.open('%s')''' % REAL_URL   # selenium中没有专门的打开新窗口的方法，是通过'window.execute_script()'来执行'js'脚本的形式来打开窗口的
    browser.execute_script(js)
    browser.switch_to.window(browser.window_handles[1])     # 选到场站信息窗口
    sleep(1)    # 以等待不要跳转的太快
    kit_button = browser.find_element_by_xpath("//button[contains(text(),'添加设备')]")       # 选到添加设备按钮
    # 注意，必须要全屏，或者滚动到 添加设备 这个按钮出现才能点击
    ActionChains(browser).click(kit_button).perform()       # 单纯的kit_button.click也行

    kit_selection_button = browser.find_element_by_css_selector("select[class='form-control eos-select-arrow']").click()
    # pyautogui.write(['down', 'down', 'down', 'down', 'down', 'down', 'down', 'down'])   # 8次向下选择到“多功能电表”
    # pyautogui.press('enter')    # 选择“多功能电表”
    option = browser.find_element_by_css_selector("option[value='227']").click()    # 这个直接可以选到多功能电表
    # kit_name = browser.find_element_by_id("attr_layout_1608641779377_name").send_keys(KitName)    # 输入设备名字，这个可行但id是动态变化的
    # # ￥￥￥￥￥￥￥￥##############
    # kit_name = browser.find_element_by_css_selector("input[id$='_name']").send_keys(KitName)    # 这个就不行，为什么？——因为找到的不是唯一的
    # &&&&&&&&&&￥￥￥￥￥￥￥￥￥￥￥
    kit_name = browser.find_elements_by_css_selector("input[data-key='name']")[2].send_keys(KitName)
    kit_voltage = browser.find_element_by_css_selector("input[data-key='Un']").send_keys('400')      # 输入线电压
    kit_maxCurrent = browser.find_element_by_css_selector("input[data-key='maxCurrent']").send_keys(Rated_Current)      # 输入额定电流
    kit_capacity = browser.find_element_by_css_selector("input[data-key='TransformerCapacity']").send_keys(Capacity)    # 输入容量
    kit_submit = browser.find_elements_by_css_selector("a[class='btn btn-primary eos-button-l']")[1].click()    # 提交保存
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑到这才算是添加了一个设备↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    # submit_after_addition = browser.find_elements_by_css_selector("a[class='btn btn-primary eos-button-l']")[1].click()     # 最后提交以更新场站信息
    submit_after_addition = browser.find_elements_by_xpath("//a[contains(text(),'保存')]")[0].click()     # 最后提交以更新场站信息
    # 《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《

    # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
    browser.switch_to.window(browser.window_handles[0])    # 选回Edge接入窗口
    iframe = browser.find_elements_by_tag_name("iframe")[0]     # 选到了iframe下

    browser.switch_to.frame(iframe)

    elem_inputbox = browser.find_element_by_css_selector("input[type='text']").send_keys(STATION)   # 往Edge的搜索框里输入要搜索的场站名
    elem_loupe = browser.find_element_by_css_selector("span[class='ic_basic-input-search-icon']").click()   # 点击右侧的搜索放大镜
    sleep(10)   # 等待10s

    elem_configuration = browser.find_element_by_css_selector("a[href*='%s']" % SITEID).click()     # 选到特定的配置按钮
    elem_add_box = browser.find_element_by_css_selector("button[class='dropdown btn btn-primary']").click()     # 点击添加盒子

    TEST_BOX_NAME = '141盒子'
    TEST_BOX_SN = '903dda4d-f78a-4780-97e3-00a0ac22dfdb'
    TEST_ADDRESS = '192.168.9.141'

    elem_box_name = browser.find_element_by_css_selector("input[id='addBoxName']").send_keys(TEST_BOX_NAME)     # 输入盒子名字
    elem_box_sn = browser.find_element_by_css_selector("input[id='addBoxSN']").send_keys(TEST_BOX_SN)       # 输入对应的SN号
    elem_box_submit = browser.find_element_by_xpath("// *[ @ id = 'container'] / div / div[1] / div[2] / div / div[2] / div[1] / div / div / div[3] / div / button[2]").click()     # 点击提交

    # 接下来点击添加连接
    link_add = browser.find_elements_by_css_selector("a[class='eos-link']")[1].click()      # 点击添加连接的链接
    link_name = browser.find_element_by_css_selector("input[id='collectName']").send_keys('104转发1')     # 连接的名字都叫104转发x，后期再对x做多端口处理
    link_mode = browser.find_element_by_css_selector("option[value='TCP_SVR']").click()     # 选中TCP/IP的处理方式
    link_address = browser.find_elements_by_css_selector("input[id='ipport']")[0].send_keys(TEST_ADDRESS)   # 发送内网盒子ip地址
    link_port = browser.find_elements_by_css_selector("input[id='port']")[0].send_keys(PORT_NUM)    # 发送端口号
    link_submit = browser.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div/div[3]/div/button[2]").click()      # 提交连接，用的绝对定位，比较繁琐

    # 对添加的连接添加先前已加入的设备并选一个初始模板——难点：如果有多个端口号，如何分配设备？方法：在excel表中就分配好，以及录入的时候不能过早跳转
    """首先得找到添加设备这个链接，然后往前偏移找出<span></span>用其中的内容来判断是否该点这个链接"""
    elem_filter = []
    devide_add = browser.find_elements_by_css_selector("a[class='eos-link']")
    for elem in devide_add:
        """这样找到了对应连接下的-添加设备-按钮"""
        try:
            if elem.find_element_by_xpath("parent::*/preceding-sibling::div[1]/span[2]").text == '104转发1':      # 104转发1还得用先前的变量替换
                elem_filter.append(elem)
        except:     # 忽略找不到对象的元素
            pass
    elem_filter[0].click()      # 之所以弄成这样，是为了避免浏览器被设置成英语就找不到元素的情况

    check_box = browser.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[1]/div[2]/div/table/thead/tr/th[1]/input").click()      # 选中所有设备
    # 然后统一设定一个变比模板，后面再来修改
    """或者说，读取excel的时候就进线正则判定，它应该选哪一个变比模板"""
    device_template = browser.find_element_by_css_selector("option[value='4169']").click()      # 统一先选 创力800/5的模板
    device_submit = browser.find_element_by_xpath(
        "//*[@id='container']/div/div[1]/div[2]/div/div[3]/div/div[2]/a[2]").click()        # 点击保存
    # 还是需要有变量存着刚才做的是哪个连接下的操作，以备后面点开去修改偏移量

    # TODO: 编写逻辑编号，以及各自的偏移量&各自独特的变比
    """这里还需要去判定104转发x左边的箭头的父节点是否是collapse-layout-open的，倘若是collapse-layout-close的，则需要去点击，否则没必要
    ——注意，这里是默认只有一个盒子的情况的，若有多个盒子，建议编写一个类来进行针对操作"""
    sleep(1.5)      # 等待反应
    elem_icon = browser.find_element_by_xpath("//span[contains(text(), '%s')]" % '104转发1')
    elem_icon.click()      # 试验了一下不需要判定，直接对先前存的变量进行点击就行————其实是需要判定的

    corresponding_edit_icon = elem_icon.find_element_by_xpath(
        "parent::*/parent::*/following-sibling::div[2]/div/div/table/tbody/tr/child::td[10]/div/div/a/span[1]")
    corresponding_edit_icon.click()     # 点击相应的编辑按钮

    # 这里实际测验发现应该用ctrl-a热键结合再输入，而且  #collpase0_1 ←←←这个也有问题，不能这么选，应该用104转发x的x-1作为#collpase0_x-1筛选
    logic_num = browser.find_element_by_css_selector(
        "#collpase0_0 > div > div > table > tbody > tr > td:nth-child(4) > div > input")
    logic_num.send_keys('1')     # 往逻辑编号中写入1
    # 注意，接下去必须用Xpath的偏移语法，这样才能保证写到的是同一行的内容——————实验后发现相对偏移很麻烦，还是以第一个为基准来偏移最好
    sleep(1)
    offset_1 = logic_num.find_element_by_xpath("parent::*/parent::*/following-sibling::td[1]")
    offset_2 = offset_1.find_element_by_css_selector("option[value='4114']")
    offset_2.click()     # 重新选择电管家YC78的模板
    sleep(1)
    offset_3 = offset_1.find_element_by_xpath("following-sibling::td[1]")
    # 这里实际测验发现应该也用ctrl-a热键结合再输入
    offset_3.find_element_by_css_selector("input[type='text']").send_keys('0-77')   # 输入AI偏移量
    offset_4 = offset_3.find_element_by_xpath("following-sibling::td[1]")
    sleep(1)
    # 这里实际测验发现应该也用ctrl-a热键结合再输入
    offset_4.find_element_by_css_selector("input[type='text']").send_keys('1-4')    # 输入DI偏移量
    offset_5 = offset_4.find_element_by_xpath("following-sibling::td[3]")
    sleep(1)
    offset_5.find_element_by_css_selector("button[class='btn btn-boxconf btn-boxconf-p']").click()      # 点击确认
    sleep(1)
    publisher = browser.find_element_by_css_selector("a.btn").click()    # 点击发布


    # pyautogui.write(['\t', '\t', '\t', '\t'])   # 4次tab选到搜索栏
    # pyperclip.copy(STATION)
    # pyautogui.hotkey('ctrl', 'v')

    # ActionChains(browser).click(elem_account).perform()
    # sleep(1)
    # pyautogui.write(ACCOUNT + '\t')
    # pyautogui.write(PASSWORD + '\t')

    # pyautogui.press('enter')        # 搜索到帅帅电气科技然后按回车
    # sleep(10)       # 等待反应
    #
    # # TODO: 选到特定的带siteid的配置连接按钮
    # elem_configure_connection = browser.find_element_by_css_selector(REGX)    # 有用，但是，可以做到在cssSelector中使用正则变量吗？

    # TODO: 开始对Edge接入进行连接的建立
    print('ok')
except:
    print('有哪步出错了。')
