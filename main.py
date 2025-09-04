#!/usr/bin/env python3
"""
Robot Eye Expression System - Main Program
主程序文件，负责初始化Pygame，管理主循环和事件处理
"""
import pygame
import sys
from state_machine import StateMachine
from animations import AnimationManager

class RobotEyes:
    def __init__(self):
        """初始化机器人眼睛系统"""
        # 显示器配置
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 480
        self.FPS = 60
        self.BLACK = (0, 0, 0)
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Robot Eyes - AuraFace")
        self.clock = pygame.time.Clock()
        
        # 初始化系统组件
        self.animation_manager = AnimationManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.state_machine = StateMachine(self.animation_manager)
        
        # 运行状态
        self.running = True
        
    def handle_events(self):
        """处理键盘事件和系统事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # 键盘控制状态切换
                key_to_state = {
                    pygame.K_h: 'happy',         # H键 - 开心
                    pygame.K_s: 'surprised',     # S键 - 惊讶  
                    pygame.K_c: 'confused',      # C键 - 困惑
                    pygame.K_w: 'wink',          # W键 - 眨眼
                    pygame.K_l: 'look_left',     # L键 - 向左看
                    pygame.K_r: 'look_right',    # R键 - 向右看
                    pygame.K_u: 'look_up',       # U键 - 向上看
                    pygame.K_d: 'look_down',     # D键 - 向下看
                    pygame.K_i: 'idle',          # I键 - 返回空闲状态
                    
                    # 新增创意表情控制
                    pygame.K_j: 'joy',           # J键 - 大笑狂欢
                    pygame.K_t: 'thinking',      # T键 - 思考困惑  
                    pygame.K_a: 'angry',         # A键 - 生气愤怒
                    pygame.K_z: 'sleepy',        # Z键 - 疲惫瞌睡
                    pygame.K_x: 'surprised_mouth', # X键 - 带嘴巴惊讶
                    
                    # 全新的10个多样化表情控制
                    pygame.K_q: 'sadness',       # Q键 - 悲伤难过
                    pygame.K_f: 'furious',       # F键 - 狂怒咆哮
                    pygame.K_y: 'shy',           # Y键 - 害羞腼腆
                    pygame.K_m: 'mischievous',   # M键 - 恶作剧狡猾
                    pygame.K_b: 'bored',         # B键 - 无聊不耐烦
                    pygame.K_e: 'excited',       # E键 - 兴奋期待
                    pygame.K_n: 'fear',          # N键 - 恐惧害怕
                    pygame.K_o: 'focused',       # O键 - 专注思考
                    pygame.K_p: 'puzzled',       # P键 - 迷惑困惑
                    pygame.K_v: 'triumphant',    # V键 - 胜利得意
                    
                    pygame.K_ESCAPE: None        # ESC键 - 退出
                }
                
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in key_to_state:
                    new_state = key_to_state[event.key]
                    if new_state:
                        self.state_machine.change_state(new_state)
    
    def update(self):
        """更新游戏状态"""
        self.state_machine.update()
    
    def draw(self):
        """绘制当前帧"""
        # 清屏为黑色
        self.screen.fill(self.BLACK)
        
        # 获取当前动画帧并绘制
        current_frame = self.state_machine.get_current_frame()
        if current_frame:
            self.screen.blit(current_frame, (0, 0))
        
        # 刷新显示
        pygame.display.flip()
    
    def run(self):
        """主循环"""
        print("🤖 Robot Eyes System Started!")
        print("Basic Controls:")
        print("H - Happy, S - Surprised, C - Confused, W - Wink")
        print("L - Look Left, R - Look Right, U - Look Up, D - Look Down")
        print("I - Idle, ESC - Exit")
        print()
        print("🎭 Creative Expressions:")
        print("J - Joy (Laughter), T - Thinking (Question marks)")
        print("A - Angry (Frown), Z - Sleepy (ZZZ), X - Surprised (with mouth)")
        print()
        print("🌟 Advanced Emotions:")
        print("Q - Sadness (Teardrops), F - Furious (Vibration), Y - Shy (Hand cover)")
        print("M - Mischievous (Wink), B - Bored (Yawn), E - Excited (Hearts)")
        print("N - Fear (Trembling), O - Focused (Spotlight), P - Puzzled (Eye chaos)")
        print("V - Triumphant (Crown/Trophy)")
        print("-" * 60)
        
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新状态
            self.update()
            
            # 绘制画面
            self.draw()
            
            # 控制帧率
            self.clock.tick(self.FPS)
        
        # 清理资源
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # 创建并运行机器人眼睛系统
    robot_eyes = RobotEyes()
    robot_eyes.run()