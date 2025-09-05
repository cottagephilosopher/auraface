# AuraFace - Robot Eye Expression System

A Python-based robot face expression system that displays natural, smooth, and lively animations with 25+ diverse facial expressions combining eyes and mouth on an 800x480 display.

## Features

- **Natural Eye + Mouth Animations**: Smooth blinking, emotional expressions, and coordinated facial movements
- **25+ Diverse Expressions**: From basic emotions to complex dynamic animations with special effects
- **Advanced Visual Elements**: Teardrops, lightning bolts, hearts, crowns, trophies, sparkles, and hand gestures
- **State Machine Management**: Clean state transitions between all expressions with automatic timeouts
- **Automatic Behaviors**: Random blinking and micro-movements in idle state
- **Rich Animation Effects**: Trembling, bouncing, peeking, nodding, and independent eye movements
- **Real-time Control**: Comprehensive keyboard input for instant expression changes

## System Requirements

- Python 3.7+
- 800x480 display (optimized for this resolution)
- pygame library

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
Run the main program for manual control:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

### Auto Demo Mode
Run the slideshow demo to see all expressions automatically:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python demo_slideshow.py
```

**Demo Controls:**
- **SPACE** - Pause/Resume slideshow
- **←/→ Arrows** - Manual expression switching
- **ESC** - Exit demo

### Controls

**Basic Expressions:**
- **H** - Happy expression
- **S** - Surprised expression  
- **C** - Confused expression
- **W** - Wink
- **L** - Look left, **R** - Look right
- **U** - Look up, **D** - Look down
- **I** - Return to idle state

**🎭 Creative Expressions:**
- **J** - Joy/Laughter (crescent eyes + wide smile + sparkles)
- **T** - Thinking/Confused (scanning eyes + wavy mouth + question marks)
- **A** - Angry (angled eyebrows + frown + shake effect)
- **Z** - Sleepy/Tired (half-closed eyes + straight mouth + floating Z symbols)
- **X** - Surprised with mouth (big eyes + O-shaped mouth)

**🌟 Advanced Emotions:**
- **Q** - Sadness (drooping eyes + falling teardrops)
- **F** - Furious (triangle eyes + jagged mouth + intense vibration + lightning)
- **Y** - Shy (hand covering eye + peeking motion + gentle smile)
- **M** - Mischievous (winking + raised eyebrow + star sparkles)
- **B** - Bored (drooping eyelids + yawn motion + slow movements)
- **E** - Excited (bouncing eyes + floating hearts + big smile)
- **N** - Fear (elongated oval eyes + continuous trembling + panic lines)
- **O** - Focused (converging eyebrows + steady gaze + spotlight effect)
- **P** - Puzzled (independent chaotic eye movements + multiple question marks)
- **V** - Triumphant (nodding motion + crown/trophy icons + victory sparkles)

**System:**
- **ESC** - Exit program

## File Structure

- `main.py` - Main program with Pygame setup and event handling
- `demo_slideshow.py` - Automated slideshow demo of all 25 expressions
- `animations.py` - Advanced eye drawing and animation frame generation with smooth effects
- `state_machine.py` - State management with smooth transitions and automatic behaviors
- `requirements.txt` - Python dependencies

## Features Details

### Automatic Behaviors (Idle State)
- Random blinking every 3-8 seconds
- Subtle micro-movements every 0.5-2 seconds
- Smooth transitions between all states

### Animations

**Basic Expressions:**
- **Blinking**: 12-frame smooth blink animation
- **Happy**: Eyes transform to crescent moon shape
- **Surprised**: Eyes enlarge with visible pupils
- **Confused**: Slow left-right scanning motion
- **Directional Looking**: Smooth eye movement in 4 directions
- **Winking**: Single eye blink animation

**🎭 Creative Facial Expressions:**
- **Joy**: 25-frame crescent eyes + wide smile + twinkling sparkles
- **Thinking**: 50-frame eye scanning + wavy mouth + floating question marks/ellipsis
- **Angry**: 20-frame angled eyebrows + frown + subtle shake effects
- **Sleepy**: 40-frame drooping eyelids + straight mouth + drifting Z symbols  
- **Surprised (with mouth)**: 20-frame enlarged eyes + O-shaped mouth coordination

**🌟 Advanced Emotion Animations:**
- **Sadness**: 45-frame drooping eyes + cascading teardrops + downward mouth
- **Furious**: 35-frame inverted triangle eyes + jagged roaring mouth + lightning + intense vibration
- **Shy**: 50-frame hand covering/uncovering eye + peek animations + gentle smile progression
- **Mischievous**: 30-frame rapid winking + raised eyebrow + star sparkle effects
- **Bored**: 60-frame slow eye droop cycles + yawning mouth movements + lethargy effects
- **Excited**: 40-frame bouncing eyes/mouth + floating heart icons + high energy
- **Fear**: 45-frame enlarged oval eyes + panic lines + continuous trembling effects
- **Focused**: 50-frame converging eyebrows + steady gaze + spotlight concentration effect
- **Puzzled**: 55-frame chaotic independent eye movements + multiple floating question marks
- **Triumphant**: 45-frame nodding motions + crown/trophy alternation + celebration sparkles

**Visual Elements:**
- **Mouth Shapes**: Smiles, frowns, wavy lines, O-shapes, straight lines, jagged roar
- **Special Symbols**: Question marks, ellipsis, Z/ZZ sleep symbols, hearts, crowns, trophies
- **Advanced Effects**: Hand gestures, teardrops, lightning bolts, panic lines, spotlight beams
- **Dynamic Motions**: Trembling, bouncing, nodding, peeking, independent eye movements

All animations run at 60 FPS for maximum smoothness and natural appearance.

## Smooth Animation System

### Advanced Visual Technology
- **Anti-aliased Drawing**: Smooth ellipses and curves with multi-layer rendering
- **Bézier Curves**: Mathematical precision for organic shapes like teardrops and hearts
- **30fps Animation Engine**: High-quality motion with sophisticated timing
- **12-frame Transitions**: Ultra-smooth expression changes with seamless blending

### Natural Motion Physics
- **10 Advanced Easing Functions**: Bounce, elastic, anticipation, overshoot effects
- **Physics-based Animation**: Realistic acceleration, momentum, and natural timing
- **Emotion-adaptive Timing**: Different expressions use optimal easing curves
- **Micro-movement System**: Subtle life-like animations even in idle state

### Expression Transition System
- **Alpha Blending**: Smooth cross-fade between any two expressions
- **Automatic Transition Detection**: Smart selection of optimal easing functions
- **Frame Interpolation**: Mathematical blending of animation frames
- **Seamless State Changes**: No abrupt jumps between emotional states

The system now provides cinema-quality smooth animations that feel natural and alive!