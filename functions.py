

def judgement(port_num):
    """用来判断端口号用的ip地址和sn号"""
    if (30002 <= port_num <= 30200) or (30402 <= port_num <= 30500)\
            or (30501 <= port_num <= 30600) or (30801 <= port_num <= 31200):
        ip = '10.65.26.143'
        sn = 'de221685-5460-4c50-80ff-3d322eb5b019'
    elif (30201 <= port_num <= 30400) or (30601 <= port_num <= 30700)\
            or (31201 <= port_num <= 32000):
        ip = '10.65.26.144'
        sn = '90829856-5781-41fe-a6d4-d1ec5f16e548'
    elif 32001 <= port_num <= 32400:
        ip = '192.168.9.74'
        sn = '2462f05b-c90a-4a92-9469-43444d0297dd'
    elif 32401 <= port_num <= 32800:
        ip = '192.168.9.83'
        sn = 'a742eaa1-7348-472b-b32d-a9f00abdbda0'
    elif 32801 <= port_num <= 33200:
        ip = '192.168.9.86'
        sn = 'da5526ba-afc0-4eae-a7a5-fcd947126c5f'
    elif 33201 <= port_num <= 33600:
        ip = '192.168.9.88'
        sn = '584a2b58-8878-4c37-9144-cd4f427c7d04'
    elif 33601 <= port_num <= 34000:
        ip = '192.168.9.89'
        sn = '5cf81848-1122-4d0c-b665-2b44f1899a13'
    elif 34001 <= port_num <= 34400:
        ip = '192.168.9.94'
        sn = 'd3af993f-3f82-45ae-85e9-d8a093db4aff'
    elif 34401 <= port_num <= 34800:
        ip = '192.168.9.95'
        sn = 'da52699e-311f-4317-a675-12d07d59151d'
    elif 34801 <= port_num <= 35200:
        ip = '192.168.9.98'
        sn = '6e562d4f-9cfd-49b4-8c30-58b5d673b97d'
    elif 35201 <= port_num <= 35600:
        ip = '192.168.9.131'
        sn = '5cc7755c-a417-4cc7-9571-172753739f0d'
    elif 35601 <= port_num <= 36000:
        ip = '192.168.9.132'
        sn = 'b2c4ce75-4d77-445f-858d-650d24b53d44'
    elif 36001 <= port_num <= 36400:
        ip = '192.168.9.133'
        sn = '53d7c2e1-066b-4a63-aff9-48234d8d423b'
    elif 36401 <= port_num <= 36800:
        ip = '192.168.9.134'
        sn = 'c349eb79-e992-4a86-bb9b-f0983b13be7f'
    elif 36801 <= port_num <= 37200:
        ip = '192.168.9.135'
        sn = 'cc7d1a27-f180-477d-a361-f8d21988633e'
    elif 37201 <= port_num <= 37600:
        ip = '192.168.9.136'
        sn = 'db88f85c-d1cf-4a20-8521-3f62e4bcc335'
    elif 37601 <= port_num <= 38000:
        ip = '192.168.9.137'
        sn = '26eb74ff-dbf1-4bcc-ab21-b9f97af7c76a'
    elif 38001 <= port_num <= 38400:
        ip = '192.168.9.138'
        sn = '36c3de54-8547-41f1-8050-357fd9e6c972'
    elif 38401 <= port_num <= 38800:
        ip = '192.168.9.139'
        sn = '5ae573b7-5919-4337-a893-c7e0ab02b3c1'
    elif 38801 <= port_num <= 39200:
        ip = '192.168.9.140'
        sn = '3727f1f3-98a3-4e6e-b26e-c32936bcd7b2'
    elif 39201 <= port_num <= 39600:
        ip = '192.168.9.141'
        sn = '903dda4d-f78a-4780-97e3-00a0ac22dfdb'
    else:
        return False
    return ip, sn


def which_link(port_num, port_list):
    """判断该用哪个连接名字来进行下一步的操作"""
    if port_num not in port_list:
        port_list.append(port_num)
        X = len(port_list)
    else:
        X = len(port_list)
    return "104转发%s" % X


