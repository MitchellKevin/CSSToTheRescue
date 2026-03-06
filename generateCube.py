#!/usr/bin/env python3
"""
Rubik's 2x2 Cube State HTML Generator - FIXED
Each button links to correct next state based on actual move
"""

import json
import os
from pathlib import Path

class RubiksHTMLGenerator:
    """Genereert HTML files voor Rubik's cube states"""
    
    COLOR_MAP = {
        0: '#ffffff',  # White
        1: '#ffff00',  # Yellow
        2: '#ff0000',  # Red
        3: '#ff9900',  # Orange
        4: '#0066ff',  # Blue
        5: '#00aa00'   # Green
    }
    
    FACE_CLASSES = ['top', 'bottom', 'front', 'back', 'right', 'left']
    
    def __init__(self, output_dir='rubiks_states'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.state_to_index = {}
        
    def generate_sticker_html(self, color_code):
        """Generate HTML for one sticker"""
        color = self.COLOR_MAP[color_code]
        dark = self._darken_color(color)
        return f'<div class="sticker" style="background: linear-gradient(135deg, {color} 0%, {dark} 100%);"></div>'
    
    def _darken_color(self, color):
        """Darken a hex color"""
        darken_map = {
            '#ffffff': '#e0e0e0',
            '#ffff00': '#e6e600',
            '#ff0000': '#cc0000',
            '#ff9900': '#e68000',
            '#0066ff': '#0052cc',
            '#00aa00': '#008800',
        }
        return darken_map.get(color, color)
    
    def generate_face_html(self, face_colors, face_class):
        """Generate HTML for one face"""
        stickers = ''.join([self.generate_sticker_html(c) for c in face_colors])
        return f'<div class="face {face_class}">{stickers}</div>'
    
    def state_to_filename(self, state_index):
        """Convert state index to filename"""
        return f"state_{state_index:05d}.html"
    
    def state_to_key(self, state):
        """Convert state array to JSON string key"""
        return json.dumps(state)
    
    def apply_move_to_state(self, state, move):
        """Apply a move to a state and return new state"""
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
    
    def rotateFaceCW(self, face):
        return [face[2], face[0], face[3], face[1]]
    
    def rotateFaceCCW(self, face):
        return [face[1], face[3], face[0], face[2]]
    
    def moveR(self, state):
        temp = [state[0][1], state[0][3]]
        state[0][1] = state[3][0]
        state[0][3] = state[3][2]
        state[3][0] = state[1][1]
        state[3][2] = state[1][3]
        state[1][1] = state[2][1]
        state[1][3] = state[2][3]
        state[2][1] = temp[0]
        state[2][3] = temp[1]
        state[4] = self.rotateFaceCW(state[4])
    
    def moveRPrime(self, state):
        temp = [state[0][1], state[0][3]]
        state[0][1] = state[2][1]
        state[0][3] = state[2][3]
        state[2][1] = state[1][1]
        state[2][3] = state[1][3]
        state[1][1] = state[3][0]
        state[1][3] = state[3][2]
        state[3][0] = temp[0]
        state[3][2] = temp[1]
        state[4] = self.rotateFaceCCW(state[4])
    
    def moveL(self, state):
        temp = [state[0][0], state[0][2]]
        state[0][0] = state[2][0]
        state[0][2] = state[2][2]
        state[2][0] = state[1][0]
        state[2][2] = state[1][2]
        state[1][0] = state[3][3]
        state[1][2] = state[3][1]
        state[3][3] = temp[0]
        state[3][1] = temp[1]
        state[5] = self.rotateFaceCW(state[5])
    
    def moveLPrime(self, state):
        temp = [state[0][0], state[0][2]]
        state[0][0] = state[3][3]
        state[0][2] = state[3][1]
        state[3][3] = state[1][0]
        state[3][1] = state[1][2]
        state[1][0] = state[2][0]
        state[1][2] = state[2][2]
        state[2][0] = temp[0]
        state[2][2] = temp[1]
        state[5] = self.rotateFaceCCW(state[5])
    
    def moveU(self, state):
        temp = [state[2][0], state[2][1]]
        state[2][0] = state[5][0]
        state[2][1] = state[5][1]
        state[5][0] = state[3][0]
        state[5][1] = state[3][1]
        state[3][0] = state[4][0]
        state[3][1] = state[4][1]
        state[4][0] = temp[0]
        state[4][1] = temp[1]
        state[0] = self.rotateFaceCW(state[0])
    
    def moveUPrime(self, state):
        temp = [state[2][0], state[2][1]]
        state[2][0] = state[4][0]
        state[2][1] = state[4][1]
        state[4][0] = state[3][0]
        state[4][1] = state[3][1]
        state[3][0] = state[5][0]
        state[3][1] = state[5][1]
        state[5][0] = temp[0]
        state[5][1] = temp[1]
        state[0] = self.rotateFaceCCW(state[0])
    
    def moveD(self, state):
        temp = [state[2][2], state[2][3]]
        state[2][2] = state[4][2]
        state[2][3] = state[4][3]
        state[4][2] = state[3][2]
        state[4][3] = state[3][3]
        state[3][2] = state[5][2]
        state[3][3] = state[5][3]
        state[5][2] = temp[0]
        state[5][3] = temp[1]
        state[1] = self.rotateFaceCW(state[1])
    
    def moveDPrime(self, state):
        temp = [state[2][2], state[2][3]]
        state[2][2] = state[5][2]
        state[2][3] = state[5][3]
        state[5][2] = state[3][2]
        state[5][3] = state[3][3]
        state[3][2] = state[4][2]
        state[3][3] = state[4][3]
        state[4][2] = temp[0]
        state[4][3] = temp[1]
        state[1] = self.rotateFaceCCW(state[1])
    
    def find_next_state_index(self, state, move, all_states):
        """Find which state we go to after applying a move"""
        next_state = self.apply_move_to_state(state, move)
        next_state_key = self.state_to_key(next_state)
        
        if next_state_key in self.state_to_index:
            return self.state_to_index[next_state_key]
        
        return None
    
    def generate_html_page(self, state_data, state_index, total_states, all_states):
        """Generate single HTML page for a state"""
        
        state = state_data['state']
        moves = state_data.get('moves', [])
        
        faces_html = ''.join([
            self.generate_face_html(state[i], self.FACE_CLASSES[i])
            for i in range(6)
        ])
        
        move_sequence = ' -> '.join(moves) if moves else 'SOLVED'
        nav_buttons = self._generate_nav_buttons(state, state_index, all_states)
        
        html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rubik's 2x2 - State {state_index}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --white: #ffffff;
            --yellow: #ffff00;
            --red: #ff0000;
            --orange: #ff9900;
            --blue: #0066ff;
            --green: #00aa00;
            --dark-bg: #0a0e27;
            --accent: #00d9ff;
            --text: #f0f0f0;
        }}

        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1a3e 100%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            position: relative;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 217, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 128, 0.03) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }}

        .container {{
            position: relative;
            z-index: 2;
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            justify-content: center;
            align-items: flex-start;
            max-width: 1400px;
            padding: 2rem;
        }}

        h1 {{
            position: absolute;
            top: 1rem;
            left: 50%;
            transform: translateX(-50%);
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
            letter-spacing: 3px;
            color: var(--accent);
        }}

        .cube-container {{
            perspective: 1200px;
            width: 350px;
            height: 350px;
            position: relative;
            margin-top: 4rem;
        }}

        .cube {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: rotateStart 4s infinite linear;
        }}

        @keyframes rotateStart {{
            from {{
                transform: rotateX(20deg) rotateY(30deg);
            }}
            to {{
                transform: rotateX(20deg) rotateY(390deg);
            }}
        }}

        .face {{
            position: absolute;
            width: 100%;
            height: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
            padding: 8px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            background: rgba(0, 0, 0, 0.3);
        }}

        .sticker {{
            border-radius: 4px;
            border: 1px solid rgba(0, 0, 0, 0.5);
            box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.3),
                        0 2px 4px rgba(0, 0, 0, 0.5);
        }}

        .face.top {{ transform: rotateX(90deg) translateZ(175px); }}
        .face.bottom {{ transform: rotateX(-90deg) translateZ(175px); }}
        .face.front {{ transform: translateZ(175px); }}
        .face.back {{ transform: rotateY(180deg) translateZ(175px); }}
        .face.right {{ transform: rotateY(90deg) translateZ(175px); }}
        .face.left {{ transform: rotateY(-90deg) translateZ(175px); }}

        .controls {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 12px;
            padding: 2rem;
            width: 100%;
            max-width: 450px;
            backdrop-filter: blur(10px);
        }}

        .controls h2 {{
            font-size: 1.4em;
            margin-bottom: 1.5rem;
            color: var(--accent);
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .state-info {{
            text-align: center;
            margin-bottom: 1.5rem;
        }}

        .state-counter {{
            font-size: 2em;
            color: var(--accent);
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
            margin-bottom: 0.5rem;
        }}

        .move-sequence {{
            font-size: 0.9em;
            color: #aaa;
            word-break: break-word;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .button-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
            margin-bottom: 1.5rem;
        }}

        .move-btn {{
            padding: 0.9rem;
            font-size: 0.95em;
            font-weight: bold;
            border: 2px solid var(--accent);
            background: rgba(0, 217, 255, 0.1);
            color: var(--accent);
            border-radius: 6px;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-decoration: none;
            display: block;
            text-align: center;
            cursor: pointer;
        }}

        .move-btn:hover {{
            background: rgba(0, 217, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
        }}

        .right {{ border-color: var(--blue); color: var(--blue); }}
        .right:hover {{ background: rgba(0, 100, 255, 0.2); }}

        .left {{ border-color: var(--green); color: var(--green); }}
        .left:hover {{ background: rgba(0, 170, 0, 0.2); }}

        .top {{ border-color: var(--white); color: var(--white); }}
        .top:hover {{ background: rgba(255, 255, 255, 0.1); }}

        .bottom {{ border-color: var(--yellow); color: var(--yellow); }}
        .bottom:hover {{ background: rgba(255, 255, 0, 0.15); }}

        .nav-buttons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
        }}

        .nav-btn {{
            padding: 0.8rem;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.05);
            color: var(--text);
            border-radius: 6px;
            font-weight: bold;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
            text-decoration: none;
            display: block;
            text-align: center;
        }}

        .nav-btn:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--accent);
            color: var(--accent);
        }}

        .reset-btn {{
            grid-column: 1 / -1;
            background: rgba(255, 100, 100, 0.1);
            border-color: #ff6464;
            color: #ff6464;
        }}

        .reset-btn:hover {{
            background: rgba(255, 100, 100, 0.2);
        }}

        @media (max-width: 1024px) {{
            .cube-container {{ width: 300px; height: 300px; }}
            .controls {{ max-width: 100%; width: 100%; }}
        }}

        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8em; }}
            .container {{ flex-direction: column; align-items: center; }}
            .cube-container {{ width: 250px; height: 250px; }}
        }}
    </style>
