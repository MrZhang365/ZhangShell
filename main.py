import websocket
import os
import json
import sys
import _thread as thread
import traceback
import requests

class client:
    def __init__(self):
        self.ver = '1.2'
        self.config = self.__read_json('config.json')
        self.ws = websocket.create_connection(self.config['url'])
        self.on = {}
        self.token = self.config['token']
        self.__send({'cmd':'join','channel':self.config['channel'],'nick':self.config['nick']})
        self.chat(f'云电脑机器人准备就绪。\n机器人所有者的识别码：{self.config["owner"]}\n授权使用本机器人部分功能的用户：{str(self.config["op"])}\n禁止执行的命令：{str(self.config["bannedcmd"])}\n要查看帮助，请发送：`{self.config["prefix"]}help`\n#### 仅接收授权用户的信息\n###### Made by [MrZhang365](https://mrzhang365.github.io/)')
        got = requests.get(f'https://onlineservice.zhangsoft.cf/zhangshell?ver={self.ver}&token={self.token}').json()
        result = '小张软件云服务提示：\n'
        if got['ver_msg']:
            result += got['ver_msg']+'\n'
        if got['token_msg']:
            result += got['token_msg']
        self.chat(result)
    def __send(self,packet):
        #print(packet)
        self.ws.send(json.dumps(packet))
    def __read_json(self,file):
        f = open(file,'r')
        return json.loads(f.read())
    def write_json(self,file,dict):
        f = open(file,'w')
        f.write(json.dumps(dict))
        f.close()
    def chat(self,text):
        self.__send({'cmd':'chat','text':text})
    def whisper(self,nick,text):
        self.__send({'cmd':'whisper','nick':nick,'text':text})
    def listen(self):
        while True:
            result = json.loads(self.ws.recv())
            #print(result)
            if result['cmd'] not in self.on:
                continue
            self.on[result['cmd']](self,result)


def run(command,robot):
    try:
        fd = os.popen(command)
        output = fd.read()
        fd.close()
        robot.chat('成功执行 `{}` 命令，终端输出：\n```shell\n{}\n```'.format(command,output))
    except:
        robot.chat('机器人执行shell代码时出现错误！详细信息：{}'.format(traceback.format_exc()))
    return 0
def restart():
    py=sys.executable
    os.execl(py,py,*sys.argv)

def on_message(robot,result):
    global restart_time
    if result['nick'] == robot.config['nick']:return 0
    trip = ''
    if 'trip' not in result:
        trip = ''
    else:
        trip = result['trip']
    level = 0 #0为普通用户 1为授权用户（op） 2为机器人所有者
    if trip == robot.config['owner']:
        level = 2
    elif trip in robot.config['op']:
        level = 1
    if level == 0:
        return 0
    msg = result['text']
    if msg[0] != robot.config['prefix']:
        return 0
    cmdlist = msg.split()
    new_str = cmdlist[0][1:]
    cmdlist[0] = new_str
    if cmdlist[0] == 'restart':
        restart()
    elif cmdlist[0] == 'shell':
        if len(cmdlist) < 2:
            robot.chat('所以我执行了个锤子？')
            return 0
        command = msg[7:]
        for i in robot.config['bannedcmd']:
            if i in command.split() and level != 2:
                robot.chat('抱歉，目前不允许使用 `{}` 命令。'.format(i))
                return 0
        thread.start_new_thread(run,(command,robot))
    elif cmdlist[0] == 'add':
        if level != 2:
            return 0
        if len(cmdlist) != 2:
            robot.chat('参数错误，请重试。')
            return 0
        if cmdlist[1] in robot.config['op']:
            robot.chat('这个用户已经存在了，无需重复操作。')
            return 0
        robot.config['op'].append(cmdlist[1])
        robot.write_json('config.json',robot.config)
        robot.chat('已将 {} 添加到授权用户列表中。'.format(cmdlist[1]))
    elif cmdlist[0] == 'ban':
        if level != 2:
            return 0
        if len(cmdlist) != 2:
            robot.chat('参数错误，请重试。')
            return 0
        if cmdlist[1] in robot.config['bannedcmd']:
            robot.chat('这个命令已经被禁止执行了，无需重复操作。')
            return 0
        robot.config['bannedcmd'].append(cmdlist[1])
        robot.write_json('config.json',robot.config)
        robot.chat('已禁止执行 {} 命令。'.format(cmdlist[1]))
    elif cmdlist[0] == 'unban':
        if level != 2:
            return 0
        if len(cmdlist) != 2:
            robot.chat('参数错误，请重试。')
            return 0
        if cmdlist[1] not in robot.config['bannedcmd']:
            robot.chat('这个命令没有被禁止执行，无需操作。')
            return 0
        robot.config['bannedcmd'].remove(cmdlist[1])
        robot.write_json('config.json',robot.config)
        robot.chat('已允许执行 {} 命令。'.format(cmdlist[1]))
    elif cmdlist[0] == 'listban':
        robot.chat('目前禁止执行以下命令：{}'.format(str(robot.config['bannedcmd'])))
    elif cmdlist[0] == 'del':
        if level != 2:
            return 0
        if len(cmdlist) != 2:
            robot.chat('参数错误，请重试。')
            return 0
        if cmdlist[1] not in robot.config['op']:
            robot.chat('这个用户不在授权列表中，无需操作。')
            return 0
        robot.config['op'].remove(cmdlist[1])
        robot.write_json('config.json',robot.config)
        robot.chat('已将 {} 移出授权用户列表。'.format(cmdlist[1]))
    elif cmdlist[0] == 'listop':
        robot.chat('目前授权以下用户使用本机器人：{}'.format(str(robot.config['op'])))
    elif cmdlist[0] == 'help':
        robot.whisper(result['nick'],'''.
| 命令名称 | 说明 |
|-:|:-|
|help|查看帮助|
|shell|执行shell代码|
|restart|重启机器人|
|add|添加授权用户|
|del|删除授权用户|
|ban|禁止执行某个命令|
|unban|允许执行某个命令|
|listban|查看所有被禁止执行的命令|
|listop|查看所有授权的用户|

要执行机器人命令，请在命令前面加上前缀：`{}`'''.format(robot.config['prefix']))
bot = client()
bot.on.update({'chat':on_message})
bot.listen()