def add_unique_device_in_link(browser, device_name):
    """添加设备到连接中去，用来勾选与设备名一致的设备选项,<tbody>在无设备的时候是无<tr></tr>内容的"""
    tables = browser.find_elements_by_css_selector(
        "#container > div > div.page-layout-body > div.page-layout-content > "
        "div > div:nth-child(1) > div:nth-child(2) > div > table > tbody >tr")
    for table in tables:
        if table.find_element_by_xpath("child::td[3]").text == device_name:
            table.find_element_by_xpath("child::td[1]/child::input").click()
            table.find_element_by_xpath("child::td[1]/child::input").click()
            table.find_element_by_xpath("child::td[1]/child::input").click()    # 点三次是为了，防止浏览器卡主不动


def establish_link(browser, LINK_NAME, IP, PORT_NUM):
    """用于新建连接，需要点击的是对应盒子下的添加连接按钮，否则会失败"""
    # link_add = browser.find_elements_by_css_selector("a[class='eos-link']")[1].click()  # 点击添加连接的链接——这个不对
    current_bar = browser.find_element_by_css_selector("div[class='tab-pane fade active in']")  # 找到对应盒子下的布局
    current_bar.find_element_by_xpath("child::*/child::div[2]/child::a").click()    # 这才能点击到对应的添加连接按钮
    # div[style='height: 40px; line-height: 40px;']————用这个获取到bar，然后往下倒到a儿子试试
    link_name = browser.find_element_by_css_selector("input[id='collectName']").send_keys(
        LINK_NAME)  # 连接的名字都叫104转发x，后期再对x做多端口处理
    link_mode = browser.find_element_by_css_selector(
        "option[value='TCP_SVR']").click()  # 选中TCP/IP的处理方式
    link_address = browser.find_elements_by_css_selector("input[id='ipport']")[0].send_keys(
        IP)  # 发送内网盒子ip地址
    link_port = browser.find_elements_by_css_selector("input[id='port']")[0].send_keys(
        PORT_NUM)  # 发送端口号
    link_submit = browser.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[3]/div/button[2]"
    ).click()  # 提交连接，用的绝对定位，比较繁琐


def find_link(browser, LINK_NAME):
    """首先得找到添加设备这个链接，然后往前偏移找出<span></span>用其中的内容来判断是否该点这个链接"""
    elem_filter = []
    device_add = browser.find_elements_by_css_selector("a[class='eos-link']")
    for elem in device_add:
        """这样找到了对应连接下的-添加设备-按钮"""
        try:
            if elem.find_element_by_xpath(
                    "parent::*/preceding-sibling::div[1]/span[2]").text == LINK_NAME:  # 找到了对应连接
                elem_filter.append(elem)
        except:  # 忽略找不到对象的元素
            pass
    # 对应的连接一定是第一个的，所以可以后续只选中返回的列表中的第一个元素
    return elem_filter


def wait_loading(browser):
    """iframe下有个mask页面来显示加载中，需要等它消失，才好点击下一步"""
    while True:
        try:
            if browser.find_element_by_css_selector("div[class='modal-mask modal-mask-open']"):
                continue
        except Exception as f:  # 直到页面找不到任何 open 状态的mask，才会跳出循环，否则一直等待
            print(str(f))
            break


