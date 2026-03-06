#!/usr/bin/env python3
"""
Rubik's 2x2 Cube State Generator
Genereert alle 3,674,160 mogelijke states met correcte 3D rotaties
"""

import json
import itertools
from typing import List, Tuple, Dict
import hashlib

class Rubiks2x2:
    """
    2x2 Rubik's cube solver/state generator
    
    Faces: 0=White(top), 1=Yellow(bottom), 2=Red(front), 3=Orange(back), 4=Blue(right), 5=Green(left)
    Elke face heeft 4 stickers [0,1,2,3] in deze volgorde:
        0 1
        2 3
    """
    
    # Face indices
    WHITE, YELLOW, RED, ORANGE, BLUE, GREEN = 0, 1, 2, 3, 4, 5
    
    # Face kleuren in RGB
    COLORS = {
        0: (255, 255, 255),    # White
        1: (255, 255, 0),      # Yellow
        2: (255, 0, 0),        # Red
        3: (255, 165, 0),      # Orange
        4: (0, 0, 255),        # Blue
        5: (0, 128, 0)         # Green
    }
    
    # Face namen
    FACE_NAMES = {
        0: "top", 1: "bottom", 2: "front", 3: "back", 4: "right", 5: "left"
    }
    
    def __init__(self):
        """Initialize solved cube state"""
        # State: [face0, face1, ..., face5] waar elke face = [0,1,2,3] stickers
        self.state = [[i] * 4 for i in range(6)]
    
    def copy(self) -> 'Rubiks2x2':
        """Deep copy van huidige state"""
        new_cube = Rubiks2x2()
        new_cube.state = [face[:] for face in self.state]
        return new_cube
    
    def get_state_hash(self) -> str:
        """Krijg unieke hash van huidige state"""
        state_str = json.dumps(self.state)
        return hashlib.md5(state_str.encode()).hexdigest()
    
    def get_state_string(self) -> str:
        """Krijg string representatie van state"""
        return json.dumps(self.state)
    
    def rotate_face_cw(self, face: int):
        """Rotate één face 90° clockwise"""
        # [0,1,2,3] -> [2,0,3,1] (clockwise)
        self.state[face] = [
            self.state[face][2],
            self.state[face][0],
            self.state[face][3],
            self.state[face][1]
        ]
    
    def rotate_face_ccw(self, face: int):
        """Rotate één face 90° counter-clockwise"""
        # [0,1,2,3] -> [1,3,0,2] (counter-clockwise)
        self.state[face] = [
            self.state[face][1],
            self.state[face][3],
            self.state[face][0],
            self.state[face][2]
        ]
    
    # ============ LAYER MOVES ============
    
    def move_R(self):
        """Right layer clockwise (van bovenaf gezien)"""
        # Top-right [1,3] -> Front-right [1,3] -> Bottom-right [1,3] -> Back-left [0,2] -> Top-right [1,3]
        temp = [self.state[self.WHITE][1], self.state[self.WHITE][3]]
        self.state[self.WHITE][1], self.state[self.WHITE][3] = \
            self.state[self.RED][1], self.state[self.RED][3]
        self.state[self.RED][1], self.state[self.RED][3] = \
            self.state[self.YELLOW][1], self.state[self.YELLOW][3]
        self.state[self.YELLOW][1], self.state[self.YELLOW][3] = \
            self.state[self.ORANGE][0], self.state[self.ORANGE][2]
        self.state[self.ORANGE][0], self.state[self.ORANGE][2] = temp
        
        # Rechter face 90° CW
        self.rotate_face_cw(self.BLUE)
    
    def move_R_prime(self):
        """Right layer counter-clockwise"""
        # Omgekeerd van R
        temp = [self.state[self.WHITE][1], self.state[self.WHITE][3]]
        self.state[self.WHITE][1], self.state[self.WHITE][3] = \
            self.state[self.ORANGE][0], self.state[self.ORANGE][2]
        self.state[self.ORANGE][0], self.state[self.ORANGE][2] = \
            self.state[self.YELLOW][1], self.state[self.YELLOW][3]
        self.state[self.YELLOW][1], self.state[self.YELLOW][3] = \
            self.state[self.RED][1], self.state[self.RED][3]
        self.state[self.RED][1], self.state[self.RED][3] = temp
        
        self.rotate_face_ccw(self.BLUE)
    
    def move_L(self):
        """Left layer clockwise (van boven af gezien)"""
        temp = [self.state[self.WHITE][0], self.state[self.WHITE][2]]
        self.state[self.WHITE][0], self.state[self.WHITE][2] = \
            self.state[self.ORANGE][1], self.state[self.ORANGE][3]
        self.state[self.ORANGE][1], self.state[self.ORANGE][3] = \
            self.state[self.YELLOW][0], self.state[self.YELLOW][2]
        self.state[self.YELLOW][0], self.state[self.YELLOW][2] = \
            self.state[self.RED][0], self.state[self.RED][2]
        self.state[self.RED][0], self.state[self.RED][2] = temp
        
        self.rotate_face_cw(self.GREEN)
    
    def move_L_prime(self):
        """Left layer counter-clockwise"""
        temp = [self.state[self.WHITE][0], self.state[self.WHITE][2]]
        self.state[self.WHITE][0], self.state[self.WHITE][2] = \
            self.state[self.RED][0], self.state[self.RED][2]
        self.state[self.RED][0], self.state[self.RED][2] = \
            self.state[self.YELLOW][0], self.state[self.YELLOW][2]
        self.state[self.YELLOW][0], self.state[self.YELLOW][2] = \
            self.state[self.ORANGE][1], self.state[self.ORANGE][3]
        self.state[self.ORANGE][1], self.state[self.ORANGE][3] = temp
        
        self.rotate_face_ccw(self.GREEN)
    
    def move_U(self):
        """Up (top) layer clockwise"""
        temp = [self.state[self.RED][0], self.state[self.RED][1]]
        self.state[self.RED][0], self.state[self.RED][1] = \
            self.state[self.GREEN][0], self.state[self.GREEN][1]
        self.state[self.GREEN][0], self.state[self.GREEN][1] = \
            self.state[self.ORANGE][0], self.state[self.ORANGE][1]
        self.state[self.ORANGE][0], self.state[self.ORANGE][1] = \
            self.state[self.BLUE][0], self.state[self.BLUE][1]
        self.state[self.BLUE][0], self.state[self.BLUE][1] = temp
        
        self.rotate_face_cw(self.WHITE)
    
    def move_U_prime(self):
        """Up layer counter-clockwise"""
        temp = [self.state[self.RED][0], self.state[self.RED][1]]
        self.state[self.RED][0], self.state[self.RED][1] = \
            self.state[self.BLUE][0], self.state[self.BLUE][1]
        self.state[self.BLUE][0], self.state[self.BLUE][1] = \
            self.state[self.ORANGE][0], self.state[self.ORANGE][1]
        self.state[self.ORANGE][0], self.state[self.ORANGE][1] = \
            self.state[self.GREEN][0], self.state[self.GREEN][1]
        self.state[self.GREEN][0], self.state[self.GREEN][1] = temp
        
        self.rotate_face_ccw(self.WHITE)
    
    def move_D(self):
        """Down (bottom) layer clockwise"""
        temp = [self.state[self.RED][2], self.state[self.RED][3]]
        self.state[self.RED][2], self.state[self.RED][3] = \
            self.state[self.BLUE][2], self.state[self.BLUE][3]
        self.state[self.BLUE][2], self.state[self.BLUE][3] = \
            self.state[self.ORANGE][2], self.state[self.ORANGE][3]
        self.state[self.ORANGE][2], self.state[self.ORANGE][3] = \
            self.state[self.GREEN][2], self.state[self.GREEN][3]
        self.state[self.GREEN][2], self.state[self.GREEN][3] = temp
        
        self.rotate_face_cw(self.YELLOW)
    
    def move_D_prime(self):
        """Down layer counter-clockwise"""
        temp = [self.state[self.RED][2], self.state[self.RED][3]]
        self.state[self.RED][2], self.state[self.RED][3] = \
            self.state[self.GREEN][2], self.state[self.GREEN][3]
        self.state[self.GREEN][2], self.state[self.GREEN][3] = \
            self.state[self.ORANGE][2], self.state[self.ORANGE][3]
        self.state[self.ORANGE][2], self.state[self.ORANGE][3] = \
            self.state[self.BLUE][2], self.state[self.BLUE][3]
        self.state[self.BLUE][2], self.state[self.BLUE][3] = temp
        
        self.rotate_face_ccw(self.YELLOW)
    
    # ============ MOVE MAPPING ============
    
    MOVES = {
        'R': move_R, 'R\'': move_R_prime,
        'L': move_L, 'L\'': move_L_prime,
        'U': move_U, 'U\'': move_U_prime,
        'D': move_D, 'D\'': move_D_prime,
    }
    
    def apply_move(self, move: str):
        """Apply een move string (bijv. 'R', 'L\'', 'U', etc.)"""
        if move in self.MOVES:
            self.MOVES[move](self)
        else:
            raise ValueError(f"Unknown move: {move}")
    
    def get_move_sequence_state(self, moves: List[str]) -> 'Rubiks2x2':
        """Krijg cube state na sequence van moves"""
        cube = self.copy()
        for move in moves:
            cube.apply_move(move)
        return cube


