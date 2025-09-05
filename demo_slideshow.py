#!/usr/bin/env python3
"""
Robot Eye Expression Demo Slideshow
自动展示所有25个表情的幻灯片演示系统
每个表情持续2秒，带有平滑过渡效果
"""
import pygame
import sys
import time
from state_machine import StateMachine, EyeState
from animations import AnimationManager

class ExpressionSlideshow:
    def __init__(self):
        """初始化表情幻灯片演示系统"""
        # 显示器配置
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 480
        self.FPS = 60
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (100, 150, 255)
        
        # 初始化Pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("AuraFace - Expression Slideshow Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 初始化系统组件
        self.animation_manager = AnimationManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.state_machine = StateMachine(self.animation_manager)
        
        # 演示控制
        self.running = True
        self.current_expression_index = 0
        self.last_switch_time = time.time()
        self.expression_duration = 2.5  # 每个表情持续2.5秒，为过渡留出时间
        self.is_paused = False
        
        # 所有表情列表（按逻辑分组排序）
        self.expressions = [
            # 基础表情
            {'state': 'idle', 'name': 'Idle', 'description': '空闲状态 - 基础表情'},
            {'state': 'blink', 'name': 'Blink', 'description': '眨眼 - 自然眨眼动作'},
            
            # 基本情感
            {'state': 'happy', 'name': 'Happy', 'description': '开心 - 弯月眼睛'},
            {'state': 'surprised', 'name': 'Surprised', 'description': '惊讶 - 眼睛放大'},
            {'state': 'confused', 'name': 'Confused', 'description': '困惑 - 左右扫视'},
            {'state': 'wink', 'name': 'Wink', 'description': '眨眼 - 单眼眨眼'},
            
            # 方向性表情
            {'state': 'look_left', 'name': 'Look Left', 'description': '向左看'},
            {'state': 'look_right', 'name': 'Look Right', 'description': '向右看'},
            {'state': 'look_up', 'name': 'Look Up', 'description': '向上看'},
            {'state': 'look_down', 'name': 'Look Down', 'description': '向下看'},
            
            # 创意表情
            {'state': 'joy', 'name': 'Joy', 'description': '狂欢 - 大笑 + 星星'},
            {'state': 'thinking', 'name': 'Thinking', 'description': '思考 - 扫视 + 问号'},
            {'state': 'angry', 'name': 'Angry', 'description': '生气 - 眉毛 + 震动'},
            {'state': 'sleepy', 'name': 'Sleepy', 'description': '瞌睡 - 半闭眼 + Z符号'},
            {'state': 'surprised_mouth', 'name': 'Surprised+', 'description': '惊讶 - 大眼 + O嘴'},
            
            # 高级情感
            {'state': 'sadness', 'name': 'Sadness', 'description': '悲伤 - 下垂眼 + 泪珠'},
            {'state': 'furious', 'name': 'Furious', 'description': '狂怒 - 三角眼 + 闪电'},
            {'state': 'shy', 'name': 'Shy', 'description': '害羞 - 手遮眼 + 偷看'},
            {'state': 'mischievous', 'name': 'Mischievous', 'description': '恶作剧 - 眨眼 + 挑眉'},
            {'state': 'bored', 'name': 'Bored', 'description': '无聊 - 眼皮下垂 + 哈欠'},
            {'state': 'excited', 'name': 'Excited', 'description': '兴奋 - 跳动 + 心形'},
            {'state': 'fear', 'name': 'Fear', 'description': '恐惧 - 椭圆眼 + 颤抖'},
            {'state': 'focused', 'name': 'Focused', 'description': '专注 - 八字眉 + 聚光'},
            {'state': 'puzzled', 'name': 'Puzzled', 'description': '迷惑 - 眼球乱动 + 问号'},
            {'state': 'triumphant', 'name': 'Triumphant', 'description': '胜利 - 点头 + 皇冠'}
        ]
        
        print(f"🎭 表情幻灯片演示启动!")
        print(f"📊 总共 {len(self.expressions)} 个表情")
        print(f"⏱️  每个表情持续 {self.expression_duration} 秒")
        print("🎮 控制键:")
        print("   空格键 - 暂停/继续")
        print("   左/右箭头 - 手动切换")
        print("   ESC - 退出")
        print("=" * 50)
        
        # 开始第一个表情
        self._switch_to_expression(0)
    
    def _switch_to_expression(self, index):
        """切换到指定表情"""
        if 0 <= index < len(self.expressions):
            self.current_expression_index = index
            expression = self.expressions[index]
            
            print(f"🎭 [{index + 1:2d}/{len(self.expressions):2d}] {expression['name']} - {expression['description']}")
            
            # 切换状态机到新表情
            self.state_machine.change_state(expression['state'])
            self.last_switch_time = time.time()
    
    def _next_expression(self):
        """切换到下一个表情"""
        next_index = (self.current_expression_index + 1) % len(self.expressions)
        self._switch_to_expression(next_index)
    
    def _previous_expression(self):
        """切换到上一个表情"""
        prev_index = (self.current_expression_index - 1) % len(self.expressions)
        self._switch_to_expression(prev_index)
    
    def handle_events(self):
        """处理键盘事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # 暂停/继续
                    self.is_paused = not self.is_paused
                    if not self.is_paused:
                        self.last_switch_time = time.time()  # 重置计时
                    print(f"⏸️  {'暂停' if self.is_paused else '继续'}")
                elif event.key == pygame.K_LEFT:
                    # 手动切换到上一个表情
                    self._previous_expression()
                elif event.key == pygame.K_RIGHT:
                    # 手动切换到下一个表情
                    self._next_expression()
    
    def update(self):
        """更新演示状态"""
        # 更新状态机
        self.state_machine.update()
        
        # 自动切换表情（如果没有暂停）
        if not self.is_paused:
            current_time = time.time()
            if current_time - self.last_switch_time >= self.expression_duration:
                self._next_expression()
    
    def _draw_progress_bar(self):
        """绘制进度条"""
        if self.is_paused:
            return
            
        # 计算当前表情的进度
        elapsed = time.time() - self.last_switch_time
        progress = min(elapsed / self.expression_duration, 1.0)
        
        # 绘制进度条背景
        bar_width = 600
        bar_height = 8
        bar_x = (self.SCREEN_WIDTH - bar_width) // 2
        bar_y = self.SCREEN_HEIGHT - 60
        
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        
        # 绘制进度
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(self.screen, self.BLUE, (bar_x, bar_y, progress_width, bar_height))
    
    def _draw_info_panel(self):
        """绘制信息面板"""
        current_expression = self.expressions[self.current_expression_index]
        
        # 表情名称
        name_text = self.font.render(f"{current_expression['name']}", True, self.WHITE)
        name_rect = name_text.get_rect(center=(self.SCREEN_WIDTH // 2, 50))
        self.screen.blit(name_text, name_rect)
        
        # 表情描述
        desc_text = self.small_font.render(current_expression['description'], True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(self.SCREEN_WIDTH // 2, 80))
        self.screen.blit(desc_text, desc_rect)
        
        # 进度信息
        progress_text = self.small_font.render(
            f"{self.current_expression_index + 1} / {len(self.expressions)}", 
            True, (150, 150, 150)
        )
        progress_rect = progress_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(progress_text, progress_rect)
        
        # 暂停提示
        if self.is_paused:
            pause_text = self.font.render("⏸️ PAUSED", True, (255, 200, 100))
            pause_rect = pause_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 100))
            self.screen.blit(pause_text, pause_rect)
        
        # 控制提示
        control_text = self.small_font.render("SPACE=暂停 ←/→=切换 ESC=退出", True, (120, 120, 120))
        control_rect = control_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 10))
        self.screen.blit(control_text, control_rect)
    
    def draw(self):
        """绘制当前帧"""
        # 清屏为黑色
        self.screen.fill(self.BLACK)
        
        # 获取当前动画帧并绘制
        current_frame = self.state_machine.get_current_frame()
        if current_frame:
            self.screen.blit(current_frame, (0, 0))
        
        # 绘制信息面板
        self._draw_info_panel()
        
        # 绘制进度条
        self._draw_progress_bar()
        
        # 刷新显示
        pygame.display.flip()
    
    def run(self):
        """主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新状态
            self.update()
            
            # 绘制画面
            self.draw()
            
            # 控制帧率
            self.clock.tick(self.FPS)
        
        print("\n🎭 表情演示结束")
        print(f"✅ 成功展示了 {len(self.expressions)} 个平滑表情!")
        
        # 清理资源
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # 创建并运行表情幻灯片演示
    slideshow = ExpressionSlideshow()
    slideshow.run()