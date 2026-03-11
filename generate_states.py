#!/usr/bin/env python3
"""
Generate all reachable 2x2 cube states using correct move functions
"""

import json
from collections import deque

class RubiksCubeGenerator:
    """Generate all states reachable from solved cube"""
    
    def __init__(self):
        self.states = []
        self.state_set = set()
    
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
        temp = [state[0][1], state[0][3]]
        state[0][1], state[0][3] = state[3][2], state[3][0]
        state[3][2], state[3][0] = state[1][1], state[1][3]
        state[1][1], state[1][3] = state[2][1], state[2][3]
        state[2][1], state[2][3] = temp[0], temp[1]
        state[4] = [state[4][2], state[4][0], state[4][3], state[4][1]]
    
    def moveU(self, state):
        """Up turn clockwise (looking from top)"""
        temp = [state[2][0], state[2][1]]
        state[2][0], state[2][1] = state[5][0], state[5][1]
        state[5][0], state[5][1] = state[3][1], state[3][0]
        state[3][1], state[3][0] = state[4][0], state[4][1]
        state[4][0], state[4][1] = temp[0], temp[1]
        state[0] = [state[0][2], state[0][0], state[0][3], state[0][1]]
    
    def moveB(self, state):
        """Bottom turn clockwise (looking from bottom)"""
        temp = [state[2][2], state[2][3]]
        state[2][2], state[2][3] = state[5][2], state[5][3]
        state[5][2], state[5][3] = state[3][3], state[3][2]
        state[3][3], state[3][2] = state[4][2], state[4][3]
        state[4][2], state[4][3] = temp[0], temp[1]
        state[1] = [state[1][2], state[1][0], state[1][3], state[1][1]]
    

    def state_to_tuple(self, state):
        """Convert state to tuple for hashing"""
        return tuple(tuple(face) for face in state)
    
    def generate_all_states(self, max_depth=7):
        """Generate all states reachable in max_depth moves using BFS"""
        
        # Solved cube
        solved = [
            [0, 0, 0, 0],  # top
            [1, 1, 1, 1],  # bottom
            [2, 2, 2, 2],  # front
            [3, 3, 3, 3],  # back
            [4, 4, 4, 4],  # right
            [5, 5, 5, 5]   # left
        ]
        
        queue = deque([(solved, 0)])  # (state, depth)
        visited = set()
        visited.add(self.state_to_tuple(solved))
        
        self.states.append(solved)
        
        moves = ['L', 'R', 'U', 'B']
        count = 1
        
        print(f"Generating states up to {max_depth} moves deep...")
        
        while queue:
            current_state, depth = queue.popleft()
            
            if depth < max_depth:
                for move in moves:
                    next_state = self.apply_move(current_state, move)
                    state_tuple = self.state_to_tuple(next_state)
                    
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        self.states.append(next_state)
                        queue.append((next_state, depth + 1))
                        count += 1
                        
                        if count % 100 == 0:
                            print(f"  {count} states generated...")
        
        print(f"Total states generated: {count}")
        return self.states
    
    def save_to_json(self, filename='rubiks_states.json'):
        """Save all states to JSON"""
        data = {
            'total': len(self.states),
            'states': [{'state': state} for state in self.states]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        print(f"Saved {len(self.states)} states to {filename}")


def main():
    print("Generating 2x2 Rubik's Cube states...")
    
    generator = RubiksCubeGenerator()
    states = generator.generate_all_states(max_depth=7)
    generator.save_to_json('rubiks_states.json')
    
    print("Done! Now run: python3 generate_2x2.py")


if __name__ == '__main__':
    main()
