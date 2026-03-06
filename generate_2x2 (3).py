#!/usr/bin/env python3
"""
Rubik's 2x2 Cube - 7 moves possible
Pure HTML/CSS interactive cube
"""

import json
from pathlib import Path

class Rubiks2x2Generator:
    """Generates 2x2 cube states for 7 moves"""
    
    COLOR_MAP = {
        0: 'white',
        1: 'yellow', 
        2: 'red',
        3: 'orange',
        4: 'blue',
        5: 'green'
    }
    
    def __init__(self):
        self.state_to_index = {}
        self.state_list = []
    
    def apply_move(self, state, move):
        """Apply move to state"""
        new_state = [face[:] for face in state]
        
        if move == 'L':
            self.moveL(new_state)
        elif move == 'R':
            self.moveR(new_state)
        elif move == 'U':
            self.moveU(new_state)
        elif move == 'B':
            self.moveB(new_state)
        
        return new_state
    
    def rotateCW(self, face):
        return [face[2], face[0], face[3], face[1]]
    
    def rotateCCW(self, face):
        return [face[1], face[3], face[0], face[2]]
    
    def moveL(self, state):
        """Left turn clockwise (looking from left)"""
        temp = [state[0][0], state[0][2]]
        state[0][0], state[0][2] = state[2][0], state[2][2]
        state[2][0], state[2][2] = state[1][0], state[1][2]
        state[1][0], state[1][2] = state[3][3], state[3][1]
        state[3][3], state[3][1] = temp[0], temp[1]
        state[5] = [state[5][2], state[5][0], state[5][3], state[5][1]]
    
    def moveR(self, state):
        """Right turn clockwise (looking from right)"""
        # Back face indices are mirrored: top[1,3] -> back[2,0], back[2,0] -> bottom[1,3]
        temp = [state[0][1], state[0][3]]
        state[0][1], state[0][3] = state[3][2], state[3][0]
        state[3][2], state[3][0] = state[1][1], state[1][3]
        state[1][1], state[1][3] = state[2][1], state[2][3]
        state[2][1], state[2][3] = temp[0], temp[1]
        state[4] = [state[4][2], state[4][0], state[4][3], state[4][1]]
    
    def moveU(self, state):
        """Up turn clockwise (looking from top)"""
        # Top layer rotates: Front -> Right -> Back -> Left -> Front
        # Back stickers need to be reversed when cycling
        temp = [state[2][0], state[2][1]]
        state[2][0], state[2][1] = state[5][0], state[5][1]
        state[5][0], state[5][1] = state[3][1], state[3][0]  # Back reversed
        state[3][1], state[3][0] = state[4][0], state[4][1]  # Back reversed
        state[4][0], state[4][1] = temp[0], temp[1]
        # Rotate top face clockwise
        state[0] = [state[0][2], state[0][0], state[0][3], state[0][1]]
    
    def moveB(self, state):
        """Bottom turn clockwise (looking from bottom)"""
        # Bottom layer rotates: Front -> Right -> Back -> Left -> Front
        # Back stickers need to be reversed when cycling
        temp = [state[2][2], state[2][3]]
        state[2][2], state[2][3] = state[4][2], state[4][3]
        state[4][2], state[4][3] = state[3][3], state[3][2]  # Back reversed
        state[3][3], state[3][2] = state[5][2], state[5][3]  # Back reversed
        state[5][2], state[5][3] = temp[0], temp[1]
        # Rotate bottom face clockwise
        state[1] = [state[1][2], state[1][0], state[1][3], state[1][1]]
    
    def state_to_key(self, state):
        return json.dumps(state)
    
    def generate_html(self, states_data):
        """Generate HTML with states for 7 moves"""
        
        # Max possible states: roughly 4^7 but we limit to available
        max_states = min(2000, len(states_data))
        
        print(f"Building state index for {max_states} states (allows 7 moves)...")
        for idx, state_data in enumerate(states_data[:max_states]):
            key = self.state_to_key(state_data['state'])
            self.state_to_index[key] = idx
            self.state_list.append(state_data['state'])
        
        print("Generating HTML...")
        
        # Generate HTML with states
        radio_inputs = ""
        scene_divs = ""
        display_rules = ""
        move_buttons_css = ""
        move_buttons_html = ""
        
        for idx in range(max_states):
            state = states_data[idx]['state']
            radio_inputs += f'  <input type="radio" name="state" id="s{idx:04d}" {"checked" if idx == 0 else ""}>\n'
            
            display_rules += f"#s{idx:04d}:checked ~ #scene #cubeState_{idx:04d} {{ display: block; }}\n"
            move_buttons_css += f"#s{idx:04d}:checked ~ .controls #move{idx:04d} {{ display: flex; gap: 15px; }}\n"
            
            # Generate scene div
            scene_divs += f'  <div id="cubeState_{idx:04d}">\n'
            scene_divs += self.generate_2x2_cube_html(state)
            scene_divs += '  </div>\n'
            
            # Generate move buttons for this state
            move_buttons_html += f'    <div class="move-controls" id="move{idx:04d}">\n'
            
            for move in ['L', 'R', 'U', 'B']:
                next_state = self.apply_move(state, move)
                next_key = self.state_to_key(next_state)
                next_idx = self.state_to_index.get(next_key, 0)
                move_buttons_html += f'      <label for="s{next_idx:04d}" class="move-btn move-{move}">{move}</label>\n'
            
            move_buttons_html += '    </div>\n'
        
        html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<title>Rubik's 2x2 Cube - 7 Moves</title>