</head>
<body>
    <h1>3D RUBIK'S 2x2</h1>

    <div class="container">
        <div class="cube-container">
            <div class="cube">
                {faces_html}
            </div>
        </div>

        <div class="controls">
            <h2>Controls</h2>

            <div class="state-info">
                <div class="state-counter">State {state_index} / {total_states}</div>
            </div>

            <div class="move-sequence">
                {move_sequence}
            </div>

            <div class="button-grid">
                {nav_buttons}
            </div>

            <div class="nav-buttons">
                <a href="state_00000.html" class="nav-btn reset-btn">Reset</a>
                <a href="index.html" class="nav-btn">Home</a>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_nav_buttons(self, state, state_index, all_states):
        """Generate move buttons with correct links"""
        moves = ['R', "R'", 'L', "L'", 'U', "U'", 'D', "D'"]
        move_classes = ['right', 'right', 'left', 'left', 'top', 'top', 'bottom', 'bottom']
        
        buttons = []
        
        for move, move_class in zip(moves, move_classes):
            next_idx = self.find_next_state_index(state, move, all_states)
            
            if next_idx is not None:
                filename = self.state_to_filename(next_idx)
            else:
                filename = "state_00000.html"
            
            buttons.append(
                f'<a href="{filename}" class="move-btn {move_class}">{move}</a>'
            )
        
        return '\n                '.join(buttons)
    
    def generate_all_pages(self, states_data, max_states=None):
        """Generate HTML pages for all states"""
        if max_states:
            states_to_process = states_data[:max_states]
        else:
            states_to_process = states_data
        
        total = len(states_to_process)
        
        print("Building state index...")
        for idx, state_data in enumerate(states_to_process):
            state_key = self.state_to_key(state_data['state'])
            self.state_to_index[state_key] = idx
        
        print(f"Generating {total} HTML pages...")
        
        for idx, state_data in enumerate(states_to_process):
            html_content = self.generate_html_page(
                state_data, idx, total, states_to_process
            )
            
            filename = self.state_to_filename(idx)
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            if (idx + 1) % 10 == 0:
                print(f"  Generated {idx + 1}/{total}")
        
        print(f"OK: All {total} pages generated")
    
    def generate_index(self, total_states):
        """Generate index.html"""
        html = """<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rubik's 2x2 Cube</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --dark-bg: #0a0e27;
            --accent: #00d9ff;
            --text: #f0f0f0;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1a3e 100%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 217, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 128, 0.03) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .container {
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 2rem;
        }
        
        h1 {
            font-size: 3em;
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
            letter-spacing: 3px;
            color: var(--accent);
            margin-bottom: 1rem;
        }
        
        p {
            font-size: 1.2em;
            margin-bottom: 2rem;
            color: #aaa;
        }
        
        .start-btn {
            padding: 1rem 2rem;
            font-size: 1.1em;
            border: 2px solid var(--accent);
            background: rgba(0, 217, 255, 0.1);
            color: var(--accent);
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
            display: inline-block;
        }
        
        .start-btn:hover {
            background: rgba(0, 217, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>3D RUBIK'S 2x2</h1>
        <p>Interactive 3D cube with """ + str(total_states) + """ different states</p>
        <a href="state_00000.html" class="start-btn">START</a>
    </div>
</body>
</html>"""
        
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"OK: index.html generated")


def main():
    """Main function"""
    try:
        print("Loading states from rubiks_states.json...")
        
        with open('states.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        states = data['states']
        print(f"Loaded {len(states)} states")
        
        generator = RubiksHTMLGenerator(output_dir='rubiks_states')
        generator.generate_all_pages(states, max_states=100)
        generator.generate_index(len(states))
        
        print("\nDONE! Open rubiks_states/index.html")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()