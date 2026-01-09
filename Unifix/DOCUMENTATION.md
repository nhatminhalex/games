# Unifix Programming Language Documentation

## Overview

Unifix is a simple yet powerful programming language designed for education and game development. It features a clean, Python-like syntax with curly brace blocks, making it easy to learn while supporting advanced features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Syntax](#basic-syntax)
3. [Variables and Data Types](#variables-and-data-types)
4. [Operators](#operators)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Arrays/Lists](#arrayslists)
8. [Built-in Functions](#built-in-functions)
9. [Graphics and Games](#graphics-and-games)
10. [Input Handling](#input-handling)
11. [Examples](#examples)

---

## Getting Started

### Running Unifix Programs

```bash
python unifix.py your_program.unfx
#or
unifix your_program.unfx
```

### Hello World

```
print "Hello, World!"
```

---

## Basic Syntax

### Comments

Comments start with `#` and continue to the end of the line:

```
# This is a comment
print "Hello"  # Inline comment
```

### Statements

Statements are separated by newlines. Curly braces `{ }` define blocks:

```
print "First"
print "Second"

if x > 0 {
    print "Positive"
}
```

---

## Variables and Data Types

### Variable Declaration

```
set name = value
```

### Supported Data Types

| Type | Example |
|------|---------|
| Integer | `42` |
| Float | `3.14` |
| String | `"Hello"` |
| Boolean | `true`, `false` |
| Array | `[1, 2, 3]` |

### Examples

```
set age = 25
set price = 19.99
set name = "Alice"
set is_active = true
set items = ["apple", "banana", "cherry"]
```

---

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` |
| `-` | Subtraction | `5 - 3` |
| `*` | Multiplication | `5 * 3` |
| `/` | Division | `6 / 2` |
| `%` | Modulo | `10 % 3` |
| `^` | Power | `2 ^ 3` (8) |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal | `x == y` |
| `!=` | Not equal | `x != y` |
| `>` | Greater than | `x > y` |
| `<` | Less than | `x < y` |
| `>=` | Greater than or equal | `x >= y` |
| `<=` | Less than or equal | `x <= y` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Logical AND | `x > 0 and x < 10` |
| `or` | Logical OR | `x < 0 or x > 10` |
| `not` | Logical NOT | `not x == 0` |

---

## Control Flow

### If-Else Statements

```
if condition {
    # code
} else if another_condition {
    # code
} else {
    # code
}
```

Example:

```
set score = 85

if score >= 90 {
    print "Grade: A"
} else if score >= 80 {
    print "Grade: B"
} else {
    print "Grade: C or below"
}
```

### While Loops

```
while condition {
    # code
}
```

Example:

```
set counter = 1
while counter <= 5 {
    print "Count: " + counter
    set counter = counter + 1
}
```

### Repeat Loops

```
repeat n {
    # code
}
```

Example:

```
repeat 3 {
    print "Hello!"
}
```

---

## Functions

### Function Definition

```
def function_name(param1, param2, ...) {
    # code
    return value
}
```

### Examples

Basic function:

```
def greet() {
    print "Hello!"
}
greet()  # Call: prints "Hello!"
```

Function with parameters:

```
def add(a, b) {
    return a + b
}
set sum = add(5, 3)  # sum = 8
```

Function with conditionals:

```
def absolute_value(n) {
    if n >= 0 {
        return n
    } else {
        return 0 - n
    }
}
```

Recursive function:

```
def factorial(n) {
    if n <= 1 {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}
```

---

## Arrays/Lists

### Array Creation

```
set fruits = ["apple", "banana", "cherry"]
set numbers = [1, 2, 3, 4, 5]
set mixed = [1, "hello", true, 3.14]
```

### Array Indexing

Arrays are 0-indexed:

```
set fruits = ["apple", "banana", "cherry"]
print fruits[0]  # "apple"
print fruits[1]  # "banana"
```

### Array Length

```
set len = len(array)
```

### Loop Through Array

```
set fruits = ["apple", "banana", "cherry"]
set i = 0
while i < len(fruits) {
    print fruits[i]
    set i = i + 1
}
```

---

## Built-in Functions

### Math Functions

| Function | Description | Example |
|----------|-------------|---------|
| `random()` | Random float 0-1 | `random()` |
| `random(n)` | Random int 0-n | `random(100)` |
| `random(a, b)` | Random int a-b | `random(1, 6)` |
| `abs(n)` | Absolute value | `abs(-5)` |
| `round(n)` | Round to int | `round(3.7)` |
| `floor(n)` | Floor to int | `floor(3.7)` |
| `ceil(n)` | Ceiling to int | `ceil(3.2)` |
| `sqrt(n)` | Square root | `sqrt(16)` |
| `sin(deg)` | Sine (degrees) | `sin(30)` |
| `cos(deg)` | Cosine (degrees) | `cos(45)` |
| `tan(deg)` | Tangent (degrees) | `tan(45)` |
| `len(obj)` | Length of array/string | `len(arr)` |

### String Methods

| Method | Description | Example |
|--------|-------------|---------|
| `upper(s)` | Uppercase string | `upper("hello")` → `"HELLO"` |
| `lower(s)` | Lowercase string | `lower("HELLO")` → `"hello"` |
| `length(s)` | String length | `length("hi")` → `2` |
| `substring(s, start, end)` | Extract substring | `substring("hello", 0, 2)` → `"he"` |

---

## Graphics and Games

### Setup

```
import unifixgame
unifixgame.window [width, height]
```

### Colors

Available colors: `red`, `green`, `blue`, `white`, `black`, `yellow`, `orange`, `purple`, `gray`

Or RGB values: `unifixgame.color [255, 0, 0]`

### Drawing Shapes

```
# Set position
unifixgame.setPosition [x, y]

# Draw shapes
unifixgame.circle radius
unifixgame.rectangle size
unifixgame.triangle size
unifixgame.line [end_x, end_y]
unifixgame.text "message"
```

### Update Display

```
unifixgame.update
```

### Background

```
unifixgame.background "black"
unifixgame.background [0, 0, 0]  # RGB
unifixgame.clear
```

### Physics

```
unifixgame.enablePhysics
unifixgame.floor y_position
```

### Sprites

```
unifixgame.loadSprite "image.png"
unifixgame.drawSprite "image.png"
```

### Sound

```
unifixgame.playSound "sound.wav"
```

### Animation Loop

```
repeat 100 {
    # Update game state
    unifixgame.update
}
```

---

## Input Handling

### Keyboard

```
# Check specific keys
unifixgame.getKey "space"
unifixgame.getKey "up"
unifixgame.getKey "down"
unifixgame.getKey "left"
unifixgame.getKey "right"

if __key__ {
    # Key is pressed
}
```

### Mouse

```
# Get mouse position
unifixgame.getMouseX
unifixgame.getMouseY
print "Mouse at: " + __mouse_x__ + ", " + __mouse_y__

# Check if pressed
unifixgame.mousePressed
if __mouse_pressed__ {
    # Mouse is pressed
}
```

### Console Input

```
ask "Enter your name: "
print "Hello, " + last_input
```

---

## Examples

### Complete Game Example

```
import unifixgame

unifixgame.window [600, 400]
unifixgame.background "black"

set x = 300
set y = 200

repeat 300 {
    unifixgame.getKey "left"
    if __key__ { set x = x - 3 }
    
    unifixgame.getKey "right"
    if __key__ { set x = x + 3 }
    
    unifixgame.getKey "up"
    if __key__ { set y = y - 3 }
    
    unifixgame.getKey "down"
    if __key__ { set y = y + 3 }
    
    unifixgame.clear
    unifixgame.color "red"
    unifixgame.setPosition [x, y]
    unifixgame.rectangle 30
    unifixgame.update
}
```

### Function with Array

```
def sum_array(arr) {
    set total = 0
    set i = 0
    while i < len(arr) {
        set total = total + arr[i]
        set i = i + 1
    }
    return total
}

set numbers = [1, 2, 3, 4, 5]
print "Sum: " + sum_array(numbers)
```

---

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| `Undefined variable` | Check variable name is declared with `set` |
| `Illegal character` | Check for typos or unsupported characters |
| `Index out of range` | Ensure array index is within bounds |
| `Mismatched braces` | Check all `{` have corresponding `}` |

---

## File Structure

```
unifix/
├── main.py              # Interpreter
├── test.unfx            # Test program
├── gametest.unfx        # Graphics test
├── DOCUMENTATION.md     # This file
├── TODO.md              # Development notes
└── examples/
    ├── functions.unfx
    ├── arrays.unfx
    ├── while_loops.unfx
    ├── operators.unfx
    ├── math.unfx
    ├── string_methods.unfx
    ├── graphics.unfx
    ├── input.unfx
    └── complete_demo.unfx
```

---

## Language Features Summary

✅ **Completed Features:**
- Variables and data types
- Arithmetic, comparison, and logical operators
- If-else conditionals
- While loops
- Repeat loops
- User-defined functions
- Arrays/lists with indexing
- String operations
- Built-in math functions
- Graphics (shapes, colors, text)
- Sprite support
- Sound playback
- Keyboard and mouse input
- Physics engine integration
- Proper variable scoping

---

## Version History

- **v2.0** - Complete overhaul with all new features
- **v1.0** - Initial release with basic functionality

---

Happy Coding with Unifix! 🚀