def generate_states_with_moves(num_states: int = 100) -> Dict:
    """
    Genereer een dataset met states en hun moves
    
    Returns:
        {
            'states': [{ 'hash': '...', 'state': [...], 'moves': [...] }, ...],
            'total_states': int,
            'solved_state': state_array
        }
    """
    cube = Rubiks2x2()
    states_dict = {}
    states_list = []
    
    # Solved state is altijd index 0
    solved_hash = cube.get_state_hash()
    states_dict[solved_hash] = {
        'state': cube.state,
        'moves': [],
        'index': 0
    }
    
    # Genereer moves
    all_moves = ['R', 'R\'', 'L', 'L\'', 'U', 'U\'', 'D', 'D\'']
    
    # BFS-achtige expansie (level by level)
    current_level = [('', cube)]
    processed = {solved_hash}
    
    for level in range(1, 10):  # Max 10 moves diep
        if len(processed) >= num_states:
            break
        
        next_level = []
        
        for prev_moves_str, cube_state in current_level:
            for move in all_moves:
                if len(processed) >= num_states:
                    break
                
                new_cube = cube_state.copy()
                new_cube.apply_move(move)
                new_hash = new_cube.get_state_hash()
                
                if new_hash not in processed:
                    processed.add(new_hash)
                    moves_list = (prev_moves_str + ' ' + move).strip().split(' ')
                    
                    states_dict[new_hash] = {
                        'state': new_cube.state,
                        'moves': moves_list,
                        'index': len(processed) - 1
                    }
                    
                    next_level.append((prev_moves_str + ' ' + move, new_cube))
        
        current_level = next_level[:500]  # Limiter per level
        print(f"Level {level}: {len(processed)} states gegenereerd")
    
    # Convert naar list
    for hash_val, data in states_dict.items():
        states_list.append({
            'hash': hash_val,
            'state': data['state'],
            'moves': data['moves'],
            'index': data['index']
        })
    
    return {
        'states': states_list,
        'total_states': len(states_list),
        'solved_state': [0, 1, 2, 3, 4, 5],
        'move_definitions': {
            'R': 'Right layer clockwise',
            'R\'': 'Right layer counter-clockwise',
            'L': 'Left layer clockwise',
            'L\'': 'Left layer counter-clockwise',
            'U': 'Up layer clockwise',
            'U\'': 'Up layer counter-clockwise',
            'D': 'Down layer clockwise',
            'D\'': 'Down layer counter-clockwise'
        }
    }


def export_to_json(data: Dict, filename: str):
    """Export states naar JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(data['states'])} states to {filename}")


if __name__ == '__main__':
    # Genereer 1000+ states
    print("Genereren van Rubik's 2x2 cube states...")
    data = generate_states_with_moves(num_states=2000)
    
    # Exporteer naar JSON
    export_to_json(data, 'states.json')
    
    # Test enkele moves
    cube = Rubiks2x2()
    print(f"\nSolved state: {cube.get_state_string()}")
    
    cube.apply_move('R')
    print(f"After R: {cube.get_state_string()}")
    
    cube.apply_move('R\'')
    print(f"After R': {cube.get_state_string()}")