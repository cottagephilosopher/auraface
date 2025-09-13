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

- **智能助手**：AI助手根据对话内容显示相应表情
- **游戏娱乐**：游戏中角色表情展示
- **教育培训**：教学课件中的互动表情展示
- **展示演示**：产品演示中的情感化展示效果

## 项目结构

```
emoji-web/
├── emotion-display.html    # 表情展示前端页面（核心组件）
├── images/                # 表情图片资源目录
│   ├── blink_1.png        # 眨眼动画第1帧
│   ├── blink_2.png        # 眨眼动画第2帧
│   ├── ...                # 眨眼动画第3-15帧
│   ├── roar_1.png         # 咆哮动画第1帧
│   ├── roar_2.png         # 咆哮动画第2帧
│   └── ...                # 咆哮动画第3-15帧
├── example/               # WebSocket调用示例
│   ├── test-server.js     # 示例WebSocket服务器
│   ├── package.json       # 示例项目依赖
│   └── node_modules/      # 示例项目依赖包
└── README.md
```

## 核心组件

本项目的核心是 `emotion-display.html` 文件，它是一个独立的表情动画展示组件，可以集成到任何项目中。

### 核心功能
- 通过WebSocket接收表情指令
- 自动播放15帧表情动画序列
- 支持平滑的透明度过渡效果
- 循环播放控制（播放完成后暂停3秒）

### 集成方法

1. 将 `emotion-display.html` 和 `images/` 目录复制到你的项目中
2. 修改 `emotion-display.html` 中的WebSocket连接地址：
   ```javascript
   websocket = new WebSocket('ws://your-server:your-port');
   ```
3. 通过WebSocket发送表情指令：`blink`、`roar` 等

## WebSocket API

向WebSocket服务器发送以下文本消息来控制表情：

- `blink` - 播放眨眼表情动画
- `roar` - 播放咆哮表情动画

更多表情可通过添加相应图片资源扩展。

## 示例演示

`example/` 目录提供了一个完整的WebSocket调用示例，演示如何与表情展示组件交互。

### 运行示例

1. **进入示例目录**：
   ```bash
   cd example
   ```

2. **安装示例依赖**：
   ```bash
   npm install
   ```

3. **启动示例服务器**：
   ```bash
   npm start
   ```

4. **打开展示页面**：
   在浏览器中打开根目录的 `emotion-display.html` 文件

5. **测试表情动画**：
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

1. **添加图片资源**：在 `images/` 目录下添加15张图片：`新表情名_1.png` 到 `新表情名_15.png`

2. **更新表情映射**：在 `emotion-display.html` 中的 `emotionMap` 对象添加映射：
   ```javascript
   const emotionMap = {
       'blink': 'blink',
       'roar': 'roar',
       '新表情名': '新表情名'
   };
   ```

3. **更新服务器端**（可选）：如果使用示例服务器，在 `example/test-server.js` 中添加相应的命令处理

## 项目定位

这是一个**可复用的表情动画展示组件**，而不是一个完整的应用程序。`example/` 目录仅提供WebSocket调用的参考实现，实际使用时你需要将核心组件集成到自己的项目中，并实现相应的WebSocket服务器来发送表情指令。

## 注意事项

- 确保WebSocket端口10808未被占用
- 表情图片需严格按照命名规则放置
- 浏览器需支持WebSocket和CSS3 transition
- 建议使用Chrome、Firefox等现代浏览器