<style>
/* ===== RESET ===== */
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: sans-serif;
  background: #1a1a1a;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}}

h1 {{
  position: absolute;
  top: 30px;
  font-size: 2.5em;
  letter-spacing: 3px;
  color: #fff;
}}

.move-counter {{
  position: absolute;
  top: 100px;
  font-size: 1.2em;
  color: #aaa;
}}

/* ===== SCENE ===== */
#scene {{
  width: 400px;
  height: 400px;
  perspective: 1200px;
  position: relative;
  margin-bottom: 150px;
}}

/* ===== CUBE STATES ===== */
[id^="cubeState_"] {{
  display: none;
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(-20deg) rotateY(30deg);
}}

{display_rules}

/* ===== 2x2 CUBIES ===== */
.cubie {{
  position: absolute;
  width: 100px;
  height: 100px;
  transform-style: preserve-3d;
}}

/* Position 8 cubies in 2x2x2 */
/* Front layer */
.cubie.f-tl {{ transform: translateX(-50px) translateY(-50px) translateZ(50px); }}
.cubie.f-tr {{ transform: translateX(50px) translateY(-50px) translateZ(50px); }}
.cubie.f-bl {{ transform: translateX(-50px) translateY(50px) translateZ(50px); }}
.cubie.f-br {{ transform: translateX(50px) translateY(50px) translateZ(50px); }}

/* Back layer */
.cubie.b-tl {{ transform: translateX(-50px) translateY(-50px) translateZ(-50px); }}
.cubie.b-tr {{ transform: translateX(50px) translateY(-50px) translateZ(-50px); }}
.cubie.b-bl {{ transform: translateX(-50px) translateY(50px) translateZ(-50px); }}
.cubie.b-br {{ transform: translateX(50px) translateY(50px) translateZ(-50px); }}

/* ===== STICKER FACES ===== */
.face {{
  position: absolute;
  width: 100px;
  height: 100px;
  border: 2px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}}

/* Front face stickers */
.cubie .face-front {{ 
  transform: translateZ(50px);
}}

/* Back face stickers */
.cubie .face-back {{ 
  transform: rotateY(180deg) translateZ(50px);
}}

/* Top face stickers */
.cubie .face-top {{ 
  transform: rotateX(90deg) translateZ(50px);
}}

/* Bottom face stickers */
.cubie .face-bottom {{ 
  transform: rotateX(-90deg) translateZ(50px);
}}

/* Right face stickers */
.cubie .face-right {{ 
  transform: rotateY(90deg) translateZ(50px);
}}

/* Left face stickers */
.cubie .face-left {{ 
  transform: rotateY(-90deg) translateZ(50px);
}}

/* ===== MOVE CONTROLS ===== */
.controls {{
  position: absolute;
  bottom: 30px;
  display: flex;
  gap: 15px;
  z-index: 10;
}}

.move-controls {{
  display: none;
}}

{move_buttons_css}

.move-btn {{
  padding: 15px 25px;
  background: #333;
  color: white;
  border: 3px solid #666;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1em;
  transition: all 0.2s;
  text-decoration: none;
  display: block;
}}

.move-btn:hover {{
  background: #444;
  border-color: #999;
  transform: scale(1.05);
}}

.move-btn:active {{
  transform: scale(0.95);
}}

