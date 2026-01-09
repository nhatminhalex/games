import re
import sys
import pygame
import pymunk
import random
import math

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.rules = [
            ('COMMENT', r'#.*'),
            ('DEF', r'def'),
            ('IMPORT', r'import'),
            ('IF', r'if'),
            ('ELSE', r'else'),
            ('REPEAT', r'repeat'),
            ('WHILE', r'while'),
            ('SET', r'set'),
            ('PRINT', r'print'),
            ('ASK', r'ask'),
            ('RETURN', r'return'),
            ('TRUE', r'true'),
            ('FALSE', r'false'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COMMA', r','),
            ('GTE', r'>='),
            ('LTE', r'<='),
            ('NEQ', r'!='),
            ('EQ', r'=='),
            ('GT', r'>'),
            ('LT', r'<'),
            ('PLUS', r'\+'),
            ('MINUS', r'\-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'\/'),
            ('MODULO', r'%'),
            ('POWER', r'\^'),
            ('DOT', r'\.'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('EQUALS', r'='),
            ('STRING', r'"[^"]*"'),
            ('NUMBER', r'\d+\.?\d*'),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'\s+'),
        ]

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = None
            for token_type, pattern in self.rules:
                regex = re.compile(pattern)
                match = regex.match(self.code, pos)
                if match:
                    if token_type not in ['WHITESPACE', 'NEWLINE', 'COMMENT']:
                        value = match.group(0)
                        if token_type == 'STRING': value = value[1:-1]
                        elif token_type in ['TRUE', 'FALSE']: value = (token_type == 'TRUE')
                        elif token_type == 'NUMBER': value = float(value) if '.' in value else int(value)
                        self.tokens.append((token_type, value))
                    pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Illegal character '{self.code[pos]}' at position {pos}")
        return self.tokens

class UnifixInterpreter:
    def __init__(self, tokens, variables=None, functions=None, parent_scope=None):
        self.tokens = tokens
        self.variables = variables.copy() if variables is not None else {}
        self.functions = functions.copy() if functions is not None else {}
        self.parent_scope = parent_scope  # For scoping
        self.pos = 0
        self.return_value = None
        self.break_loop = False
        
        # Pygame & Physics State
        self.game_active = False
        self.physics_active = False
        self.screen = None
        self.clock = None
        self.space = None
        self.player_body = None
        self.player_shape = None
        self.floors = []
        self.bg_color = (255, 255, 255)
        self.sprites = {}
        self.sounds = {}
        self.key_states = {}
        self.mouse_state = {'x': 0, 'y': 0, 'pressed': False}

    def get_value(self):
        if self.pos >= len(self.tokens):
            return None
        token_type, value = self.tokens[self.pos]
        self.pos += 1
        
        if token_type == 'ID':
            # Check current scope, then parent scopes
            current = self
            while current:
                if value in current.variables:
                    return current.variables[value]
                current = current.parent_scope
            raise NameError(f"Undefined variable: {value}")
        elif token_type == 'TRUE':
            return True
        elif token_type == 'FALSE':
            return False
        return value

    def evaluate_expression(self):
        if self.pos >= len(self.tokens):
            return None
        
        result = self.get_value()
        
        # Handle parentheses for function calls
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'LBRACKET':
            # List/array access
            self.pos += 1
            index = self.evaluate_expression()
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'RBRACKET':
                self.pos += 1
                if isinstance(result, list):
                    result = result[int(index)] if 0 <= int(index) < len(result) else None
                elif isinstance(result, str):
                    result = result[int(index)] if 0 <= int(index) < len(result) else ''
        
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in [
            'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'POWER',
            'EQ', 'GT', 'LT', 'GTE', 'LTE', 'NEQ'
        ]:
            op = self.tokens[self.pos][0]
            self.pos += 1
            next_val = self.evaluate_expression()
            
            if op == 'PLUS': result = self._add(result, next_val)
            elif op == 'MINUS': result -= next_val
            elif op == 'MULTIPLY': result *= next_val
            elif op == 'DIVIDE': result /= next_val
            elif op == 'MODULO': result %= next_val
            elif op == 'POWER': result **= next_val
            elif op == 'EQ': result = (result == next_val)
            elif op == 'GT': result = (result > next_val)
            elif op == 'LT': result = (result < next_val)
            elif op == 'GTE': result = (result >= next_val)
            elif op == 'LTE': result = (result <= next_val)
            elif op == 'NEQ': result = (result != next_val)
        
        return result

    def _add(self, a, b):
        """Handle addition for both numbers and strings"""
        if isinstance(a, str) or isinstance(b, str):
            return str(a) + str(b)
        return a + b

    def evaluate_logical_expression(self):
        """Evaluate boolean expressions with and/or/not"""
        result = self.evaluate_expression()
        
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ['AND', 'OR']:
            op = self.tokens[self.pos][0]
            self.pos += 1
            next_val = self.evaluate_expression()
            
            if op == 'AND':
                result = (result and next_val)
            elif op == 'OR':
                result = (result or next_val)
        
        return result

    def capture_block(self):
        block = []
        brace_stack = 1
        self.pos += 1
        while brace_stack > 0 and self.pos < len(self.tokens):
            if self.tokens[self.pos][0] == 'LBRACE':
                brace_stack += 1
            elif self.tokens[self.pos][0] == 'RBRACE':
                brace_stack -= 1
            if brace_stack > 0:
                block.append(self.tokens[self.pos])
            self.pos += 1
        return block

    def run(self, subset_tokens=None):
        if subset_tokens is not None:
            self.tokens = subset_tokens
            self.pos = 0

        while self.pos < len(self.tokens) and not self.break_loop:
            if self.pos >= len(self.tokens):
                break
                
            token_type, value = self.tokens[self.pos]

            # Handle comments
            if token_type == 'COMMENT':
                self.pos += 1
                continue

            # Function definition
            if token_type == 'DEF':
                self.pos += 1
                if self.pos >= len(self.tokens):
                    break
                func_name = self.tokens[self.pos][1]
                self.pos += 1
                
                # Capture parameters
                params = []
                if self.tokens[self.pos][0] == 'LBRACKET':
                    self.pos += 1
                    while self.tokens[self.pos][0] != 'RBRACKET':
                        if self.tokens[self.pos][0] == 'ID':
                            params.append(self.tokens[self.pos][1])
                        self.pos += 1
                    self.pos += 1  # Skip RBRACKET
                
                # Capture function body
                func_body = self.capture_block()
                self.functions[func_name] = {
                    'params': params,
                    'body': func_body,
                    'captured_vars': self.variables.copy()
                }
                continue

            # Import statements
            if token_type == 'IMPORT':
                self.pos += 1
                if self.pos < len(self.tokens) and self.tokens[self.pos][1] == "unifixgame":
                    self.game_active = True
                    pygame.init()
                    self.pos += 1
                continue

            # Variable assignment
            if token_type == 'SET':
                self.pos += 1
                if self.pos >= len(self.tokens):
                    break
                var_name = self.tokens[self.pos][1]
                self.pos += 1
                value = self.evaluate_expression()
                self.variables[var_name] = value
                continue

            # Print statement
            if token_type == 'PRINT':
                self.pos += 1
                print_value = self.evaluate_expression()
                print(print_value)
                continue

            # Ask for input
            if token_type == 'ASK':
                self.pos += 1
                if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'STRING':
                    prompt = self.tokens[self.pos][1]
                    self.pos += 1
                else:
                    prompt = ""
                user_input = input(prompt)
                # Store in last_input variable
                self.variables['last_input'] = user_input
                continue

            # If statement
            if token_type == 'IF':
                self.pos += 1
                condition = self.evaluate_logical_expression()
                block = self.capture_block()
                if condition:
                    new_interp = UnifixInterpreter(
                        block, self.variables, self.functions, self
                    )
                    new_interp._copy_game_state()
                    new_interp.run()
                    # Copy back variables
                    self.variables.update(new_interp.variables)
                else:
                    # Check for else
                    if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ELSE':
                        self.pos += 1
                        else_block = self.capture_block()
                        new_interp = UnifixInterpreter(
                            else_block, self.variables, self.functions, self
                        )
                        new_interp._copy_game_state()
                        new_interp.run()
                        self.variables.update(new_interp.variables)
                continue

            # While loop
            if token_type == 'WHILE':
                self.pos += 1
                condition = self.evaluate_logical_expression()
                block = self.capture_block()
                
                while condition and not self.break_loop:
                    new_interp = UnifixInterpreter(
                        block, self.variables, self.functions, self
                    )
                    new_interp._copy_game_state()
                    new_interp.run()
                    self.variables.update(new_interp.variables)
                    condition = self.evaluate_logical_expression()
                continue

            # Repeat loop
            if token_type == 'REPEAT':
                self.pos += 1
                times = int(self.evaluate_expression())
                block = self.capture_block()
                for _ in range(times):
                    if self.break_loop:
                        break
                    new_interp = UnifixInterpreter(
                        block, self.variables, self.functions, self
                    )
                    new_interp._copy_game_state()
                    new_interp.run()
                    self.variables.update(new_interp.variables)
                continue

            # Return statement
            if token_type == 'RETURN':
                self.pos += 1
                self.return_value = self.evaluate_expression()
                self.break_loop = True
                continue

            # Built-in functions
            if token_type == 'ID' and value in ['random', 'len', 'abs', 'round', 'floor', 'ceil', 'sqrt', 'sin', 'cos', 'tan']:
                func_name = value
                self.pos += 1
                args = []
                if self.tokens[self.pos][0] == 'LBRACKET':
                    self.pos += 1
                    while self.tokens[self.pos][0] != 'RBRACKET':
                        args.append(self.evaluate_expression())
                        if self.tokens[self.pos][0] == 'COMMA':
                            self.pos += 1
                    self.pos += 1
                
                result = self._call_builtin(func_name, args)
                self.variables['__result__'] = result
                continue

            # String methods
            if token_type == 'ID' and value in ['length', 'upper', 'lower', 'substring']:
                method_name = value
                self.pos += 1
                obj = self.get_value()  # Get the string variable
                args = []
                if self.tokens[self.pos][0] == 'LBRACKET':
                    self.pos += 1
                    while self.tokens[self.pos][0] != 'RBRACKET':
                        args.append(self.evaluate_expression())
                        if self.tokens[self.pos][0] == 'COMMA':
                            self.pos += 1
                    self.pos += 1
                
                result = self._call_string_method(method_name, obj, args)
                self.variables['__result__'] = result
                continue

            # List/Array creation
            if token_type == 'LBRACKET':
                items = []
                self.pos += 1
                while self.tokens[self.pos][0] != 'RBRACKET':
                    items.append(self.evaluate_expression())
                    if self.tokens[self.pos][0] == 'COMMA':
                        self.pos += 1
                self.pos += 1
                self.variables['__result__'] = items
                continue

            # unifixgame commands
            if token_type == 'ID' and value == 'unifixgame':
                self.pos += 1
                command = self.tokens[self.pos][1]
                self.pos += 1
                arg = self.evaluate_expression()
                
                self._handle_game_command(command, arg)
                continue

            # Function call
            if token_type == 'ID' and value in self.functions:
                func_name = value
                self.pos += 1
                
                # Parse arguments
                args = []
                if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'LBRACKET':
                    self.pos += 1
                    while self.tokens[self.pos][0] != 'RBRACKET':
                        args.append(self.evaluate_expression())
                        if self.tokens[self.pos][0] == 'COMMA':
                            self.pos += 1
                    self.pos += 1
                
                self._call_function(func_name, args)
                continue

            # Unknown token
            self.pos += 1

    def _copy_game_state(self):
        """Copy game state to child interpreter"""
        pass  # State is shared via references

    def _call_builtin(self, func_name, args):
        """Call built-in mathematical and utility functions"""
        if func_name == 'random':
            if len(args) == 0:
                return random.random()
            elif len(args) == 1:
                return random.randint(0, int(args[0]))
            else:
                return random.uniform(args[0], args[1])
        elif func_name == 'len':
            arg = args[0]
            if isinstance(arg, list):
                return len(arg)
            elif isinstance(arg, str):
                return len(arg)
            return 0
        elif func_name == 'abs':
            return abs(args[0])
        elif func_name == 'round':
            return round(args[0]) if args else 0
        elif func_name == 'floor':
            return math.floor(args[0]) if args else 0
        elif func_name == 'ceil':
            return math.ceil(args[0]) if args else 0
        elif func_name == 'sqrt':
            return math.sqrt(args[0]) if args else 0
        elif func_name == 'sin':
            return math.sin(math.radians(args[0])) if args else 0
        elif func_name == 'cos':
            return math.cos(math.radians(args[0])) if args else 0
        elif func_name == 'tan':
            return math.tan(math.radians(args[0])) if args else 0
        return None

    def _call_string_method(self, method_name, obj, args):
        """Call string methods"""
        if not isinstance(obj, str):
            obj = str(obj)
        
        if method_name == 'length':
            return len(obj)
        elif method_name == 'upper':
            return obj.upper()
        elif method_name == 'lower':
            return obj.lower()
        elif method_name == 'substring':
            if len(args) >= 2:
                start = int(args[0])
                end = int(args[1])
                return obj[start:end]
            elif len(args) == 1:
                return obj[int(args[0]):]
            return obj
        return None

    def _call_function(self, func_name, args):
        """Call user-defined function"""
        func = self.functions[func_name]
        
        # Create new scope
        new_scope = UnifixInterpreter(
            func['body'], 
            func['captured_vars'].copy(), 
            self.functions, 
            self
        )
        new_scope._copy_game_state()
        
        # Bind arguments to parameters
        for i, param in enumerate(func['params']):
            if i < len(args):
                new_scope.variables[param] = args[i]
        
        # Run function
        new_scope.run()
        
        # Store return value
        if new_scope.return_value is not None:
            self.variables['__result__'] = new_scope.return_value

    def _handle_game_command(self, command, arg):
        """Handle all unifixgame commands"""
        if not self.game_active:
            return

        if command == "window":
            if isinstance(arg, list) and len(arg) == 2:
                self.screen = pygame.display.set_mode((int(arg[0]), int(arg[1])))
            else:
                self.screen = pygame.display.set_mode((600, 600))
            pygame.display.set_caption("Unifix Game")
            self.clock = pygame.time.Clock()
        
        elif command == "color":
            color_map = {
                'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
                'white': (255, 255, 255), 'black': (0, 0, 0), 'yellow': (255, 255, 0),
                'orange': (255, 165, 0), 'purple': (128, 0, 128), 'gray': (128, 128, 128)
            }
            color = color_map.get(arg, (255, 0, 0))
            self.variables['__color__'] = color
        
        elif command == "circle":
            if self.screen and 'x' in self.variables and 'y' in self.variables:
                x = self.variables.get('x', 300)
                y = self.variables.get('y', 300)
                radius = int(arg) if arg else 20
                color = self.variables.get('__color__', (255, 0, 0))
                pygame.draw.circle(self.screen, color, (x, y), radius)
        
        elif command == "rectangle":
            if self.screen and 'x' in self.variables and 'y' in self.variables:
                x = self.variables.get('x', 300)
                y = self.variables.get('y', 300)
                width = int(arg) if arg else 40
                color = self.variables.get('__color__', (255, 0, 0))
                height = self.variables.get('height', width)
                pygame.draw.rect(self.screen, color, (x - width//2, y - height//2, width, height))
        
        elif command == "triangle":
            if self.screen and 'x' in self.variables and 'y' in self.variables:
                x = self.variables.get('x', 300)
                y = self.variables.get('y', 300)
                size = int(arg) if arg else 40
                color = self.variables.get('__color__', (255, 0, 0))
                points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
                pygame.draw.polygon(self.screen, color, points)
        
        elif command == "line":
            if self.screen:
                if isinstance(arg, list) and len(arg) >= 2:
                    x1, y1 = int(arg[0]), int(arg[1])
                    x2 = self.variables.get('x', x1 + 100)
                    y2 = self.variables.get('y', y1)
                    color = self.variables.get('__color__', (0, 0, 0))
                    pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 2)
        
        elif command == "text":
            if self.screen and 'x' in self.variables and 'y' in self.variables:
                x = self.variables.get('x', 300)
                y = self.variables.get('y', 300)
                text = str(arg) if arg else "Hello"
                color = self.variables.get('__color__', (0, 0, 0))
                font = pygame.font.Font(None, 32)
                surface = font.render(text, True, color)
                self.screen.blit(surface, (x, y))
        
        elif command == "move":
            if 'x' in self.variables and 'y' in self.variables:
                self.variables['x'] = self.variables.get('x', 300) + int(arg)
        
        elif command == "setPosition":
            if isinstance(arg, list) and len(arg) == 2:
                self.variables['x'] = int(arg[0])
                self.variables['y'] = int(arg[1])
        
        elif command == "turn":
            if 'angle' in self.variables:
                self.variables['angle'] = (self.variables.get('angle', 0) + int(arg)) % 360
            else:
                self.variables['angle'] = int(arg) % 360
        
        elif command == "enablePhysics":
            self.physics_active = True
            self.space = pymunk.Space()
            self.space.gravity = (0, 900)
            
            # Setup Player Body
            self.player_body = pymunk.Body(1, pymunk.moment_for_box(1, (40, 40)))
            self.player_body.position = (300, 100)
            self.player_shape = pymunk.Poly.create_box(self.player_body, (40, 40))
            self.player_shape.elasticity = 0.5
            self.space.add(self.player_body, self.player_shape)
        
        elif command == "floor":
            if self.space:
                y_coord = int(arg) if arg else 500
                floor = pymunk.Segment(self.space.static_body, (0, y_coord), (600, y_coord), 5)
                floor.elasticity = 0.5
                self.space.add(floor)
                self.floors.append(floor)
        
        elif command == "update":
            if self.screen:
                # Handle Pygame Events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self.key_states[event.unicode] = True
                        self.key_states['all_keys'] = self.key_states.get('all_keys', [])
                        self.key_states['all_keys'].append(event.key)
                    elif event.type == pygame.KEYUP:
                        self.key_states[event.unicode] = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_state['pressed'] = True
                        self.mouse_state['x'], self.mouse_state['y'] = pygame.mouse.get_pos()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_state['pressed'] = False
                
                # Handle continuous key states
                keys = pygame.key.get_pressed()
                self.key_states['space'] = keys[pygame.K_SPACE]
                self.key_states['up'] = keys[pygame.K_UP]
                self.key_states['down'] = keys[pygame.K_DOWN]
                self.key_states['left'] = keys[pygame.K_LEFT]
                self.key_states['right'] = keys[pygame.K_RIGHT]
                
                # Update mouse position
                self.mouse_state['x'], self.mouse_state['y'] = pygame.mouse.get_pos()
                
                # Step Physics
                if self.physics_active: 
                    self.space.step(1/60.0)
                
                # Draw
                self.screen.fill(self.bg_color)
                
                # Draw Floor
                for f in self.floors:
                    pygame.draw.line(self.screen, (0, 0, 0), f.a, f.b, 5)
                
                # Draw Player
                if self.player_body:
                    pos = self.player_body.position
                    pygame.draw.rect(self.screen, (255, 0, 0), (pos.x-20, pos.y-20, 40, 40))
                
                pygame.display.flip()
                if self.clock:
                    self.clock.tick(60)
        
        elif command == "loadSprite":
            if isinstance(arg, str):
                try:
                    sprite = pygame.image.load(arg)
                    self.sprites[arg] = pygame.transform.scale(sprite, (50, 50))
                except:
                    pass
        
        elif command == "drawSprite":
            if self.screen and isinstance(arg, str) and arg in self.sprites:
                x = self.variables.get('x', 300)
                y = self.variables.get('y', 300)
                self.screen.blit(self.sprites[arg], (x, y))
        
        elif command == "playSound":
            if isinstance(arg, str):
                try:
                    if arg not in self.sounds:
                        self.sounds[arg] = pygame.mixer.Sound(arg)
                    self.sounds[arg].play()
                except:
                    pass
        
        elif command == "background":
            if isinstance(arg, list) and len(arg) == 3:
                self.bg_color = (int(arg[0]), int(arg[1]), int(arg[2]))
            elif arg in ['red', 'green', 'blue', 'white', 'black', 'yellow']:
                color_map = {'red': (255,0,0), 'green': (0,255,0), 'blue': (0,0,255),
                           'white': (255,255,255), 'black': (0,0,0), 'yellow': (255,255,0)}
                self.bg_color = color_map.get(arg, (255,255,255))
        
        elif command == "clear":
            if self.screen:
                self.screen.fill(self.bg_color)
        
        elif command == "wait":
            if self.clock:
                self.clock.tick(int(arg)) if arg else self.clock.tick(60)
        
        elif command == "getKey":
            keys = pygame.key.get_pressed()
            if arg == "space": self.variables['__key__'] = keys[pygame.K_SPACE]
            elif arg == "up": self.variables['__key__'] = keys[pygame.K_UP]
            elif arg == "down": self.variables['__key__'] = keys[pygame.K_DOWN]
            elif arg == "left": self.variables['__key__'] = keys[pygame.K_LEFT]
            elif arg == "right": self.variables['__key__'] = keys[pygame.K_RIGHT]
            else: self.variables['__key__'] = False
        
        elif command == "getMouseX":
            self.variables['__mouse_x__'] = pygame.mouse.get_pos()[0]
        
        elif command == "getMouseY":
            self.variables['__mouse_y__'] = pygame.mouse.get_pos()[1]
        
        elif command == "mousePressed":
            self.variables['__mouse_pressed__'] = pygame.mouse.get_pressed()[0]

def run_file(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        interpreter = UnifixInterpreter(tokens)
        interpreter.run()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
