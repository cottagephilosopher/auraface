# 表情动画展示系统

## 功能简介

这是一个基于WebSocket的实时表情动画展示系统，支持播放15帧表情动画序列，具备平滑的透明度过渡效果。

### 主要功能

- **实时表情动画播放**：支持播放15帧循环动画
- **WebSocket通信**：通过WebSocket实现实时控制
- **平滑过渡效果**：切换表情时具备1秒透明度渐变效果
- **循环播放控制**：动画播放完成后暂停3秒再重新开始
- **多表情支持**：目前支持眨眼(blink)和咆哮(roar)两种表情,表情扩展中

## 使用场景

- **直播互动**：观众通过弹幕或礼物触发主播表情动画
- **智能助手**：AI助手根据对话内容显示相应表情
- **游戏娱乐**：游戏中角色表情展示
- **教育培训**：教学课件中的互动表情展示
- **展示演示**：产品演示中的情感化展示效果

## 项目结构

```
emoji-web/
├── emotion-display.html    # 表情展示前端页面
├── test-server.js         # WebSocket测试服务器
├── package.json           # 项目依赖配置
├── images/               # 表情图片资源目录
│   ├── blink_1.png       # 眨眼动画第1帧
│   ├── blink_2.png       # 眨眼动画第2帧
│   ├── ...               # 眨眼动画第3-15帧
│   ├── roar_1.png        # 咆哮动画第1帧
│   ├── roar_2.png        # 咆哮动画第2帧
│   └── ...               # 咆哮动画第3-15帧
└── README.md
```

## 安装使用

### 1. 安装依赖

```bash
npm install
```

### 2. 启动测试服务器

```bash
npm start
```

服务器将在端口10808启动，显示如下信息：
```
表情测试服务器启动在端口 10808
WebSocket地址: ws://localhost:10808
```

### 3. 打开展示页面

在浏览器中打开 `emotion-display.html` 文件

### 4. 测试表情动画

在服务器控制台输入以下命令：

- `1` 或 `blink` - 播放眨眼表情动画
- `2` 或 `roar` - 播放咆哮表情动画
- `status` - 显示服务器状态
- `help` - 显示帮助信息
- `quit` 或 `exit` - 退出服务器

## 动画规格

- **帧数**：每个表情包含15帧图片
- **帧率**：每帧间隔100毫秒（10fps）
- **循环间隔**：动画播放完成后暂停3秒
- **过渡效果**：切换不同表情时1秒透明度渐变
- **图片格式**：PNG格式，命名规则为 `{表情名}_{帧序号}.png`

## 技术实现

- **前端**：HTML5 + CSS3 + JavaScript
- **后端**：Node.js + WebSocket (ws库)
- **通信协议**：WebSocket实时双向通信
- **动画控制**：JavaScript setInterval + setTimeout
- **视觉效果**：CSS3 opacity transition

## 扩展表情

要添加新的表情动画：

1. 在 `images/` 目录下添加15张图片：`新表情名_1.png` 到 `新表情名_15.png`
2. 在 `emotion-display.html` 中的 `emotionMap` 对象添加映射：
   ```javascript
   const emotionMap = {
       'blink': 'blink',
       'roar': 'roar',
       '新表情名': '新表情名'
   };
   ```
3. 在 `test-server.js` 中的命令处理添加新的case分支

## 注意事项

- 确保WebSocket端口8080未被占用
- 表情图片需严格按照命名规则放置
- 浏览器需支持WebSocket和CSS3 transition
- 建议使用Chrome、Firefox等现代浏览器