/* Move button colors */
.move-L {{ border-color: #00ff00; color: #00ff00; }}
.move-R {{ border-color: #00ffff; color: #00ffff; }}
.move-U {{ border-color: #ffff00; color: #ffff00; }}
.move-B {{ border-color: #ff00ff; color: #ff00ff; }}

.move-L:hover {{ background: rgba(0, 255, 0, 0.1); }}
.move-R:hover {{ background: rgba(0, 255, 255, 0.1); }}
.move-U:hover {{ background: rgba(255, 255, 0, 0.1); }}
.move-B:hover {{ background: rgba(255, 0, 255, 0.1); }}

/* Hide radio inputs */
input[type="radio"] {{ display: none; }}

</style>
</head>
<body>

<h1>RUBIK'S 2×2</h1>
<div class="move-counter">Can do 7 moves</div>

{radio_inputs}
<div id="scene">
{scene_divs}</div>

<div class="controls">
{move_buttons_html}</div>

</body>
</html>"""
        
        return html
    
    def generate_2x2_cube_html(self, state):
        """Generate HTML structure for 2x2 cube with correct colors"""
        html = '    <div class="cubie f-tl">\n'
        html += f'      <div class="face face-front" style="background:{self.get_color(state[2][0])}"></div>\n'
        html += f'      <div class="face face-top" style="background:{self.get_color(state[0][0])}"></div>\n'
        html += f'      <div class="face face-left" style="background:{self.get_color(state[5][0])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie f-tr">\n'
        html += f'      <div class="face face-front" style="background:{self.get_color(state[2][1])}"></div>\n'
        html += f'      <div class="face face-top" style="background:{self.get_color(state[0][1])}"></div>\n'
        html += f'      <div class="face face-right" style="background:{self.get_color(state[4][0])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie f-bl">\n'
        html += f'      <div class="face face-front" style="background:{self.get_color(state[2][2])}"></div>\n'
        html += f'      <div class="face face-bottom" style="background:{self.get_color(state[1][0])}"></div>\n'
        html += f'      <div class="face face-left" style="background:{self.get_color(state[5][2])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie f-br">\n'
        html += f'      <div class="face face-front" style="background:{self.get_color(state[2][3])}"></div>\n'
        html += f'      <div class="face face-bottom" style="background:{self.get_color(state[1][1])}"></div>\n'
        html += f'      <div class="face face-right" style="background:{self.get_color(state[4][2])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie b-tl">\n'
        html += f'      <div class="face face-back" style="background:{self.get_color(state[3][3])}"></div>\n'
        html += f'      <div class="face face-top" style="background:{self.get_color(state[0][2])}"></div>\n'
        html += f'      <div class="face face-left" style="background:{self.get_color(state[5][3])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie b-tr">\n'
        html += f'      <div class="face face-back" style="background:{self.get_color(state[3][2])}"></div>\n'
        html += f'      <div class="face face-top" style="background:{self.get_color(state[0][3])}"></div>\n'
        html += f'      <div class="face face-right" style="background:{self.get_color(state[4][3])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie b-bl">\n'
        html += f'      <div class="face face-back" style="background:{self.get_color(state[3][1])}"></div>\n'
        html += f'      <div class="face face-bottom" style="background:{self.get_color(state[1][2])}"></div>\n'
        html += f'      <div class="face face-left" style="background:{self.get_color(state[5][1])}"></div>\n'
        html += '    </div>\n'
        
        html += '    <div class="cubie b-br">\n'
        html += f'      <div class="face face-back" style="background:{self.get_color(state[3][0])}"></div>\n'
        html += f'      <div class="face face-bottom" style="background:{self.get_color(state[1][3])}"></div>\n'
        html += f'      <div class="face face-right" style="background:{self.get_color(state[4][1])}"></div>\n'
        html += '    </div>\n'
        
        return html
    
    def get_color(self, color_code):
        """Convert color code to hex"""
        colors = {
            0: '#ffffff',  # white
            1: '#ffff00',  # yellow
            2: '#ff0000',  # red
            3: '#ff9900',  # orange
            4: '#0066ff',  # blue
            5: '#00aa00'   # green
        }
        return colors.get(color_code, '#fff')
    
    def save(self, html_content):
        with open('rubiks_2x2.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("OK: Saved to rubiks_2x2.html")


def main():
    try:
        print("Loading rubiks_states.json...")
        with open('rubiks_states.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        states = data['states']
        print(f"Loaded {len(states)} states")
        
        generator = Rubiks2x2Generator()
        html = generator.generate_html(states)
        generator.save(html)
        
        print("\nDONE! Open rubiks_2x2.html in your browser")
        print("You can now do 7 moves! Use L, R, U, B buttons to rotate")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
