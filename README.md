# ZhangShell机器人
### 简介
这个机器人可以让你在HackChat系列聊天室内执行Shell，可以让更多人学习Shell
### 开始使用
先修改config.json文件，键值意义如下：
- `url` 机器人的WebSocket地址，这里提供的是 hack.chat 聊天室的WebSocket地址
- `owner` 机器人主人的识别码，该用户拥有机器人的最高权限
- `op` 授权使用本机器人的部分功能的用户
- `nick` 机器人加入聊天室时使用的昵称
- `prefix` 规定什么符号可以触发机器人
- `channel` 设置机器人要加入哪个频道（房间），这里提供的是 `your-channel`
- `bannedcmd` 禁止执行的Shell命令

您应该修改：`url`、`owner`、`nick`、`prefix`、`channel`  
对于 `bannedcmd`，我们默认是禁止执行包含 `main.py` 和 `config.json` 的命令。

### 机器人功能  
- `help` 命令用于查看帮助
- `shell <Shell代码>` 执行Shell命令
- `restart` 重启机器人
- `add <目标用户的识别码>` 添加一个允许使用本机器人的用户 **只有机器人主人才能执行**
- `del <目标用户的识别码>` 删除一个允许使用本机器人的用户 **只有机器人主人才能执行**
- `listop` 查看所有允许使用本机器人的用户
- `ban <命令名称>` 禁止执行指定的Shell命令 **但是机器人主人还是可以执行这些命令** **只有机器人主人才能执行**
- `unban <命令名称>` 取消禁止执行指定的Shell命令 **只有机器人主人才能执行**
- `listban` 查看所有被禁止执行的Shell命令

### 安全提示  
由于机器人放到了聊天室里面，所以许多人**都可以通过机器人在你的计算机上执行命令**。  
因此，我们建议您不给机器人太高的权限，例如root和sudo。  
此外，我们不建议您给机器人**设置识别码**。  

### 疑难解答  
Q: 为什么我发送命令机器人不会回复？  
A: 这可能是因为你没有被授权使用本机器人。如果您是机器人的主人，请检查 `config.json` 里面的 `owner` 键值是否正确。  

Q: 为什么机器人在执行命令的时候会提示编码错误？  
A: 这个错误多半是由于Windows10的编码问题导致的，我们建议您把机器人转移到Linux计算机上。  

Q: 为什么我可以执行被禁止执行的Shell命令？  
A: 那是因为你是机器人的主人，你可以执行任何Shell命令，包括 `rm -rf /*`，前提是机器人有root权限。

Q: 什么是Shell？  
A: woc，你连Shell都不知道？请立刻删除本机器人，然后别玩了。

Q: 这个机器人是怎么诞生的？  
A: 2022年9月，[zzChumo](https://github.com/zzChumo)委托小张制作了这个机器人。  

# 重要通知  
由于小张对HC以及其衍生聊天室的失望（ https://blog.mrzhang365.cf/2023/01/02/cs-1/ ），他决定停止更新与HC及其衍生聊天室有关项目。
