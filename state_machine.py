#!/usr/bin/env python3
"""
Robot Eye State Machine Module
负责管理机器人眼睛的各种状态转换和动画播放逻辑
"""
import time
import random
from enum import Enum

class EyeState(Enum):
    """眼睛状态枚举"""
    IDLE = "idle"
    HAPPY = "happy"
    SURPRISED = "surprised"
    CONFUSED = "confused"
    WINKING = "wink"
    LOOKING_LEFT = "look_left"
    LOOKING_RIGHT = "look_right"
    LOOKING_UP = "look_up"
    LOOKING_DOWN = "look_down"
    BLINKING = "blink"
    
    # 新增的创意表情状态
    JOY = "joy"                    # 大笑/狂欢
    THINKING = "thinking"          # 思考/困惑
    ANGRY = "angry"               # 生气/愤怒
    SLEEPY = "sleepy"             # 疲惫/瞌睡
    SURPRISED_MOUTH = "surprised_mouth"  # 带嘴巴的惊讶
    
    # 全新的10个多样化表情状态
    SADNESS = "sadness"           # 悲伤/难过 - 下垂眼睛+泪滴
    FURIOUS = "furious"           # 愤怒/咆哮 - 倒三角眼+锯齿嘴
    SHY = "shy"                   # 害羞/腼腆 - 手遮眼+偷看
    MISCHIEVOUS = "mischievous"   # 恶作剧/狡猾 - 眨眼+挑眉
    BORED = "bored"               # 无聊/不耐烦 - 打哈欠+眼皮下垂
    EXCITED = "excited"           # 兴奋/期待 - 跳动+心形图标
    FEAR = "fear"                 # 恐惧/害怕 - 大椭圆眼+抖动
    FOCUSED = "focused"           # 思考/专注 - 八字眉+聚光灯
    PUZZLED = "puzzled"           # 困惑/迷惑 - 眼球不同方向
    TRIUMPHANT = "triumphant"     # 胜利/得意 - 点头+皇冠图标

