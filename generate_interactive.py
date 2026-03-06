#!/usr/bin/env python3
"""
Rubik's 2x2 Cube - Interactive user-controlled moves
Generate all states with correct move links in your HTML/CSS format
"""

import json
from pathlib import Path

class InteractiveCubeGenerator:
    """Generates interactive cube where user can click to perform moves"""
    
    COLOR_MAP = {
        0: 'white',
        1: 'yellow', 
        2: 'red',
        3: 'orange',
        4: 'blue',
        5: 'green'
    }
    
    FACE_ORDER = [0, 2, 4, 5, 3, 1]  # top, front, right, left, back, bottom
    MOVES = ['R', "R'", 'L', "L'", 'U', "U'", 'D', "D'"]
    
    def __init__(self):
        self.state_to_index = {}
        self.state_index_list = []
    
    def apply_move(self, state, move):
        """Apply move to state"""
        new_state = [face[:] for face in state]
        
        if move == 'R':
            self.moveR(new_state)
        elif move == "R'":
            self.moveRPrime(new_state)
        elif move == 'L':
            self.moveL(new_state)
        elif move == "L'":
            self.moveLPrime(new_state)
        elif move == 'U':
            self.moveU(new_state)
        elif move == "U'":
            self.moveUPrime(new_state)
        elif move == 'D':
            self.moveD(new_state)
        elif move == "D'":
            self.moveDPrime(new_state)
        
        return new_state
    
    def rotateCW(self, face):
        return [face[2], face[0], face[3], face[1]]
    
    def rotateCCW(self, face):
        return [face[1], face[3], face[0], face[2]]
    
    def moveR(self, state):
        temp = [state[0][1], state[0][3]]
        state[0][1], state[0][3] = state[3][0], state[3][2]
        state[3][0], state[3][2] = state[1][1], state[1][3]
        state[1][1], state[1][3] = state[2][1], state[2][3]
        state[2][1], state[2][3] = temp[0], temp[1]
        state[4] = self.rotateCW(state[4])
    
    def moveRPrime(self, state):
        temp = [state[0][1], state[0][3]]
        state[0][1], state[0][3] = state[2][1], state[2][3]
        state[2][1], state[2][3] = state[1][1], state[1][3]
        state[1][1], state[1][3] = state[3][0], state[3][2]
        state[3][0], state[3][2] = temp[0], temp[1]
        state[4] = self.rotateCCW(state[4])
    
    def moveL(self, state):
        temp = [state[0][0], state[0][2]]
        state[0][0], state[0][2] = state[2][0], state[2][2]
        state[2][0], state[2][2] = state[1][0], state[1][2]
        state[1][0], state[1][2] = state[3][3], state[3][1]
        state[3][3], state[3][1] = temp[0], temp[1]
        state[5] = self.rotateCW(state[5])
    
    def moveLPrime(self, state):
        temp = [state[0][0], state[0][2]]
        state[0][0], state[0][2] = state[3][3], state[3][1]
        state[3][3], state[3][1] = state[1][0], state[1][2]
        state[1][0], state[1][2] = state[2][0], state[2][2]
        state[2][0], state[2][2] = temp[0], temp[1]
        state[5] = self.rotateCCW(state[5])
    
    def moveU(self, state):
        temp = [state[2][0], state[2][1]]
        state[2][0], state[2][1] = state[5][0], state[5][1]
        state[5][0], state[5][1] = state[3][0], state[3][1]
        state[3][0], state[3][1] = state[4][0], state[4][1]
        state[4][0], state[4][1] = temp[0], temp[1]
        state[0] = self.rotateCW(state[0])
    
    def moveUPrime(self, state):
        temp = [state[2][0], state[2][1]]
        state[2][0], state[2][1] = state[4][0], state[4][1]
        state[4][0], state[4][1] = state[3][0], state[3][1]
        state[3][0], state[3][1] = state[5][0], state[5][1]
        state[5][0], state[5][1] = temp[0], temp[1]
        state[0] = self.rotateCCW(state[0])
    
    def moveD(self, state):
        temp = [state[2][2], state[2][3]]
        state[2][2], state[2][3] = state[4][2], state[4][3]
        state[4][2], state[4][3] = state[3][2], state[3][3]
        state[3][2], state[3][3] = state[5][2], state[5][3]
        state[5][2], state[5][3] = temp[0], temp[1]
        state[1] = self.rotateCW(state[1])
    
    def moveDPrime(self, state):
        temp = [state[2][2], state[2][3]]
        state[2][2], state[2][3] = state[5][2], state[5][3]
        state[5][2], state[5][3] = state[3][2], state[3][3]
        state[3][2], state[3][3] = state[4][2], state[4][3]
        state[4][2], state[4][3] = temp[0], temp[1]
        state[1] = self.rotateCCW(state[1])
    
    def state_to_key(self, state):
        return json.dumps(state)
    
    def generate_css_for_state(self, state, state_idx):
        """Generate CSS rules for one state"""
        css = f"\n/* STATE {state_idx:05d} */\n"
        
        layer_names = ['top', 'mid', 'bot']
        
        for layer_idx, layer_name in enumerate(layer_names):
            cubie_num = 1
            
            for row in range(3):
                for col in range(3):
                    css += f"#cubeState_{state_idx:05d} .layer.{layer_name} > div:nth-child({cubie_num}) > div {{\n"
                    
                    face_rules = []
                    for face_pos, face_idx in enumerate(self.FACE_ORDER):
                        sticker_idx = row * 3 + col
                        if sticker_idx < 4:
                            color_code = state[face_idx][sticker_idx]
                        else:
                            color_code = 0
                        
                        color_name = self.COLOR_MAP[color_code]
                        face_rules.append(f"--face{face_pos + 1}: {color_name};")
                    
                    css += " ".join(face_rules) + "}\n"
                    cubie_num += 1
        
        for i in range(1, 7):
            css += f"#cubeState_{state_idx:05d} .layer > div > div:nth-child({i}) {{ background: var(--face{i}); }}\n"
        
        return css
    
    def generate_html(self, states_data, max_states=100):
        """Generate interactive HTML with all states"""
        
        # Build state index
        print(f"Building state index for {min(max_states, len(states_data))} states...")
        for idx, state_data in enumerate(states_data[:max_states]):
            key = self.state_to_key(state_data['state'])
            self.state_to_index[key] = idx
            self.state_index_list.append(state_data['state'])
        
        # Generate CSS for all states
        print("Generating CSS for all states...")
        css_rules = ""
        for idx in range(min(max_states, len(states_data))):
            state = states_data[idx]['state']
            css_rules += self.generate_css_for_state(state, idx)
        
        # Generate radio buttons for each state
        radio_inputs = ""
        for idx in range(min(max_states, len(states_data))):
            radio_inputs += f'<input type="radio" name="step" id="s{idx:05d}"{"checked" if idx == 0 else ""}>\n'
        
        # Generate scene divs with move buttons
        scene_divs = ""
        for idx in range(min(max_states, len(states_data))):
            state = states_data[idx]['state']
            
            scene_divs += f'  <div id="cubeState_{idx:05d}">\n'
            scene_divs += '    <div class="layer top">\n'
            for i in range(9):
                scene_divs += '      <div><div></div><div></div><div></div><div></div><div></div><div></div></div>\n'
            scene_divs += '    </div>\n'
            
            scene_divs += '    <div class="layer mid">\n'
            for i in range(9):
                scene_divs += '      <div><div></div><div></div><div></div><div></div><div></div><div></div></div>\n'
            scene_divs += '    </div>\n'
            
            scene_divs += '    <div class="layer bot">\n'
            for i in range(9):
                scene_divs += '      <div><div></div><div></div><div></div><div></div><div></div><div></div></div>\n'
            scene_divs += '    </div>\n'
            
            # Add move buttons for this state
            scene_divs += '    <div class="moves">\n'
            for move in self.MOVES:
                next_state = self.apply_move(state, move)
                next_key = self.state_to_key(next_state)
                next_idx = self.state_to_index.get(next_key, 0)
                scene_divs += f'      <a href="#s{next_idx:05d}" class="move-btn">{move}</a>\n'
            scene_divs += '    </div>\n'
            
            scene_divs += '  </div>\n'
        
        # Generate control buttons
        control_buttons = ""
        for idx in range(min(max_states, len(states_data))):
            control_buttons += f'  <label for="s{idx:05d}">{idx}</label>\n'
        
        # Complete HTML
        html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<title>Rubik's 2x2 Cube - Interactive</title>
