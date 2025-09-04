#!/usr/bin/env python3
"""
Robot Eye Animations Module
负责生成各种眼睛动画的帧序列，包括基本形状绘制和复杂动画效果
"""
import pygame
import math
import random

def ease_in(t, start, end):
    """缓入函数 - 慢开始"""
    t = max(0, min(1, t))
    return start + (end - start) * t * t

def ease_out(t, start, end):
    """缓出函数 - 慢结束"""
    t = max(0, min(1, t))
    return start + (end - start) * (1 - (1 - t) * (1 - t))

def ease_in_out(t, start, end):
    """缓入缓出函数 - 慢开始慢结束"""
    t = max(0, min(1, t))
    if t < 0.5:
        return start + (end - start) * 2 * t * t
    else:
        return start + (end - start) * (1 - 2 * (1 - t) * (1 - t))

def linear(t, start, end):
    """线性插值函数"""
    t = max(0, min(1, t))
    return start + (end - start) * t

class AnimationManager:
    def __init__(self, screen_width, screen_height):
        """初始化动画管理器"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 颜色定义
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        
        # 眼睛基础参数
        self.eye_width = 80
        self.eye_height = 80
        self.eye_spacing = 160  # 两眼间距
        
        # 眼睛位置（屏幕中心偏上）
        eye_y = screen_height // 2 - 40  # 将眼睛位置上移为嘴巴留出空间
        self.left_eye_center = (screen_width // 2 - self.eye_spacing // 2, eye_y)
        self.right_eye_center = (screen_width // 2 + self.eye_spacing // 2, eye_y)
        
        # 嘴巴基础参数
        self.mouth_width = 120
        self.mouth_height = 40
        mouth_y = screen_height // 2 + 60  # 嘴巴位置在眼睛下方
        self.mouth_center = (screen_width // 2, mouth_y)
        
        # 预生成所有动画帧
        self.animations = {}
        self._generate_all_animations()
    
    def _create_surface(self):
        """创建新的透明Surface"""
        surface = pygame.Surface((self.screen_width, self.screen_height))
        surface.fill(self.BLACK)
        return surface
    
    def _draw_eye(self, surface, center, width, height, offset=(0, 0), scale=1.0):
        """绘制单个眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        adjusted_width = int(width * scale)
        adjusted_height = int(height * scale)
        
        pygame.draw.ellipse(surface, self.WHITE, 
                          (adjusted_center[0] - adjusted_width//2,
                           adjusted_center[1] - adjusted_height//2,
                           adjusted_width, adjusted_height))
    
    def _draw_eyes_as_arcs(self, surface, y_offset=0, arc_height=30):
        """绘制弧形眼睛（开心状态）"""
        left_center = (self.left_eye_center[0], self.left_eye_center[1] + y_offset)
        right_center = (self.right_eye_center[0], self.right_eye_center[1] + y_offset)
        
        # 绘制弯月形状
        pygame.draw.arc(surface, self.WHITE,
                       (left_center[0] - self.eye_width//2,
                        left_center[1] - arc_height//2,
                        self.eye_width, arc_height),
                       0, math.pi, 3)
        pygame.draw.arc(surface, self.WHITE,
                       (right_center[0] - self.eye_width//2,
                        right_center[1] - arc_height//2,
                        self.eye_width, arc_height),
                       0, math.pi, 3)
    
    def _draw_sparkles_at_eye_corners(self, surface):
        """在眼角绘制闪烁效果"""
        # 左眼外侧闪烁
        left_sparkle = (self.left_eye_center[0] - 50, self.left_eye_center[1] - 15)
        pygame.draw.line(surface, self.WHITE, 
                        (left_sparkle[0] - 8, left_sparkle[1]), 
                        (left_sparkle[0] + 8, left_sparkle[1]), 2)
        pygame.draw.line(surface, self.WHITE,
                        (left_sparkle[0], left_sparkle[1] - 8),
                        (left_sparkle[0], left_sparkle[1] + 8), 2)
        
        # 右眼外侧闪烁
        right_sparkle = (self.right_eye_center[0] + 50, self.right_eye_center[1] - 20)
        pygame.draw.line(surface, self.WHITE,
                        (right_sparkle[0] - 6, right_sparkle[1]),
                        (right_sparkle[0] + 6, right_sparkle[1]), 2)
        pygame.draw.line(surface, self.WHITE,
                        (right_sparkle[0], right_sparkle[1] - 6),
                        (right_sparkle[0], right_sparkle[1] + 6), 2)
    
    def _draw_radial_lines_around_eyes(self, surface):
        """在眼睛周围绘制放射线（惊讶效果）"""
        for eye_center in [self.left_eye_center, self.right_eye_center]:
            for i in range(8):  # 8条放射线
                angle = i * math.pi / 4
                start_radius = 60
                end_radius = 80
                start_x = eye_center[0] + math.cos(angle) * start_radius
                start_y = eye_center[1] + math.sin(angle) * start_radius
                end_x = eye_center[0] + math.cos(angle) * end_radius
                end_y = eye_center[1] + math.sin(angle) * end_radius
                pygame.draw.line(surface, self.WHITE, (start_x, start_y), (end_x, end_y), 2)
    
    def _draw_lightning_bolts(self, surface):
        """绘制闪电符号（愤怒效果）"""
        # 左侧闪电
        left_bolt_x = self.left_eye_center[0] - 20
        left_bolt_y = self.left_eye_center[1] - 60
        lightning_points = [
            (left_bolt_x, left_bolt_y),
            (left_bolt_x + 8, left_bolt_y + 12),
            (left_bolt_x + 3, left_bolt_y + 12),
            (left_bolt_x + 10, left_bolt_y + 25)
        ]
        pygame.draw.lines(surface, self.WHITE, False, lightning_points, 3)
        
        # 右侧闪电
        right_bolt_x = self.right_eye_center[0] + 20
        right_bolt_y = self.right_eye_center[1] - 55
        lightning_points = [
            (right_bolt_x, right_bolt_y),
            (right_bolt_x - 8, right_bolt_y + 15),
            (right_bolt_x - 3, right_bolt_y + 15),
            (right_bolt_x - 10, right_bolt_y + 28)
        ]
        pygame.draw.lines(surface, self.WHITE, False, lightning_points, 3)
    
    def _draw_teardrop(self, surface, position, size=8):
        """绘制泪滴（悲伤效果）"""
        x, y = position
        # 绘制泪滴形状：圆形+三角形
        pygame.draw.circle(surface, self.WHITE, (x, y + size//2), size//2)
        # 小三角形顶部
        points = [(x, y), (x - size//3, y + size//2), (x + size//3, y + size//2)]
        pygame.draw.polygon(surface, self.WHITE, points)
    
    def _draw_heart(self, surface, position, size=16):
        """绘制心形图标（兴奋效果）"""
        x, y = position
        # 简化的心形：两个圆+三角形
        radius = size // 4
        pygame.draw.circle(surface, self.WHITE, (x - radius//2, y), radius)
        pygame.draw.circle(surface, self.WHITE, (x + radius//2, y), radius)
        # 下方三角形
        points = [(x - radius, y + radius//2), (x + radius, y + radius//2), (x, y + size)]
        pygame.draw.polygon(surface, self.WHITE, points)
    
    def _draw_crown(self, surface, position, size=20):
        """绘制皇冠图标（胜利效果）"""
        x, y = position
        # 皇冠底座
        base_width = size
        base_height = size // 4
        pygame.draw.rect(surface, self.WHITE, (x - base_width//2, y + size//2, base_width, base_height))
        
        # 皇冠尖角
        points = [
            (x - base_width//2, y + size//2),
            (x - base_width//4, y),
            (x, y + size//4),
            (x + base_width//4, y),
            (x + base_width//2, y + size//2)
        ]
        pygame.draw.polygon(surface, self.WHITE, points)
    
    def _draw_trophy(self, surface, position, size=18):
        """绘制奖杯图标（胜利效果）"""
        x, y = position
        # 奖杯杯身
        cup_width = size // 2
        cup_height = size // 2
        pygame.draw.ellipse(surface, self.WHITE, (x - cup_width//2, y, cup_width, cup_height))
        
        # 奖杯把手
        pygame.draw.arc(surface, self.WHITE, (x - size//2, y + size//4, size//3, size//3), 
                       math.pi/2, 3*math.pi/2, 2)
        pygame.draw.arc(surface, self.WHITE, (x + size//6, y + size//4, size//3, size//3), 
                       -math.pi/2, math.pi/2, 2)
        
        # 奖杯底座
        pygame.draw.rect(surface, self.WHITE, (x - size//3, y + cup_height, size*2//3, size//4))
    
    def _draw_hand_cover(self, surface, position, size=40, openness=0.0):
        """绘制遮挡的手掌（害羞效果）"""
        x, y = position
        # 手掌基本形状：椭圆形
        hand_width = int(size * (1 - openness * 0.3))
        hand_height = int(size * 1.2)
        pygame.draw.ellipse(surface, self.WHITE, 
                          (x - hand_width//2, y - hand_height//2, hand_width, hand_height))
        
        # 如果有开口，在中间画个小缝隙
        if openness > 0.3:
            gap_width = int(size * openness * 0.4)
            gap_height = int(size * 0.8)
            pygame.draw.ellipse(surface, self.BLACK,
                              (x - gap_width//2, y - gap_height//2, gap_width, gap_height))
    
    def _draw_star_sparkle(self, surface, position, size=8):
        """绘制星星闪烁效果（恶作剧效果）"""
        x, y = position
        # 绘制四角星星
        half_size = size // 2
        pygame.draw.line(surface, self.WHITE, (x, y - half_size), (x, y + half_size), 2)
        pygame.draw.line(surface, self.WHITE, (x - half_size, y), (x + half_size, y), 2)
        pygame.draw.line(surface, self.WHITE, (x - half_size//2, y - half_size//2), 
                        (x + half_size//2, y + half_size//2), 1)
        pygame.draw.line(surface, self.WHITE, (x - half_size//2, y + half_size//2), 
                        (x + half_size//2, y - half_size//2), 1)
    
    def _draw_raised_eyebrow(self, surface, center, width):
        """绘制上挑的眉毛（恶作剧效果）"""
        eyebrow_y = center[1] - width//2 - 20
        
        # 上挑的眉毛
        start_x = center[0] - width//2 - 5
        end_x = center[0] + width//2 + 5
        start_y = eyebrow_y + 8
        end_y = eyebrow_y - 5
        
        pygame.draw.line(surface, self.WHITE, (start_x, start_y), (end_x, end_y), 4)
    
    def _draw_converging_eyebrows(self, surface):
        """绘制向中心聚拢的八字眉（专注效果）"""
        # 左眉毛 - 向内倾斜
        left_start = (self.left_eye_center[0] - 25, self.left_eye_center[1] - 45)
        left_end = (self.left_eye_center[0] + 15, self.left_eye_center[1] - 35)
        pygame.draw.line(surface, self.WHITE, left_start, left_end, 4)
        
        # 右眉毛 - 向内倾斜
        right_start = (self.right_eye_center[0] + 25, self.right_eye_center[1] - 45)
        right_end = (self.right_eye_center[0] - 15, self.right_eye_center[1] - 35)
        pygame.draw.line(surface, self.WHITE, right_start, right_end, 4)
    
    def _draw_spotlight_effect(self, surface):
        """绘制聚光灯效果（专注状态）- 简化版本"""
        # 在眼部周围绘制暗化效果
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(80)  # 半透明黑色
        overlay.fill((0, 0, 0))
        
        # 在眼部区域留白（不绘制暗化）
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2 - 20
        
        # 绘制围绕眼部的聚焦框
        focus_width = 200
        focus_height = 100
        focus_rect = (center_x - focus_width//2, center_y - focus_height//2, focus_width, focus_height)
        
        # 绘制聚焦区域的边框
        pygame.draw.rect(surface, self.WHITE, focus_rect, 2)
        
        # 可选：添加角落装饰
        corner_size = 15
        corners = [
            (center_x - focus_width//2, center_y - focus_height//2),  # 左上
            (center_x + focus_width//2, center_y - focus_height//2),  # 右上
            (center_x - focus_width//2, center_y + focus_height//2),  # 左下
            (center_x + focus_width//2, center_y + focus_height//2)   # 右下
        ]
        
        for corner in corners:
            pygame.draw.lines(surface, self.WHITE, False, [
                (corner[0] - corner_size, corner[1]),
                corner,
                (corner[0], corner[1] - corner_size)
            ], 3)
    
    def _draw_happy_eye(self, surface, center, width, height, offset=(0, 0), intensity=1.0):
        """绘制开心的弯月眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制弯月形状（使用两个圆形来创造弯月效果）
        arc_height = int(height * intensity * 0.3)
        
        # 上弧
        pygame.draw.arc(surface, self.WHITE,
                       (adjusted_center[0] - width//2,
                        adjusted_center[1] - arc_height//2,
                        width, arc_height),
                       0, math.pi, 3)
    
    def _draw_surprised_eye(self, surface, center, width, height, offset=(0, 0), scale=1.5):
        """绘制惊讶的大眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        adjusted_width = int(width * scale)
        adjusted_height = int(height * scale)
        
        # 外圈
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - adjusted_width//2,
                           adjusted_center[1] - adjusted_height//2,
                           adjusted_width, adjusted_height), 2)
        
        # 内圈（瞳孔）
        pupil_size = int(min(adjusted_width, adjusted_height) * 0.3)
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - pupil_size//2,
                           adjusted_center[1] - pupil_size//2,
                           pupil_size, pupil_size))
    
    def _draw_angry_eye(self, surface, center, width, height, offset=(0, 0)):
        """绘制生气的眼睛（带眉毛）"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制普通眼睛
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - width//2,
                           adjusted_center[1] - height//2,
                           width, height))
        
        # 绘制倾斜的眉毛（直线版本）
        eyebrow_y = adjusted_center[1] - height//2 - 15
        eyebrow_width = width + 10
        
        # 左眼眉（向左下倾斜）
        if center[0] < self.screen_width // 2:  # 左眼
            pygame.draw.line(surface, self.WHITE,
                           (adjusted_center[0] - eyebrow_width//2, eyebrow_y - 5),
                           (adjusted_center[0] + eyebrow_width//2, eyebrow_y + 5), 4)
        else:  # 右眼
            pygame.draw.line(surface, self.WHITE,
                           (adjusted_center[0] - eyebrow_width//2, eyebrow_y + 5),
                           (adjusted_center[0] + eyebrow_width//2, eyebrow_y - 5), 4)
    
    def _draw_sleepy_eye(self, surface, center, width, height, offset=(0, 0), openness=0.3):
        """绘制睡意的半闭眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制半闭的眼睛
        sleepy_height = int(height * openness)
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - width//2,
                           adjusted_center[1] - sleepy_height//2,
                           width, sleepy_height))
    
    def _draw_sad_eye(self, surface, center, width, height, offset=(0, 0)):
        """绘制悲伤的下垂眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制下垂的弧形眼睛
        arc_height = height // 2
        pygame.draw.arc(surface, self.WHITE,
                       (adjusted_center[0] - width//2,
                        adjusted_center[1] + height//4,  # 向下偏移
                        width, arc_height),
                       0, math.pi, 3)
    
    def _draw_furious_eye(self, surface, center, width, height, offset=(0, 0)):
        """绘制狂怒的倒三角眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制倒三角形
        triangle_points = [
            (adjusted_center[0], adjusted_center[1] + height//2),     # 下方顶点
            (adjusted_center[0] - width//2, adjusted_center[1] - height//2),  # 左上角
            (adjusted_center[0] + width//2, adjusted_center[1] - height//2)   # 右上角
        ]
        pygame.draw.polygon(surface, self.WHITE, triangle_points)
    
    def _draw_fear_eye(self, surface, center, width, height, offset=(0, 0)):
        """绘制恐惧的大椭圆眼睛"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制拉长的椭圆形眼睛
        fear_width = int(width * 1.3)
        fear_height = int(height * 0.8)
        
        # 外圈
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - fear_width//2,
                           adjusted_center[1] - fear_height//2,
                           fear_width, fear_height), 2)
        
        # 小瞳孔（向内聚拢）
        pupil_size = max(8, int(min(fear_width, fear_height) * 0.2))
        pupil_offset_x = 8 if center[0] < self.screen_width // 2 else -8  # 向内聚拢
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - pupil_size//2 + pupil_offset_x,
                           adjusted_center[1] - pupil_size//2,
                           pupil_size, pupil_size))
    
    def _draw_bored_eye(self, surface, center, width, height, openness=0.3, offset=(0, 0)):
        """绘制无聊的半闭眼睛（类似瞌睡但更平）"""
        adjusted_center = (center[0] + offset[0], center[1] + offset[1])
        
        # 绘制扁平的眼睛
        bored_height = int(height * openness)
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - width//2,
                           adjusted_center[1] - bored_height//2,
                           width, bored_height))
    
    def _draw_excited_eye(self, surface, center, width, height, bounce_offset=(0, 0)):
        """绘制兴奋的跳动眼睛"""
        adjusted_center = (center[0] + bounce_offset[0], center[1] + bounce_offset[1])
        
        # 绘制稍微放大的圆形眼睛
        excited_width = int(width * 1.1)
        excited_height = int(height * 1.1)
        pygame.draw.ellipse(surface, self.WHITE,
                          (adjusted_center[0] - excited_width//2,
                           adjusted_center[1] - excited_height//2,
                           excited_width, excited_height))
    
    def _draw_mouth(self, surface, mouth_type="neutral", intensity=1.0):
        """绘制嘴巴"""
        center = self.mouth_center
        width = self.mouth_width
        height = self.mouth_height
        
        if mouth_type == "smile":
            # 微笑弧度
            arc_height = int(height * intensity * 0.8)
            pygame.draw.arc(surface, self.WHITE,
                          (center[0] - width//2, center[1] - arc_height//2,
                           width, arc_height),
                          0, math.pi, 3)
        
        elif mouth_type == "big_smile":
            # 大笑（更大的弧度）
            arc_height = int(height * intensity)
            pygame.draw.arc(surface, self.WHITE,
                          (center[0] - width//2, center[1] - arc_height//2,
                           width, arc_height),
                          0, math.pi, 5)
        
        elif mouth_type == "frown":
            # 不高兴（向下的弧度）
            arc_height = int(height * intensity * 0.6)
            pygame.draw.arc(surface, self.WHITE,
                          (center[0] - width//2, center[1] + arc_height//2,
                           width, arc_height),
                          math.pi, 2 * math.pi, 3)
        
        elif mouth_type == "surprised":
            # 惊讶（小圆形）
            mouth_radius = int(width * 0.15 * intensity)
            pygame.draw.ellipse(surface, self.WHITE,
                              (center[0] - mouth_radius, center[1] - mouth_radius,
                               mouth_radius * 2, mouth_radius * 2), 2)
        
        elif mouth_type == "wavy":
            # 波浪形（困惑）
            points = []
            wave_count = 3
            for i in range(wave_count * 8):
                x = center[0] - width//2 + (i * width) // (wave_count * 8)
                y = center[1] + math.sin(i * math.pi / 4) * 8 * intensity
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.WHITE, False, points, 2)
        
        elif mouth_type == "straight":
            # 直线（中性或生气）
            line_width = int(width * 0.6)
            pygame.draw.line(surface, self.WHITE,
                           (center[0] - line_width//2, center[1]),
                           (center[0] + line_width//2, center[1]), 3)
        
        elif mouth_type == "roar":
            # 咆哮的锯齿状嘴巴
            roar_width = int(width * 0.8)
            roar_height = int(height * intensity * 0.6)
            
            # 绘制锯齿状的张开嘴巴
            teeth_count = 8
            tooth_width = roar_width // teeth_count
            
            points = []
            for i in range(teeth_count + 1):
                x = center[0] - roar_width//2 + i * tooth_width
                if i % 2 == 0:
                    y = center[1] - roar_height//2  # 齿尖向上
                else:
                    y = center[1] + roar_height//2  # 齿尖向下
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.WHITE, False, points, 4)
                
            # 在嘴巴内部绘制震动线条（声音效果）
            if intensity > 0.8:
                for i in range(3):
                    line_x = center[0] - 20 + i * 20
                    pygame.draw.line(surface, self.WHITE,
                                   (line_x, center[1] - roar_height//4),
                                   (line_x, center[1] + roar_height//4), 2)
    
    def _draw_symbol(self, surface, symbol_type, position, size=20):
        """绘制特殊符号（问号、Z等）"""
        pygame.font.init()  # 确保字体已初始化
        font = pygame.font.Font(None, size)
        
        if symbol_type == "question":
            text = font.render("?", True, self.WHITE)
            text_rect = text.get_rect(center=position)
            surface.blit(text, text_rect)
        
        elif symbol_type == "ellipsis":
            text = font.render("...", True, self.WHITE)
            text_rect = text.get_rect(center=position)
            surface.blit(text, text_rect)
        
        elif symbol_type == "z":
            text = font.render("Z", True, self.WHITE)
            text_rect = text.get_rect(center=position)
            surface.blit(text, text_rect)
        
        elif symbol_type == "zz":
            text = font.render("ZZ", True, self.WHITE)
            text_rect = text.get_rect(center=position)
            surface.blit(text, text_rect)
    
    def _generate_blink_animation(self):
        """生成眨眼动画序列"""
        frames = []
        frame_count = 12
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 计算眨眼进度（0到1再到0）
            if i <= frame_count // 2:
                progress = i / (frame_count // 2)
            else:
                progress = (frame_count - i) / (frame_count // 2)
            
            # 根据进度调整眼睛高度
            eye_height = self.eye_height * (1 - progress)
            
            if eye_height > 2:  # 避免完全消失
                self._draw_eye(surface, self.left_eye_center, self.eye_width, eye_height)
                self._draw_eye(surface, self.right_eye_center, self.eye_width, eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_happy_animation(self):
        """生成开心动画序列"""
        frames = []
        frame_count = 20
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 渐变到开心状态
            progress = min(1.0, i / 10.0)
            
            if progress < 1.0:
                # 过渡帧：从正常眼睛到开心眼睛
                normal_alpha = 1.0 - progress
                happy_alpha = progress
                
                if normal_alpha > 0:
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                                 int(self.eye_height * normal_alpha))
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                                 int(self.eye_height * normal_alpha))
                
                if happy_alpha > 0:
                    self._draw_happy_eye(surface, self.left_eye_center, self.eye_width, 
                                       self.eye_height, intensity=happy_alpha)
                    self._draw_happy_eye(surface, self.right_eye_center, self.eye_width, 
                                       self.eye_height, intensity=happy_alpha)
            else:
                # 完全开心状态
                self._draw_happy_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                self._draw_happy_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_surprised_animation(self):
        """生成惊讶/震惊表情动画 - 按照详细规范实现"""
        frames = []
        frame_count = 11  # 0-10帧总共11帧
        
        # 动画参数
        eye_radius_max = 1.5  # 最大放大倍数
        mouth_radius = 20
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            if i == 0:
                # 帧0: 瞬间爆发 - 眼睛瞬间放大，嘴巴变O形，绘制放射线
                self._draw_surprised_eye(surface, self.left_eye_center, self.eye_width,
                                       self.eye_height, scale=eye_radius_max)
                self._draw_surprised_eye(surface, self.right_eye_center, self.eye_width,
                                       self.eye_height, scale=eye_radius_max)
                
                # 绘制O形嘴巴
                self._draw_mouth(surface, "surprised", intensity=1.0)
                
                # 绘制放射线效果
                self._draw_radial_lines_around_eyes(surface)
                
            elif 1 <= i <= 5:
                # 帧1-5: 维持震惊状态
                self._draw_surprised_eye(surface, self.left_eye_center, self.eye_width,
                                       self.eye_height, scale=eye_radius_max)
                self._draw_surprised_eye(surface, self.right_eye_center, self.eye_width,
                                       self.eye_height, scale=eye_radius_max)
                
                # 维持O形嘴巴
                self._draw_mouth(surface, "surprised", intensity=1.0)
                
            elif 6 <= i <= 10:
                # 帧6-10: 快速恢复到默认状态
                t = (i - 6) / 4.0  # 0.0 到 1.0
                current_scale = linear(t, eye_radius_max, 1.0)
                
                if t < 1.0:
                    # 眼睛快速收缩
                    self._draw_surprised_eye(surface, self.left_eye_center, self.eye_width,
                                           self.eye_height, scale=current_scale)
                    self._draw_surprised_eye(surface, self.right_eye_center, self.eye_width,
                                           self.eye_height, scale=current_scale)
                    # 嘴巴恢复
                    self._draw_mouth(surface, "surprised", intensity=1.0 - t)
                else:
                    # 完全恢复正常
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_look_animation(self, direction):
        """生成看向特定方向的动画"""
        frames = []
        frame_count = 30
        
        # 方向偏移量
        direction_offsets = {
            'left': (-30, 0),
            'right': (30, 0),
            'up': (0, -20),
            'down': (0, 20)
        }
        
        target_offset = direction_offsets.get(direction, (0, 0))
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 平滑移动到目标位置并返回
            if i < frame_count // 2:
                progress = i / (frame_count // 2)
                current_offset = (target_offset[0] * progress, target_offset[1] * progress)
            else:
                progress = (frame_count - i) / (frame_count // 2)
                current_offset = (target_offset[0] * progress, target_offset[1] * progress)
            
            self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                          self.eye_height, offset=current_offset)
            self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                          self.eye_height, offset=current_offset)
            
            frames.append(surface)
        
        return frames
    
    def _generate_wink_animation(self):
        """生成眨眼动画（只眨一只眼）"""
        frames = []
        frame_count = 15
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 右眼保持正常
            self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            # 左眼眨眼
            if i <= frame_count // 2:
                progress = i / (frame_count // 2)
            else:
                progress = (frame_count - i) / (frame_count // 2)
            
            left_eye_height = self.eye_height * (1 - progress)
            if left_eye_height > 2:
                self._draw_eye(surface, self.left_eye_center, self.eye_width, left_eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_confused_animation(self):
        """生成困惑动画（缓慢左右扫视）"""
        frames = []
        frame_count = 40
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 左右扫视运动
            angle = (i / frame_count) * 4 * math.pi  # 两个完整周期
            offset_x = math.sin(angle) * 15
            
            self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                          self.eye_height, offset=(offset_x, 0))
            self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                          self.eye_height, offset=(offset_x, 0))
            
            frames.append(surface)
        
        return frames
    
    def _generate_idle_frame(self, micro_offset=(0, 0)):
        """生成空闲状态的单帧（带微小偏移）"""
        surface = self._create_surface()
        self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                      self.eye_height, offset=micro_offset)
        self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                      self.eye_height, offset=micro_offset)
        return surface
    
    def _generate_joy_animation(self):
        """生成开心/大笑表情动画 - 按照详细规范实现"""
        frames = []
        frame_count = 21  # 0-20帧总共21帧
        
        # 动画参数
        eye_y_offset_max = 20
        arc_height_max = 50
        mouth_height_max = 50
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            if i <= 5:
                # 帧0-5: 从正常状态过渡到开心状态
                t = i / 5.0
                current_eye_y_offset = ease_out(t, 0, eye_y_offset_max)
                current_arc_height = ease_out(t, self.eye_height, arc_height_max)
                current_mouth_height = ease_out(t, 0, mouth_height_max)
                
                # 混合绘制正常眼睛和弧形眼睛
                if t < 1.0:
                    # 绘制正在变形的眼睛
                    eye_height = ease_out(t, self.eye_height, current_arc_height)
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                                 eye_height, offset=(0, current_eye_y_offset))
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                                 eye_height, offset=(0, current_eye_y_offset))
                else:
                    # 完全变成弧形
                    self._draw_eyes_as_arcs(surface, current_eye_y_offset, current_arc_height)
                
                # 绘制渐变的嘴巴
                self._draw_mouth(surface, "big_smile", intensity=t)
                
            elif 6 <= i <= 15:
                # 帧6-15: 保持开心状态，第10帧显示闪烁
                self._draw_eyes_as_arcs(surface, eye_y_offset_max, arc_height_max)
                self._draw_mouth(surface, "big_smile", intensity=1.0)
                
                # 第10帧显示闪烁效果
                if i == 10:
                    self._draw_sparkles_at_eye_corners(surface)
                    
            elif 16 <= i <= 20:
                # 帧16-20: 恢复到默认状态
                t = (i - 16) / 4.0  # 0.0到1.0的过程
                current_eye_y_offset = ease_in(t, eye_y_offset_max, 0)
                current_arc_height = ease_in(t, arc_height_max, self.eye_height)
                current_mouth_height = ease_in(t, mouth_height_max, 0)
                
                # 从弧形恢复到正常眼睛
                if t < 1.0:
                    # 还在变形过程中
                    eye_height = ease_in(t, arc_height_max, self.eye_height)
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, 
                                 eye_height, offset=(0, current_eye_y_offset))
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, 
                                 eye_height, offset=(0, current_eye_y_offset))
                else:
                    # 完全恢复正常
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                
                # 嘴巴恢复（可选择不绘制或绘制平线）
                if t < 1.0:
                    self._draw_mouth(surface, "big_smile", intensity=1.0-t)
            
            frames.append(surface)
        
        return frames
    
    def _generate_thinking_animation(self):
        """生成困惑/思考表情动画 - 按照详细规范实现"""
        frames = []
        frame_count = 21  # 0-20帧总共21帧
        
        # 动画参数
        eye_x_offset_max = 30
        scan_speed = 0.5
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            if i <= 3:
                # 帧0-3: 进入困惑状态
                t = i / 3.0
                current_eye_x_offset = ease_in(t, 0, eye_x_offset_max)
                
                # 绘制偏移的眼睛
                self._draw_eye(surface, self.left_eye_center, self.eye_width,
                              self.eye_height, offset=(current_eye_x_offset + 3, 0))
                self._draw_eye(surface, self.right_eye_center, self.eye_width,
                              self.eye_height, offset=(current_eye_x_offset - 3, 0))
                
                # 绘制波浪嘴巴
                self._draw_mouth(surface, "wavy", intensity=t * 0.8)
                
            elif 4 <= i <= 15:
                # 帧4-15: 维持困惑并进行扫视
                # 缓慢的扫视运动
                scan_progress = (i - 4) / 11.0  # 0.0 到 1.0
                current_eye_scan_x = math.sin(scan_progress * scan_speed * 2 * math.pi) * (eye_x_offset_max / 2)
                
                # 绘制扫视的眼睛
                self._draw_eye(surface, self.left_eye_center, self.eye_width,
                              self.eye_height, offset=(current_eye_scan_x + 3, 0))
                self._draw_eye(surface, self.right_eye_center, self.eye_width,
                              self.eye_height, offset=(current_eye_scan_x - 3, 0))
                
                # 绘制波浪嘴巴
                self._draw_mouth(surface, "wavy", intensity=0.8)
                
                # 随机出现问号（10%概率每帧）
                if random.random() < 0.1:
                    question_pos = (self.screen_width // 2 + 80, self.left_eye_center[1] - 50)
                    self._draw_symbol(surface, "question", question_pos, 25)
                    
            elif 16 <= i <= 20:
                # 帧16-20: 恢复默认状态
                t = (i - 16) / 4.0
                current_eye_x_offset = ease_in(t, eye_x_offset_max / 2, 0)
                
                # 恢复正常眼睛位置
                if t < 1.0:
                    self._draw_eye(surface, self.left_eye_center, self.eye_width,
                                  self.eye_height, offset=(current_eye_x_offset, 0))
                    self._draw_eye(surface, self.right_eye_center, self.eye_width,
                                  self.eye_height, offset=(current_eye_x_offset, 0))
                    # 嘴巴恢复
                    self._draw_mouth(surface, "wavy", intensity=(1.0 - t) * 0.8)
                else:
                    # 完全恢复默认
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_angry_animation(self):
        """生成生气/愤怒表情动画 - 按照详细规范实现"""
        frames = []
        frame_count = 21  # 0-20帧总共21帧
        
        # 动画参数
        eyebrow_angle_max = 15  # 眉毛最大角度
        shake_magnitude = 5     # 抖动幅度
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            if i <= 3:
                # 帧0-3: 过渡到愤怒状态
                t = i / 3.0
                
                # 绘制愤怒眼睛（带逐渐倾斜的眉毛）
                self._draw_angry_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                self._draw_angry_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                
                # 绘制向下弯曲的嘴巴
                self._draw_mouth(surface, "frown", intensity=ease_in(t, 0, 1.0))
                
            elif 4 <= i <= 15:
                # 帧4-15: 保持愤怒表情并添加抖动效果
                current_x_offset = 0
                current_y_offset = 0
                
                # 20%概率产生抖动
                if random.random() < 0.2:
                    current_x_offset = random.randint(-shake_magnitude, shake_magnitude)
                    current_y_offset = random.randint(-shake_magnitude, shake_magnitude)
                    
                    # 在抖动时绘制闪电效果
                    self._draw_lightning_bolts(surface)
                
                # 绘制带抖动的愤怒眼睛和眉毛
                self._draw_angry_eye(surface, self.left_eye_center, self.eye_width, 
                                   self.eye_height, offset=(current_x_offset, current_y_offset))
                self._draw_angry_eye(surface, self.right_eye_center, self.eye_width, 
                                   self.eye_height, offset=(current_x_offset, current_y_offset))
                
                # 维持向下的嘴巴
                self._draw_mouth(surface, "frown", intensity=1.0)
                
            elif 16 <= i <= 20:
                # 帧16-20: 恢复到默认状态
                t = (i - 16) / 4.0
                
                if t < 1.0:
                    # 还在恢复过程中，绘制逐渐变正常的眼睛
                    # 这里可以混合绘制愤怒眼睛和正常眼睛
                    if t < 0.5:
                        self._draw_angry_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                        self._draw_angry_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                    else:
                        self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                        self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                    
                    # 嘴巴恢复
                    self._draw_mouth(surface, "frown", intensity=1.0 - t)
                else:
                    # 完全恢复正常
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                    self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            frames.append(surface)
        
        return frames
    
    def _generate_sleepy_animation(self):
        """生成睡意表情动画（半闭眼睛 + Z符号）"""
        frames = []
        frame_count = 40
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 眼睛缓慢闭合和睁开的循环
            sleep_cycle = (i % 20) / 20.0
            if sleep_cycle < 0.7:
                eye_openness = 0.3 + (1.0 - sleep_cycle) * 0.1  # 缓慢闭合
            else:
                eye_openness = 0.2 + (sleep_cycle - 0.7) * 0.4  # 突然睁开一点
            
            # 绘制睡意眼睛
            self._draw_sleepy_eye(surface, self.left_eye_center, self.eye_width, 
                                self.eye_height, openness=eye_openness)
            self._draw_sleepy_eye(surface, self.right_eye_center, self.eye_width, 
                                self.eye_height, openness=eye_openness)
            
            # 绘制平直嘴巴
            self._draw_mouth(surface, "straight", intensity=0.6)
            
            # Z符号飘动效果
            if i % 16 < 8:  # 单个Z
                z_pos = (self.screen_width // 2 + 80, self.left_eye_center[1] - 60 + (i % 8) * 3)
                self._draw_symbol(surface, "z", z_pos, 20)
            else:  # 双Z
                zz_pos = (self.screen_width // 2 + 90, self.left_eye_center[1] - 50 + ((i - 8) % 8) * 2)
                self._draw_symbol(surface, "zz", zz_pos, 18)
            
            frames.append(surface)
        
        return frames
    
    def _generate_surprised_with_mouth_animation(self):
        """生成惊讶表情动画（大眼睛 + O形嘴巴）"""
        frames = []
        frame_count = 20
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 快速放大效果
            if i < 6:
                scale = 1.0 + (i / 5.0) * 0.8  # 快速放大
            else:
                scale = 1.8 - ((i - 6) / 14.0) * 0.3  # 缓慢回缩到较大状态
            
            mouth_scale = min(1.0, i / 8.0)  # 嘴巴跟随放大
            
            # 绘制惊讶眼睛
            self._draw_surprised_eye(surface, self.left_eye_center, self.eye_width, 
                                   self.eye_height, scale=scale)
            self._draw_surprised_eye(surface, self.right_eye_center, self.eye_width, 
                                   self.eye_height, scale=scale)
            
            # 绘制惊讶嘴巴
            self._draw_mouth(surface, "surprised", intensity=mouth_scale)
            
            frames.append(surface)
        
        return frames
    
    def _generate_sadness_animation(self):
        """生成悲伤表情动画（下垂眼睛 + 掉落泪珠）"""
        frames = []
        frame_count = 45  # 较长的动画以展示泪珠下落
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 绘制悲伤的下垂眼睛
            self._draw_sad_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
            self._draw_sad_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            # 绘制向下弯曲的悲伤嘴巴
            self._draw_mouth(surface, "frown", intensity=0.8)
            
            # 泪珠效果：从第10帧开始出现泪珠
            if i >= 10:
                # 左眼泪珠
                tear_progress = (i - 10) / 35.0  # 泪珠下落进度
                left_tear_y = self.left_eye_center[1] + 25 + tear_progress * 100
                if left_tear_y < self.screen_height:
                    self._draw_teardrop(surface, (self.left_eye_center[0] - 15, left_tear_y), size=6)
                
                # 右眼泪珠（稍微延迟）
                if i >= 15:
                    right_tear_progress = (i - 15) / 30.0
                    right_tear_y = self.right_eye_center[1] + 25 + right_tear_progress * 100
                    if right_tear_y < self.screen_height:
                        self._draw_teardrop(surface, (self.right_eye_center[0] + 15, right_tear_y), size=6)
            
            frames.append(surface)
        
        return frames
    
    def _generate_furious_animation(self):
        """生成狂怒表情动画（倒三角眼睛 + 锯齿嘴巴 + 强烈震动）"""
        frames = []
        frame_count = 35
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 强烈的抖动效果
            shake_intensity = 8 if i > 5 else 0
            shake_x = random.randint(-shake_intensity, shake_intensity)
            shake_y = random.randint(-shake_intensity, shake_intensity)
            
            # 绘制狂怒的倒三角眼睛
            self._draw_furious_eye(surface, self.left_eye_center, self.eye_width, 
                                 self.eye_height, offset=(shake_x, shake_y))
            self._draw_furious_eye(surface, self.right_eye_center, self.eye_width, 
                                 self.eye_height, offset=(shake_x, shake_y))
            
            # 绘制咆哮的锯齿嘴巴
            roar_intensity = min(1.0, (i - 3) / 8.0) if i > 3 else 0
            if roar_intensity > 0:
                self._draw_mouth(surface, "roar", intensity=roar_intensity)
            
            # 频繁显示闪电效果
            if i > 8 and i % 3 == 0:
                self._draw_lightning_bolts(surface)
            
            frames.append(surface)
        
        return frames
    
    def _generate_shy_animation(self):
        """生成害羞表情动画（手遮眼 + 偷看动作）"""
        frames = []
        frame_count = 50
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            if i <= 10:
                # 前10帧：手掌逐渐遮挡左眼
                hand_progress = i / 10.0
                
                # 绘制右眼（正常）
                self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                
                # 绘制左眼
                self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                
                # 绘制逐渐遮挡的手掌
                if hand_progress > 0.3:
                    self._draw_hand_cover(surface, self.left_eye_center, size=45, openness=0)
                
                # 绘制害羞的微笑
                self._draw_mouth(surface, "smile", intensity=0.5)
                
            elif 11 <= i <= 35:
                # 中间阶段：完全遮挡，偷看动作
                peek_cycle = (i - 11) / 8.0
                is_peeking = (int(peek_cycle) % 3 == 1)  # 每3个周期偷看一次
                
                # 绘制右眼
                self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                
                # 根据是否在偷看来决定手掌的开口
                if is_peeking and (i - 11) % 8 < 4:
                    # 偷看：手掌有开口，可以看到左眼
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                    self._draw_hand_cover(surface, self.left_eye_center, size=45, openness=0.6)
                else:
                    # 完全遮挡
                    self._draw_hand_cover(surface, self.left_eye_center, size=45, openness=0)
                
                # 绘制害羞的微笑
                self._draw_mouth(surface, "smile", intensity=0.6)
                
            else:
                # 最后阶段：手掌逐渐移开
                uncover_progress = (i - 35) / 15.0
                
                # 绘制两只眼睛
                self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
                self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
                
                # 手掌逐渐移开
                if uncover_progress < 1.0:
                    openness = min(1.0, uncover_progress * 2)
                    if openness < 0.9:  # 完全移开前都还有手掌
                        hand_x = self.left_eye_center[0] + uncover_progress * 30
                        self._draw_hand_cover(surface, (hand_x, self.left_eye_center[1]), 
                                           size=45, openness=openness)
                
                # 绘制开心的微笑
                smile_intensity = min(1.0, uncover_progress)
                self._draw_mouth(surface, "smile", intensity=smile_intensity)
            
            frames.append(surface)
        
        return frames
    
    def _generate_mischievous_animation(self):
        """生成恶作剧表情动画（眨眼 + 挑眉 + 星星）"""
        frames = []
        frame_count = 30
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 右眼保持正常
            self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            # 右眼上方绘制上挑的眉毛
            self._draw_raised_eyebrow(surface, self.right_eye_center, self.eye_width)
            
            # 左眼眨眼动作（快速眨眼）
            wink_cycle = (i % 12)
            if wink_cycle < 3:
                # 眨眼中
                left_eye_height = self.eye_height * (1 - wink_cycle / 3.0)
                if left_eye_height > 2:
                    self._draw_eye(surface, self.left_eye_center, self.eye_width, left_eye_height)
            else:
                # 正常睁眼
                self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
            
            # 绘制狡猾的微笑
            self._draw_mouth(surface, "smile", intensity=0.7)
            
            # 在眨眼完成时显示星星
            if wink_cycle == 3:
                star_pos = (self.left_eye_center[0] - 30, self.left_eye_center[1] - 30)
                self._draw_star_sparkle(surface, star_pos, size=10)
            
            frames.append(surface)
        
        return frames
    
    def _generate_bored_animation(self):
        """生成无聊表情动画（眼皮下垂 + 打哈欠）"""
        frames = []
        frame_count = 60  # 较长的动画体现无聊感
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 眼皮缓慢下垂和重新睁开的循环
            droop_cycle = (i % 20) / 20.0
            if droop_cycle < 0.8:
                eye_openness = 0.7 - droop_cycle * 0.4  # 逐渐闭合到30%
            else:
                eye_openness = 0.3 + (droop_cycle - 0.8) * 2.0  # 快速睁开
            
            # 绘制无聊的半闭眼睛
            self._draw_bored_eye(surface, self.left_eye_center, self.eye_width, 
                               self.eye_height, openness=eye_openness)
            self._draw_bored_eye(surface, self.right_eye_center, self.eye_width, 
                               self.eye_height, openness=eye_openness)
            
            # 嘴巴左右缓慢移动（打哈欠动作）
            yawn_progress = (i % 30) / 30.0
            mouth_offset_x = math.sin(yawn_progress * math.pi) * 15
            
            # 绘制平直的无聊嘴巴
            mouth_center = (self.mouth_center[0] + mouth_offset_x, self.mouth_center[1])
            original_center = self.mouth_center
            self.mouth_center = mouth_center
            self._draw_mouth(surface, "straight", intensity=0.5)
            self.mouth_center = original_center  # 恢复原始位置
            
            frames.append(surface)
        
        return frames
    
    def _generate_excited_animation(self):
        """生成兴奋表情动画（跳动眼睛 + 心形图标）"""
        frames = []
        frame_count = 40
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 眼睛和嘴巴快速上下跳动
            bounce_frequency = 0.8  # 跳动频率
            bounce_amplitude = 8    # 跳动幅度
            bounce_offset_y = math.sin(i * bounce_frequency) * bounce_amplitude
            
            # 绘制兴奋的跳动眼睛
            self._draw_excited_eye(surface, self.left_eye_center, self.eye_width, 
                                 self.eye_height, bounce_offset=(0, bounce_offset_y))
            self._draw_excited_eye(surface, self.right_eye_center, self.eye_width, 
                                 self.eye_height, bounce_offset=(0, bounce_offset_y))
            
            # 绘制大笑嘴巴（也跳动）
            mouth_center = (self.mouth_center[0], self.mouth_center[1] + bounce_offset_y)
            original_center = self.mouth_center
            self.mouth_center = mouth_center
            self._draw_mouth(surface, "big_smile", intensity=1.0)
            self.mouth_center = original_center
            
            # 随机出现心形图标
            if i % 8 < 3:  # 跳动的心形
                heart_y = self.left_eye_center[1] - 50 + bounce_offset_y
                self._draw_heart(surface, (self.left_eye_center[0] - 60, heart_y), size=16)
                heart_y2 = self.right_eye_center[1] - 45 + bounce_offset_y
                self._draw_heart(surface, (self.right_eye_center[0] + 60, heart_y2), size=12)
            
            frames.append(surface)
        
        return frames
    
    def _generate_fear_animation(self):
        """生成恐惧表情动画（大椭圆眼 + 持续颤抖）"""
        frames = []
        frame_count = 45
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 持续的快速抖动
            tremor_intensity = 6
            tremor_x = random.randint(-tremor_intensity, tremor_intensity)
            tremor_y = random.randint(-tremor_intensity, tremor_intensity)
            
            # 绘制恐惧的大椭圆眼睛
            self._draw_fear_eye(surface, self.left_eye_center, self.eye_width, 
                              self.eye_height, offset=(tremor_x, tremor_y))
            self._draw_fear_eye(surface, self.right_eye_center, self.eye_width, 
                              self.eye_height, offset=(tremor_x, tremor_y))
            
            # 绘制小O形嘴巴（也颤抖）
            mouth_center = (self.mouth_center[0] + tremor_x, self.mouth_center[1] + tremor_y)
            original_center = self.mouth_center
            self.mouth_center = mouth_center
            self._draw_mouth(surface, "surprised", intensity=0.6)
            self.mouth_center = original_center
            
            # 在眼睛周围绘制收缩线条（恐惧效果）
            if i % 4 < 2:
                for angle in [0, math.pi/4, math.pi/2, 3*math.pi/4]:
                    for eye_center in [self.left_eye_center, self.right_eye_center]:
                        start_radius = 55
                        end_radius = 45
                        start_x = eye_center[0] + math.cos(angle) * start_radius + tremor_x
                        start_y = eye_center[1] + math.sin(angle) * start_radius + tremor_y
                        end_x = eye_center[0] + math.cos(angle) * end_radius + tremor_x
                        end_y = eye_center[1] + math.sin(angle) * end_radius + tremor_y
                        pygame.draw.line(surface, self.WHITE, (start_x, start_y), (end_x, end_y), 1)
            
            frames.append(surface)
        
        return frames
    
    def _generate_focused_animation(self):
        """生成专注表情动画（八字眉 + 聚光灯效果）"""
        frames = []
        frame_count = 50
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 绘制八字形聚拢眉毛
            self._draw_converging_eyebrows(surface)
            
            # 绘制专注凝视的眼睛（完全静止，无微动）
            self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height)
            self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height)
            
            # 绘制直线嘴巴（严肃专注）
            self._draw_mouth(surface, "straight", intensity=0.8)
            
            # 从第10帧开始显示聚光灯效果
            if i >= 10:
                self._draw_spotlight_effect(surface)
            
            frames.append(surface)
        
        return frames
    
    def _generate_puzzled_animation(self):
        """生成迷惑表情动画（眼球不同方向运动）"""
        frames = []
        frame_count = 55
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 两只眼睛完全独立的随机运动
            left_eye_phase = i * 0.3
            right_eye_phase = i * 0.7 + math.pi/3
            
            left_offset_x = math.cos(left_eye_phase) * 20
            left_offset_y = math.sin(left_eye_phase * 1.3) * 12
            
            right_offset_x = math.cos(right_eye_phase) * 18
            right_offset_y = math.sin(right_eye_phase * 0.8) * 15
            
            # 绘制混乱移动的眼睛
            self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height,
                          offset=(left_offset_x, left_offset_y))
            self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height,
                          offset=(right_offset_x, right_offset_y))
            
            # 绘制扭曲的波浪嘴巴（更混乱）
            self._draw_mouth(surface, "wavy", intensity=1.2)
            
            # 随机出现多个问号
            if i % 10 < 4:
                question_pos1 = (self.screen_width // 2 + 70, self.left_eye_center[1] - 60)
                self._draw_symbol(surface, "question", question_pos1, 20)
            if i % 12 < 3:
                question_pos2 = (self.screen_width // 2 - 70, self.right_eye_center[1] - 55)
                self._draw_symbol(surface, "question", question_pos2, 18)
            if i % 15 < 2:
                ellipsis_pos = (self.screen_width // 2, self.left_eye_center[1] - 80)
                self._draw_symbol(surface, "ellipsis", ellipsis_pos, 16)
            
            frames.append(surface)
        
        return frames
    
    def _generate_triumphant_animation(self):
        """生成胜利表情动画（点头 + 皇冠/奖杯图标）"""
        frames = []
        frame_count = 45
        
        for i in range(frame_count):
            surface = self._create_surface()
            
            # 点头动作（上下移动）
            nod_progress = (i % 16) / 16.0
            nod_offset_y = math.sin(nod_progress * 2 * math.pi) * 6
            
            # 绘制自信的眼睛（稍微上扬）
            eye_y_offset = nod_offset_y - 3  # 稍微向上
            self._draw_eye(surface, self.left_eye_center, self.eye_width, self.eye_height,
                          offset=(0, eye_y_offset))
            self._draw_eye(surface, self.right_eye_center, self.eye_width, self.eye_height,
                          offset=(0, eye_y_offset))
            
            # 绘制得意的大笑嘴巴
            mouth_center = (self.mouth_center[0], self.mouth_center[1] + nod_offset_y)
            original_center = self.mouth_center
            self.mouth_center = mouth_center
            self._draw_mouth(surface, "big_smile", intensity=1.0)
            self.mouth_center = original_center
            
            # 皇冠和奖杯图标交替出现
            if i % 20 < 8:
                # 显示皇冠
                crown_pos = (self.screen_width // 2, self.left_eye_center[1] - 80 + nod_offset_y)
                self._draw_crown(surface, crown_pos, size=25)
            elif i % 20 < 16:
                # 显示奖杯
                trophy_pos = (self.screen_width // 2 - 40, self.left_eye_center[1] - 75 + nod_offset_y)
                self._draw_trophy(surface, trophy_pos, size=20)
                trophy_pos2 = (self.screen_width // 2 + 40, self.left_eye_center[1] - 70 + nod_offset_y)
                self._draw_trophy(surface, trophy_pos2, size=18)
            
            # 额外的庆祝效果：闪烁星星
            if i % 6 < 2:
                star_pos1 = (self.left_eye_center[0] - 80, self.left_eye_center[1] - 40)
                self._draw_star_sparkle(surface, star_pos1, size=8)
                star_pos2 = (self.right_eye_center[0] + 80, self.right_eye_center[1] - 35)
                self._draw_star_sparkle(surface, star_pos2, size=10)
            
            frames.append(surface)
        
        return frames
    
    def _generate_all_animations(self):
        """预生成所有动画序列"""
        print("Generating animations...")
        
        self.animations = {
            'blink': self._generate_blink_animation(),
            'happy': self._generate_happy_animation(),
            'surprised': self._generate_surprised_animation(),
            'look_left': self._generate_look_animation('left'),
            'look_right': self._generate_look_animation('right'),
            'look_up': self._generate_look_animation('up'),
            'look_down': self._generate_look_animation('down'),
            'wink': self._generate_wink_animation(),
            'confused': self._generate_confused_animation(),
            'idle': [self._generate_idle_frame()],  # 基础空闲帧
            
            # 新增的创意表情
            'joy': self._generate_joy_animation(),                    # 大笑表情
            'thinking': self._generate_thinking_animation(),          # 思考困惑
            'angry': self._generate_angry_animation(),               # 生气愤怒
            'sleepy': self._generate_sleepy_animation(),             # 疲惫瞌睡
            'surprised_mouth': self._generate_surprised_with_mouth_animation(),  # 带嘴巴的惊讶
            
            # 全新的10个多样化表情动画
            'sadness': self._generate_sadness_animation(),           # 悲伤/难过 - 泪珠下落
            'furious': self._generate_furious_animation(),           # 狂怒/咆哮 - 倒三角眼+锯齿嘴
            'shy': self._generate_shy_animation(),                   # 害羞/腼腆 - 手遮眼+偷看
            'mischievous': self._generate_mischievous_animation(),   # 恶作剧/狡猾 - 眨眼+挑眉+星星
            'bored': self._generate_bored_animation(),               # 无聊/不耐烦 - 眼皮下垂+打哈欠
            'excited': self._generate_excited_animation(),           # 兴奋/期待 - 跳动+心形图标
            'fear': self._generate_fear_animation(),                 # 恐惧/害怕 - 椭圆眼+颤抖
            'focused': self._generate_focused_animation(),           # 专注/思考 - 八字眉+聚光灯
            'puzzled': self._generate_puzzled_animation(),           # 迷惑/困惑 - 眼球乱动+多问号
            'triumphant': self._generate_triumphant_animation()      # 胜利/得意 - 点头+皇冠奖杯
        }
        
        print(f"Generated {len(self.animations)} animation sequences")
    
    def get_animation(self, animation_name):
        """获取指定动画序列"""
        return self.animations.get(animation_name, self.animations['idle'])
    
    def get_idle_frame_with_micro_movement(self):
        """获取带有微小运动的空闲帧"""
        # 生成随机微小偏移
        micro_x = random.randint(-2, 2)
        micro_y = random.randint(-1, 1)
        return self._generate_idle_frame((micro_x, micro_y))