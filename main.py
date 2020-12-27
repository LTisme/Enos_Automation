#! python3
# 用来读入json的数据来自动填表
#-*- coding: utf-8 -*-
import json
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import functions    # 导入用到的功能函数

# 这仨还是不能缺
URL = 'https://portal-lywz1.eniot.io/configuration/addstation.html?locale=zh-CN&siteid='    # 联元仪表盘网址
EDGE_URL = 'https://portal-lywz1.eniot.io/portal/#platform-asset-conf//'    # 联元Edge接入的网址
ACCOUNT = 'TSKJ'
PASSWORD = '5PcvJBNj'

os.chdir(r'F:\python_trainning_pycharm\Automate_the_Routine\Ultimate_Automation\True_Content')
with open('data.json', encoding='UTF-8') as fbj:
    data = json.load(fbj)    # 现在data就是想要的数据结构

browser = webdriver.Firefox()   # 开启火狐有头浏览器备用
browser.get(EDGE_URL)
browser.maximize_window()   # 窗口最大化，这样有利于接下去的步骤
elem_account = browser.find_element_by_css_selector("input[type='text']").send_keys(ACCOUNT)    # 这种方法可以避免输入法冲突
elem_password = browser.find_element_by_css_selector("input[type='password']").send_keys(PASSWORD)
elem_button = browser.find_element_by_css_selector("button[class='index_submit_2OPCK']").click()
sleep(5)
elem_span = browser.find_element_by_css_selector("span[class='icon-CloseModuleSelection']").click()     # 至此登录完毕，准备就绪
while True:
    try:
        if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
            continue
    except Exception as f:
        print("Message: " + str(f))
        break

