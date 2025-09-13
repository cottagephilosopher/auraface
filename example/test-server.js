const WebSocket = require('ws');
const readline = require('readline');

const PORT = 10808;
let clients = new Set();

const server = new WebSocket.Server({ port: PORT });

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

server.on('connection', (ws) => {
    clients.add(ws);
    console.log(`客户端已连接。当前连接数: ${clients.size}`);
    
    ws.send('blink');
    
    ws.on('close', () => {
        clients.delete(ws);
        console.log(`客户端已断开。当前连接数: ${clients.size}`);
    });
    
    ws.on('error', (error) => {
        console.error('WebSocket错误:', error);
    });
});

function broadcastEmotion(emotion) {
    if (clients.size > 0) {
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(emotion);
            }
        });
        console.log(`已发送表情: ${emotion} (发送给 ${clients.size} 个客户端)`);
    } else {
        console.log('没有连接的客户端');
    }
}


function showHelp() {
    console.log('\n=== 表情测试服务器命令 ===');
    console.log('1 或 blink    - 发送眨眼表情动画');
    console.log('2 或 roar     - 发送咆哮表情动画');
    console.log('status        - 显示服务器状态');
    console.log('help          - 显示帮助');
    console.log('quit 或 exit  - 退出服务器');
    console.log('========================\n');
}

function showStatus() {
    console.log(`\n=== 服务器状态 ===`);
    console.log(`端口: ${PORT}`);
    console.log(`连接的客户端数: ${clients.size}`);
    console.log(`WebSocket地址: ws://localhost:${PORT}`);
    console.log('=================\n');
}

console.log(`表情测试服务器启动在端口 ${PORT}`);
console.log(`WebSocket地址: ws://localhost:${PORT}`);
console.log('请在HTML页面中将WebSocket地址替换为: ws://localhost:8080');
showHelp();

rl.on('line', (input) => {
    const command = input.trim().toLowerCase();
    
    switch(command) {
        case '1':
        case 'blink':
            broadcastEmotion('blink');
            break;
        case '2':
        case 'roar':
            broadcastEmotion('roar');
            break;
        case 'status':
            showStatus();
            break;
        case 'help':
            showHelp();
            break;
        case 'quit':
        case 'exit':
            console.log('关闭服务器...');
            server.close();
            process.exit(0);
            break;
        default:
            console.log('未知命令。输入 "help" 查看可用命令。');
    }
});

process.on('SIGINT', () => {
    console.log('\n收到中断信号，关闭服务器...');
    server.close();
    process.exit(0);
});