def revise_logicNum_AI_DI(browser, LINKNAME, DEVICE_NAME, Keys, times=1):
    """修改-对应设备-的逻辑编号、AI、DI偏移量——必须要用连接名来相对找到元素"""
    AI = '%d-%d' % (78 * (times - 1), 78 * times - 1)
    DI = '%d-%d' % (4 * times - 3, 4 * times)
    link_in_active_box = browser.find_element_by_xpath(
        "//*[@class='tab-pane fade active in']//span[contains(text(),'%s')]" % LINKNAME)     # 找到<span>104转发x</span>
    open_flag = link_in_active_box.find_element_by_xpath("parent::*")  # 找到corresponding_link的父节点
    if open_flag.get_attribute('class') == 'collapse-layout-close':     # 若icon箭头是关闭的，则需要点击它来将其打开
        link_in_active_box.find_element_by_xpath("following-sibling::span[1]").click()

    # 找到corresponding_link的父父父的后第二个兄弟的子子子子——也就是<table>下的<tbody>——暂名为Z
    Z = link_in_active_box.find_element_by_xpath(
        "parent::*/parent::*/following-sibling::div[2]/child::*/child::*/child::*/child::tbody")

    # Z有几个设备就会有几个<tr>,一个<tr>下面的<td>树木是固定的,故Z.find_elements_by_tag_name("tr")——暂命为“Z-tries”
    Z_tries = Z.find_elements_by_tag_name("tr")

    # TODO: 从“Z-tries”中找到要找的设备名，然后偏移大概到第7个的following-sibling，去最后一个<td>下点击编辑按钮——这样才能打开3,4,5,6,7的<td>以供编辑
    for Z_tr in Z_tries:
        """填入都用Z_tr来偏移，因为tr是他下面所有td的父节点"""
        if Z_tr.find_element_by_xpath("child::td[2]/child::div[1]").text == DEVICE_NAME:    # 定位到符合设备名称的tr元素
            target_bar = Z_tr.find_element_by_xpath("child::td[2]/child::div[1]")
            Z_tr.find_element_by_xpath("child::td[10]/div/div[1]/a[1]/span[1]").click()     # 找到编辑按钮，点击它开始编辑

            # 根据logicNum也就是times，来填入内容！！！！注意要组合热键
            Z_tr.find_element_by_xpath("child::td[4]/div/input").send_keys(Keys.CONTROL + 'a')    # 找到对应逻辑编号元素，使用全选
            Z_tr.find_element_by_xpath("child::td[4]/div/input").send_keys(times)   # 输入逻辑编号

            Z_tr.find_element_by_xpath("child::td[6]/div/input").send_keys(Keys.CONTROL + 'a')    # 找到对应AI元素，使用全选
            Z_tr.find_element_by_xpath("child::td[6]/div/input").send_keys(AI)  # 输入AI偏移量

            Z_tr.find_element_by_xpath("child::td[7]/div/input").send_keys(Keys.CONTROL + 'a')  # 找到对应DI元素，使用全选
            Z_tr.find_element_by_xpath("child::td[7]/div/input").send_keys(DI)  # 输入DI偏移量

            # 不要忘了填完后要再次点击确认按钮来保存刚修改的信息——元素已变化，变成了原按钮的父/父/following-sibling的第一个button儿子按钮了
            #  ，函数运行完后要调用一下functions.wait_loading(browser)来等待mask消失
            Z_tr.find_element_by_xpath("child::td[10]/div/div[2]/button[1]").click()    # 点击确定按钮


def regex(re, target, manufacturer, CT, PT='1'):
    """各个不同厂家所用的正则判定"""
    if manufacturer == '南德电气' and PT != '1':
        REGEX = re.compile(r'^(.*)(%s)(.*)(%s)(.*)(%s)' % (manufacturer, PT, CT))      # 南德电气用的正则
    elif manufacturer == '南德电气' and PT == '1':
        REGEX = re.compile(r'^(.*)(%s)(.*)(%s)' % ('创力', CT))  # 南德电气无PT用的正则——与创力一样
    elif manufacturer != '南德电气' and PT != '1':
        REGEX = re.compile(r'^(.*)(%s)(.*)(%s)(.*)(PT%s)' % (manufacturer, CT, PT))
        # 针对佳和带PT的，即除南德电气外有PT的肯定以PT变比结尾，且带PT二字
    else:
        REGEX = re.compile(r'^(.*)(%s)(.*)(%s)' % (manufacturer, CT))  # 佳和、创力无PT的都在这，肯定已CT变比结尾，但不带CT二字
    if REGEX.match(target):
        print(f'匹配成功')
        return True
    else:
        print(f'匹配失败')
        return False


if __name__ == '__main__':
    import re
    model = '创力104转发YC78_1500/5 (v1.0)'
    # 试验成功的话，所以后续只用把model不断的循环为option的文本值就行了
    regex(re, model, '创力', '1500/5', '1')