FIRST_OPEN_TAG = 1
for each_station in data:
    STATION = each_station['站名']
    siteID = each_station['siteID']
    # 合成每个站点独有的DASHBOARD仪表盘网址————可以快速打开
    REAL_URL = URL + siteID
    if len(browser.window_handles) == 1:    # 若是刚开始打开，也就是第一次打开这个网址
        js = '''window.open('%s')''' % REAL_URL  # selenium中没有专门的打开新窗口的方法，是通过'window.execute_script()'来执行'js'脚本的形式来打开窗口的
        browser.execute_script(js)
        browser.switch_to.window(browser.window_handles[1])  # 选到场站信息窗口
        sleep(0.5)  # 以等待不要跳转的太快
    else:
        browser.switch_to.window(browser.window_handles[1])  # 选到场站信息窗口
        browser.get(REAL_URL)   # 打开新的站点独有的DASHBOARD仪表盘网址
        sleep(2)  # 以等待不要跳转的太快
    for each_device in each_station['信息']:
        """这个for循环单纯用来往场站信息里添加设备"""
        KitName = each_device['device_name']
        Capacity = each_device['capacity']
        RatedCurrent = each_device['rated_current']
        try_times = 1   # 以防页面卡主，取消后重新再来的允许次数——每个设备一次

        # 下面这两句也时好时坏，用pyautogui看了下似乎是坐标选择有问题，试一下别的路径选择器
        # WebDriverWait(browser, 100).until(ec.element_to_be_clickable((By.CSS_SELECTOR,
        #                                                             "button.pull-left:nth-child(1)"))).click()  # 选到添加设备按钮
        # try:
        #     kit_button = browser.find_element_by_css_selector("button.pull-left:nth-child(1)").click()  # 选到添加设备按钮
        # except:
        #     kit_button = browser.find_element_by_css_selector("button.pull-left:nth-child(1)").click()  # 再来一遍
        # 注意，必须要全屏，或者滚动到 添加设备 这个按钮出现时才能点击成功
        # ActionChains(browser).click(kit_button).perform()  # 单纯的kit_button.click也行

        sleep(3)
        bar = browser.find_elements_by_css_selector("div[class='col-md-8']")
        bar[0].find_element_by_xpath("child::button[1]").click()   # 选到添加设备按钮
        sleep(1)
        # >>>>>>>TESTING<<<<<<<<<
        selection = browser.find_element_by_css_selector("div.col-md-2:nth-child(2) > select")
        ActionChains(browser).move_to_element(selection).perform()
        selection.click()
        # >>>>>>>TESTING<<<<<<<<<
        option = browser.find_element_by_css_selector("option[value='227']").click()  # 这个直接可以选到多功能电表

        # 还需要判断——>其他信息设置这一栏是否已打开
        settings = browser.find_element_by_css_selector(
            "#devicePage > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1)")
        if settings.get_attribute('class') == 'collapse-layout-close':      # 若是关闭状态则需要点击它来打开
            settings.click()
        try:    # 还有一种情况就是就算点击了展开，里面也没有内容，这种情况发生就需要取消掉再来一次
            kit_name = browser.find_elements_by_css_selector("input[data-key='name']")[2].send_keys(KitName)
            kit_voltage = browser.find_element_by_css_selector("input[data-key='Un']").send_keys('400')  # 输入线电压
            kit_maxCurrent = browser.find_element_by_css_selector("input[data-key='maxCurrent']").send_keys(
                RatedCurrent)  # 输入额定电流
            kit_capacity = browser.find_element_by_css_selector("input[data-key='TransformerCapacity']").send_keys(
                Capacity)  # 输入容量
            kit_submit = browser.find_elements_by_css_selector("a[class='btn btn-primary eos-button-l']")[1].click()  # 提交保存
            sleep(1)
        except IndexError:      # list index out of range错误，就说明页面上“其他信息设置”这一栏瓢住了，需要取消掉，重新添加一遍来恢复
            if try_times == 1:
                try_times = 0
                # 先取消掉当前页面重新尝试一遍
                cancel_button = browser.find_element_by_css_selector(
                    "#devicePage > div:nth-child(3) > div:nth-child(2) > a:nth-child(1)")
                cancel_button.click()
                # 然后再试一遍
                WebDriverWait(browser, 100).until(ec.element_to_be_clickable((By.CSS_SELECTOR,
                                                                              "button.pull-left:nth-child(1)"))).click()  # 选到添加设备按钮
                # kit_button = browser.find_element_by_css_selector("button.pull-left:nth-child(1)").click()  # 选到添加设备按钮
                # 注意，必须要全屏，或者滚动到 添加设备 这个按钮出现时才能点击成功
                # ActionChains(browser).click(kit_button).perform()  # 单纯的kit_button.click也行
                sleep(1)
                # >>>>>>>TESTING<<<<<<<<<
                selection = browser.find_element_by_css_selector("div.col-md-2:nth-child(2) > select")
                ActionChains(browser).move_to_element(selection).perform()
                selection.click()
                # >>>>>>>TESTING<<<<<<<<<
                option = browser.find_element_by_css_selector("option[value='227']").click()  # 这个直接可以选到多功能电表

                # 还需要判断——>其他信息设置这一栏是否已打开
                settings = browser.find_element_by_css_selector(
                    "#devicePage > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1)")
                if settings.get_attribute('class') == 'collapse-layout-close':
                    settings.click()
                try:
                    kit_name = browser.find_elements_by_css_selector("input[data-key='name']")[2].send_keys(KitName)
                    kit_voltage = browser.find_element_by_css_selector("input[data-key='Un']").send_keys('400')  # 输入线电压
                    kit_maxCurrent = browser.find_element_by_css_selector("input[data-key='maxCurrent']").send_keys(
                        RatedCurrent)  # 输入额定电流
                    kit_capacity = browser.find_element_by_css_selector(
                        "input[data-key='TransformerCapacity']").send_keys(
                        Capacity)  # 输入容量
                    kit_submit = browser.find_elements_by_css_selector("a[class='btn btn-primary eos-button-l']")[
                        1].click()  # 提交保存
                    sleep(1)
                except IndexError:      # 已经尝试一遍了但还是不行，那就得跳过了
                    # 跳过设备
                    continue
            else:
                # 那么尝试次数用完了，就得跳过这个设备了
                # 需要用log日志记录一下是哪个设备这么离谱
                continue
    submit_after_addition = browser.find_elements_by_xpath("//a[contains(text(),'保存')]")[0].click()  # 最后提交以更新场站信息

    if FIRST_OPEN_TAG == 1:     # 若是第一次回到Edge接入页面，则直接切回页面就好
        browser.switch_to.window(browser.window_handles[0])  # 切换回Edge接入窗口
        iframe = browser.find_elements_by_tag_name("iframe")[0]  # 选到了iframe下
        browser.switch_to.frame(iframe)

        FIRST_OPEN_TAG = 0
        elem_inputbox = browser.find_element_by_css_selector("input[type='text']").send_keys(STATION)  # 往Edge的搜索框里输入要搜索的场站名
        # elem_loupe = browser.find_element_by_css_selector("span[class='ic_basic-input-search-icon']").click()  # 点击右侧的搜索放大镜
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break
        WebDriverWait(browser, timeout=5).until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, "span[class='ic_basic-input-search-icon']"))).click()  # 点击右侧的搜索放大镜，其实不用点放大镜也可以的
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break
        elem_configuration = browser.find_element_by_css_selector("a[href*='%s']" % siteID).click()  # 选到特定的配置按钮
        sleep(5)    # 等待5s以出结果
    else:   # 否则不是第一次打开，那就需要重新打开这个页面
        browser.switch_to.window(browser.window_handles[0])  # 首先切换回Edge接入窗口
        browser.refresh()   # 刷新页面，get()方法之所以无效是因为网址没有变动
        sleep(10)   # 等待刷新
        iframe = browser.find_elements_by_tag_name("iframe")[0]  # 选到了iframe下
        browser.switch_to.frame(iframe)
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break

        elem_inputbox = browser.find_element_by_css_selector("input[type='text']").send_keys(
            STATION)  # 往Edge的搜索框里输入要搜索的场站名
        # elem_loupe = browser.find_element_by_css_selector(
        #     "span[class='ic_basic-input-search-icon']").click()  # 点击右侧的搜索放大镜，其实不用点放大镜也可以的
        # sleep(140)
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break
        WebDriverWait(browser, timeout=20).until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, "span[class='ic_basic-input-search-icon']"))).click()  # 点击右侧的搜索放大镜，其实不用点放大镜也可以的
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break
        elem_configuration = browser.find_element_by_css_selector("a[href*='%s']" % siteID).click()  # 选到特定的配置按钮
        while True:
            try:
                if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                    continue
            except Exception as f:
                print("Message: " + str(f))
                break

    box_list = []       # 用来判断盒子是否已经存在
    port_list = []      # 用来判断下一个104转发连接该用104转发几了？——有几个端口号就有几个连接——每往里面填入一个新元素，104转发x的x就要+1
    TEMP_BOX = ""       # 暂存最新的盒子
    TEMP_LINK = ""      # 暂存最新的连接——有必要吗？
    TEMP_PORT_NUM = ""  # 暂存最新的端口号
    count = 1
    for each_device in each_station['信息']:  # 初步的打算是每做一个盒子就点击下面的连接添加设备
        """这个for循环用来往Edge接入里填信息"""
        PORT_NUM = each_device['port_num']  # 获得了端口号
        DEVICE_NAME = each_device['device_name']    # 获得了设备名
        if count == 1:
            TEMP_PORT_NUM = PORT_NUM    # 第一次直接把TEMP_PORT_NUM值赋为PORT_NUM值，然后到for循环最后再判断两者是否相等
            count = 0

        # TODO: 完成这个逻辑————那大头算是真的拿下来了
        if functions.judgement(int(PORT_NUM)) is not False:   # 获得这个端口号对应的IP，和盒子名字
            IP, BOX_SN = functions.judgement(int(PORT_NUM))
            BOX_NAME = '%s盒子' % IP  # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←这←是←后←面←要←用←到←的←身←份←证
        else:
            print("--抛出异常--或者跳过这个设备--")
            # 这里可以加个日志系统，告诉哪个站点下的哪个设备被跳过了
            continue    # 跳过这个设备

        # 判断页面上这个端口号对应的盒子是否存在
        sleep(2)    # 以等待页面加载完成
        try:
            boxes = browser.find_elements_by_css_selector("a[id*='tab']")
            [box_list.append(box.text) for box in boxes]      # 这个box_list读取当前页面的盒子的名字
        except:
            pass
        if BOX_NAME not in box_list:
            """盒子不存在，则需要建盒子---------------建盒子以后可以重构个函数"""
            # 新建盒子
            box_list.append(IP)
            sleep(3)    # 等待页面加载完成
            WebDriverWait(browser, 5).until(ec.element_to_be_clickable((
                By.CSS_SELECTOR, "button[class='dropdown btn btn-primary']"))).click()  # 点击添加盒子
            # elem_add_box = browser.find_element_by_css_selector("button[class='dropdown btn btn-primary']")
            # elem_add_box.click()  # 点击添加盒子
            elem_box_name = browser.find_element_by_css_selector("input[id='addBoxName']").send_keys(BOX_NAME)  # 输入盒子名字
            elem_box_sn = browser.find_element_by_css_selector("input[id='addBoxSN']").send_keys(BOX_SN)  # 输入对应的SN号
            elem_box_submit = browser.find_element_by_xpath(
                "// *[ @ id = 'container'] / div / div[1] / div[2] / "
                "div / div[2] / div[1] / div / div / div[3] / div / button[2]").click()  # 点击提交

            sleep(2)    # 提交之后阻塞2秒以等待
            # 在新建的盒子下新建104转发x的连接，并在新建的连接中添加设备
            boxes = browser.find_elements_by_css_selector("a[id*='tab']")
            for box in boxes:
                try:    # 防止盒子取不到text属性而报错
                    BOX_TEXT = box.text
                except:
                    continue
                if BOX_TEXT == BOX_NAME:    # 找到新建的对应的盒子，并选中该盒子
                    sleep(3)
                    box.click()
                    # box.find_element_by_xpath("parent::*").click()     # 选中对应的盒子，不能直接box.click()
                    # 在新建的盒子下新建104转发x的连接，并在新建的连接中添加设备————也可以重构成函数————已重构
                    LINK_NAME = functions.which_link(PORT_NUM, port_list)
                    functions.establish_link(browser, LINK_NAME, IP, PORT_NUM)  # 建立新连接
                    sleep(1)

                    # 在新建的连接下，点击添加设备——这个按钮
                    link = functions.find_link(browser, LINK_NAME)
                    link[0].click()
                    sleep(1)
                    functions.add_unique_device_in_link(browser, DEVICE_NAME)     # 勾选中相应的设备
                    # 然后统一设定一个变比模板，后面再来修改
                    # 或者说，读取excel的时候就进行正则判定，它应该选哪一个变比模板
                    device_template = browser.find_element_by_css_selector(
                        "option[value='4169']").click()  # 统一先选 创力800/5的模板
                    device_submit = browser.find_element_by_xpath(
                        "//*[@id='container']/div/div[1]/div[2]/div/div[3]/div/div[2]/a[2]").click()  # 点击保存
                    sleep(3)    # 阻塞3秒以防万一，因为页面回去的时候可能会加载一小会儿
                    # TODO: ZAN SHI BU NONG——还是需要有变量存着刚才做的是哪个连接下的操作，以备后面点开去修改偏移量
        else:
            """盒子存在，则不用建盒子了"""
            boxes = browser.find_elements_by_css_selector("a[id*='tab']")
            for box in boxes:
                if box.text == BOX_NAME:  # 找到对应的盒子，并点击
                    sleep(3)
                    box.click()
                    # 判断端口号是否与TEMP_PORT_NUM一致
                    if TEMP_PORT_NUM != PORT_NUM:   # 若不一致————在对应盒子下新建104转发x的连接，并在新建的连接中添加设备
                        # 在新建的盒子下新建104转发x的连接，并在新建的连接中添加设备————也可以重构成函数————已重构
                        LINK_NAME = functions.which_link(PORT_NUM, port_list)   # 获得接下来该用的连接名称
                        functions.establish_link(browser, LINK_NAME, IP, PORT_NUM)  # 建立新连接
                        sleep(1)

                        # 在新建的连接下，点击添加设备——这个按钮
                        link = functions.find_link(browser, LINK_NAME)
                        link[0].click()
                        sleep(1)
                        functions.add_unique_device_in_link(browser, DEVICE_NAME)
                        # 然后统一设定一个变比模板，后面再来修改
                        # 或者说，读取excel的时候就进行正则判定，它应该选哪一个变比模板
                        device_template = browser.find_element_by_css_selector(
                            "option[value='4169']").click()  # 统一先选 创力800/5的模板
                        device_submit = browser.find_element_by_xpath(
                            "//*[@id='container']/div/div[1]/div[2]/div/div[3]/div/div[2]/a[2]").click()  # 点击保存
                        sleep(3)  # 阻塞3秒以防万一，因为页面回去的时候可能会加载一小会儿
                        # TODO: ZAN SHI BU NONG——还是需要有变量存着刚才做的是哪个连接下的操作，以备后面点开去修改偏移量
                    else:   # 若一致————在对应盒子下的对应TEMP_LINK连接下添加设备
                        LINK_NAME = functions.which_link(PORT_NUM, port_list)
                        # 开始在已有的连接下，选择添加设备按钮
                        link = functions.find_link(browser, LINK_NAME)
                        # 对应的连接是唯一的，所以可以只选中列表的第一个元素
                        if len(link) != 0:   # 找到了对应连接
                            link[0].click()  # 之所以弄成这样，是为了避免浏览器被设置成英语就找不到元素的情况
                        else:   # 如果没有找到对应的连接，说明还得要新建这个连接
                            # LINK_NAME 在前面已经取到了
                            functions.establish_link(browser, LINK_NAME, IP, PORT_NUM)  # 建立新连接
                            sleep(1)

                            # 在刚建的连接下，点击添加唯一的设备
                            link = functions.find_link(browser, LINK_NAME)
                            link[0].click()

                        sleep(1)
                        functions.add_unique_device_in_link(browser, DEVICE_NAME)
                        # 然后统一设定一个变比模板，后面再来修改
                        # 或者说，读取excel的时候就进行正则判定，它应该选哪一个变比模板
                        device_template = browser.find_element_by_css_selector(
                            "option[value='4169']").click()  # 统一先选 创力800/5的模板
                        device_submit = browser.find_element_by_xpath(
                            "//*[@id='container']/div/div[1]/div[2]/div/div[3]/div/div[2]/a[2]")
                        device_submit.click()  # 点击保存
                        sleep(3)  # 阻塞3秒以防万一，因为页面回去的时候可能会加载一小会儿
                        # TODO: ZAN SHI BU NONG——还是需要有变量存着刚才做的是哪个连接下的操作，以备后面点开去修改偏移量


        if TEMP_PORT_NUM != PORT_NUM:   # 在for循环最后再判断两者是否相等
            TEMP_PORT_NUM = PORT_NUM