<style>
/* ===== RESET / SCENE ===== */

body {{
  margin:0;
  font-family:sans-serif;
  background:#222;
  color:white;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content: center;
  height: 100vh;
}}

input[type="radio"] {{ display: none; }}

h2 {{
  position: absolute;
  color: rgba(255,255,255,0.1);
  top: 10%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  font-size: 3em;
  width: 100vw;
  text-align: center;
}}

#scene {{
  width: min(90vw, 90vh);
  height: min(90vw, 90vh);
  perspective: 1200px;
  z-index: 1;
  position: relative;
}}

/* ===== CUBE STATES ===== */
[id^="cubeState_"] {{
  display: none;
  position: relative;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
  transform: rotateX(-30deg) rotateY(30deg);
  left: 45%;
  top: 50%;
}}

/* Show current state based on radio selection */
{chr(10).join([f's{idx:05d}:checked ~ #scene #cubeState_{idx:05d} {{ display: block; }}' for idx in range(min(max_states, len(states_data)))])}

/* ===== LAYER WRAPPERS ===== */
.layer {{
  position: absolute;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
}}

.layer.top {{ transform: translateY(-70px); }}
.layer.mid {{ transform: translateY(  0px); }}
.layer.bot {{ transform: translateY( 70px); }}

/* ===== CUBIES ===== */
.layer > div {{
  position: absolute;
  width: 90px;
  height: 60px;
  transform-style: preserve-3d;
  transform: translate3d(var(--x), 0px, var(--z));
}}

