

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

