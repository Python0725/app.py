import itchat
import xml.etree.ElementTree as ET
import pandas as pd

# 登录微信账号
itchat.auto_login(hotReload=True)

# 获取好友列表，并打印好友列表中第一个好友的信息
friends = itchat.get_friends(update=True)
print('第一个好友的信息：', friends[0])

# 根据好友昵称查找好友
friend = itchat.search_friends(name='极轨业务&&星地通')[0]

# 从微信服务器获取聊天记录XML文件，并解析数据
chatroom_xml = itchat.get_mps()[0]['UserName'] + '_' + friend['UserName']
chatroom_msg = itchat.get_msg(chatroom_xml)

try:
    root = ET.fromstring(chatroom_msg['Content'])
except ET.ParseError as e:
    print('XML解析出错：', e)
    itchat.logout()
    exit()

data = []
for child in root.iter('msg'):
    if child.get('type') == '1':
        date, time = child.get('createtime').split('T')
        sender = child.get('fromusername')
        content = child.find('content').text
        data.append([date, time, sender, content])

# 将数据存储到DataFrame中
df = pd.DataFrame(data, columns=['日期', '时间', '发送人', '内容'])

# 按日期分组，将每组数据写入同一个Excel工作表中
writer = pd.ExcelWriter('chat_history.xlsx')
for date, group in df.groupby('日期'):
    # 将数据写入Excel工作表中
    group.to_excel(writer, index=False)
    # 添加一个空行
    writer.sheets[date].write(len(group) + 1, 0, '')
print('聊天记录已导出到Excel文件中')

# 保存Excel文件
writer.save()

# 登出微信账号
itchat.logout()