class StateMachine:
    def __init__(self, animation_manager):
        """初始化状态机"""
        self.animation_manager = animation_manager
        
        # 当前状态
        self.current_state = EyeState.IDLE
        self.previous_state = EyeState.IDLE
        
        # 动画控制
        self.current_animation = []
        self.animation_frame_index = 0
        self.animation_start_time = time.time()
        self.frame_duration = 1.0 / 15.0  # 15fps for animations
        
        # 自动行为控制（在IDLE状态下）
        self.last_auto_blink = time.time()
        self.last_micro_movement = time.time()
        self.auto_blink_interval = random.uniform(3, 8)  # 随机眨眼间隔
        self.micro_movement_interval = random.uniform(0.5, 2.0)  # 微动间隔
        
        # 状态持续时间（某些状态会自动返回IDLE）
        self.state_duration = {
            EyeState.HAPPY: 3.0,
            EyeState.SURPRISED: 0.8,            # 惊讶11帧 ≈ 0.73秒 + 缓冲
            EyeState.CONFUSED: 4.0,
            EyeState.WINKING: 1.0,
            EyeState.LOOKING_LEFT: 2.0,
            EyeState.LOOKING_RIGHT: 2.0,
            EyeState.LOOKING_UP: 2.0,
            EyeState.LOOKING_DOWN: 2.0,
            EyeState.BLINKING: 0.8,
            
            # 新增表情的持续时间（基于动画帧数和15fps播放速度）
            EyeState.JOY: 1.5,              # 大笑21帧 ≈ 1.4秒 + 缓冲
            EyeState.THINKING: 1.5,         # 思考21帧 ≈ 1.4秒 + 缓冲
            EyeState.ANGRY: 1.5,            # 生气21帧 ≈ 1.4秒 + 缓冲
            EyeState.SLEEPY: 8.0,           # 瞌睡持续8秒（保持原有）
            EyeState.SURPRISED_MOUTH: 3.0,  # 带嘴巴惊讶持续3秒（保持原有）
            
            # 全新的10个多样化表情持续时间
            EyeState.SADNESS: 3.0,          # 悲伤3秒（泪滴动画）
            EyeState.FURIOUS: 2.5,          # 狂怒2.5秒（强烈抖动）
            EyeState.SHY: 2.0,              # 害羞2秒（偷看动作）
            EyeState.MISCHIEVOUS: 1.5,      # 恶作剧1.5秒（快速眨眼）
            EyeState.BORED: 4.0,            # 无聊4秒（慢动作）
            EyeState.EXCITED: 2.0,          # 兴奋2秒（快节奏）
            EyeState.FEAR: 3.0,             # 恐惧3秒（持续颤抖）
            EyeState.FOCUSED: 3.5,          # 专注3.5秒（静止凝视）
            EyeState.PUZZLED: 3.0,          # 迷惑3秒（眼球乱动）
            EyeState.TRIUMPHANT: 2.5        # 胜利2.5秒（点头+图标）
        }
        
        self.state_start_time = time.time()
        
        # 初始化为IDLE状态
        self._load_idle_state()
    
    def change_state(self, new_state_name):
        """改变状态"""
        try:
            # 将字符串转换为枚举
            if isinstance(new_state_name, str):
                new_state = EyeState(new_state_name.lower())
            else:
                new_state = new_state_name
            
            # 如果状态没有变化，则忽略
            if new_state == self.current_state:
                return
            
            print(f"State change: {self.current_state.value} -> {new_state.value}")
            
            # 保存前一个状态
            self.previous_state = self.current_state
            self.current_state = new_state
            
            # 重置状态时间
            self.state_start_time = time.time()
            
            # 加载新状态的动画
            self._load_state_animation(new_state)
            
        except ValueError:
            print(f"Warning: Unknown state '{new_state_name}', staying in {self.current_state.value}")
    
    def _load_state_animation(self, state):
        """加载指定状态的动画"""
        animation_name = state.value
        self.current_animation = self.animation_manager.get_animation(animation_name)
        self.animation_frame_index = 0
        self.animation_start_time = time.time()
    
    def _load_idle_state(self):
        """加载空闲状态"""
        self.current_animation = self.animation_manager.get_animation('idle')
        self.animation_frame_index = 0
        self.animation_start_time = time.time()
    
    def _should_return_to_idle(self):
        """检查是否应该返回到IDLE状态"""
        if self.current_state == EyeState.IDLE:
            return False
        
        # 检查状态持续时间
        if self.current_state in self.state_duration:
            elapsed = time.time() - self.state_start_time
            return elapsed >= self.state_duration[self.current_state]
        
        return False
    
    def _handle_idle_behaviors(self):
        """处理IDLE状态下的自动行为"""
        current_time = time.time()
        
        # 自动眨眼
        if current_time - self.last_auto_blink >= self.auto_blink_interval:
            self.change_state(EyeState.BLINKING)
            self.last_auto_blink = current_time
            self.auto_blink_interval = random.uniform(3, 8)  # 重新设置随机间隔
            return
        
        # 微小运动
        if current_time - self.last_micro_movement >= self.micro_movement_interval:
            # 生成带微小运动的新帧
            new_frame = self.animation_manager.get_idle_frame_with_micro_movement()
            self.current_animation = [new_frame]
            self.animation_frame_index = 0
            self.last_micro_movement = current_time
            self.micro_movement_interval = random.uniform(0.5, 2.0)  # 重新设置随机间隔
    
    def update(self):
        """更新状态机"""
        current_time = time.time()
        
        # 检查是否需要返回IDLE状态
        if self._should_return_to_idle():
            self.change_state(EyeState.IDLE)
            return
        
        # 如果在IDLE状态，处理自动行为
        if self.current_state == EyeState.IDLE:
            self._handle_idle_behaviors()
        
        # 更新动画帧
        if self.current_animation:
            # 检查是否需要切换到下一帧
            elapsed = current_time - self.animation_start_time
            target_frame = int(elapsed / self.frame_duration)
            
            if target_frame >= len(self.current_animation):
                # 动画播放完毕
                if self.current_state == EyeState.IDLE:
                    # IDLE状态循环播放
                    self.animation_frame_index = 0
                    self.animation_start_time = current_time
                else:
                    # 非IDLE状态，返回IDLE
                    self.change_state(EyeState.IDLE)
            else:
                self.animation_frame_index = min(target_frame, len(self.current_animation) - 1)
    
    def get_current_frame(self):
        """获取当前应该显示的帧"""
        if self.current_animation and 0 <= self.animation_frame_index < len(self.current_animation):
            return self.current_animation[self.animation_frame_index]
        else:
            # 如果没有有效帧，返回基础空闲帧
            idle_frames = self.animation_manager.get_animation('idle')
            return idle_frames[0] if idle_frames else None
    
    def get_current_state(self):
        """获取当前状态"""
        return self.current_state
    
    def get_state_info(self):
        """获取状态信息（用于调试）"""
        elapsed = time.time() - self.state_start_time
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value,
            'elapsed_time': elapsed,
            'animation_frame': f"{self.animation_frame_index + 1}/{len(self.current_animation)}",
            'next_auto_blink': max(0, self.auto_blink_interval - (time.time() - self.last_auto_blink))
        }