.layer > div:nth-child(3n+1) {{ --x: -70px;}}
.layer > div:nth-child(3n+2) {{ --x:   0px; }}
.layer > div:nth-child(3n)   {{ --x:  70px; }}

.layer > div:nth-child(-n+3)            {{ --z:  70px; }}
.layer > div:nth-child(n+4):nth-child(-n+6) {{ --z:   0px; }}
.layer > div:nth-child(n+7)             {{ --z: -70px; }}

/* ===== FACES ===== */
.layer > div > div {{
  position: absolute;
  width: 60px;
  height: 60px;
  border: 1.5px solid rgb(0, 0, 0);
  backface-visibility: hidden;
}}

.layer > div > div:nth-child(1) {{ transform: translateZ(30px); }}
.layer > div > div:nth-child(2) {{ transform: rotateY(180deg) translateZ(30px); }}
.layer > div > div:nth-child(3) {{ transform: rotateY( 90deg) translateZ(30px); }}
.layer > div > div:nth-child(4) {{ transform: rotateY(-90deg) translateZ(30px); }}
.layer > div > div:nth-child(5) {{ transform: rotateX( 90deg) translateZ(30px); }}
.layer > div > div:nth-child(6) {{ transform: rotateX(-90deg) translateZ(30px); }}

/* ===== GENERATED STATE CSS ===== */
{css_rules}

/* ===== MOVE BUTTONS ===== */
.moves {{
  position: absolute;
  bottom: -200px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  width: 400px;
}}

.move-btn {{
  padding: 10px 15px;
  background: #444;
  color: #fff;
  border: 2px solid #666;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
  font-family: monospace;
  transition: all 0.2s;
}}

.move-btn:hover {{
  background: #555;
  border-color: #999;
}}

.move-btn:active {{
  transform: scale(0.95);
}}

/* ===== CONTROLS ===== */
#controls {{
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  max-width: 600px;
}}

#controls > label {{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: #444;
  color: #fff;
  font-family: monospace;
  font-size: 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid #666;
  transition: background .15s, border-color .15s;
}}

#controls > label:hover {{ background: #555; }}

{chr(10).join([f's{idx:05d}:checked ~ #controls label[for="s{idx:05d}"] {{ background: #5a5a5a; color: #fff; border-color: #999; }}' for idx in range(min(max_states, len(states_data)))])}
</style>
</head>
<body>

<h2>RUBIK'S 2x2</h2>

{radio_inputs}
<div id="scene">
{scene_divs}</div>

<div id="controls">
{control_buttons}</div>

</body>
</html>"""
        
        return html
    
    def save(self, html_content, filename='interactive_cube.html'):
        """Save HTML"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"OK: Saved to {filename}")


def main():
    try:
        print("Loading rubiks_states.json...")
        with open('rubiks_states.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        states = data['states']
        print(f"Loaded {len(states)} states")
        
        generator = InteractiveCubeGenerator()
        html = generator.generate_html(states, max_states=100)
        generator.save(html, filename='interactive_cube.html')
        
        print("\nDONE! Open interactive_cube.html in your browser")
        print("Click the move buttons (R, R', L, L', U, U', D, D') to navigate between states")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
