import tkinter as tk
from tkinter import font as tkfont
from math import sqrt, factorial, log10, log, sin, cos, tan, radians, pi, e

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Custom colors
        bg_color = "#f0f0f0"
        btn_color = "#e0e0e0"
        op_color = "#ff9800"
        sci_color = "#9e9e9e"
        self.root.configure(bg=bg_color)
        
        # Create display frame
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        # Custom fonts
        display_font = tkfont.Font(size=28)
        btn_font = tkfont.Font(size=14)
        sci_font = tkfont.Font(size=12)
        
        # Display
        self.display = tk.Entry(
            root, textvariable=self.display_var, 
            font=display_font, justify="right", 
            bd=10, insertwidth=2, width=18, 
            borderwidth=4, readonlybackground="#ffffff",
            relief="flat", highlightthickness=1,
            highlightcolor="#bdbdbd", highlightbackground="#bdbdbd"
        )
        self.display.config(state="readonly")
        self.display.grid(row=0, column=0, columnspan=6, pady=(10, 5), padx=10)
        
        # Memory display
        self.memory_var = tk.StringVar()
        self.memory_var.set("")
        self.memory_display = tk.Label(
            root, textvariable=self.memory_var,
            font=sci_font, bg=bg_color, anchor="e"
        )
        self.memory_display.grid(row=1, column=0, columnspan=6, sticky="e", padx=20)
        
        # Button layout - Scientific functions first row
        buttons = [
            # Row 2: Scientific functions
            ('sin', 2, 0, sci_font, sci_color), ('cos', 2, 1, sci_font, sci_color), 
            ('tan', 2, 2, sci_font, sci_color), ('π', 2, 3, sci_font, sci_color),
            ('e', 2, 4, sci_font, sci_color), ('n!', 2, 5, sci_font, sci_color),
            
            # Row 3: More scientific functions
            ('log₁₀', 3, 0, sci_font, sci_color), ('ln', 3, 1, sci_font, sci_color),
            ('x²', 3, 2, sci_font, sci_color), ('x³', 3, 3, sci_font, sci_color),
            ('x^y', 3, 4, sci_font, sci_color), ('√', 3, 5, sci_font, sci_color),
            
            # Row 4: Memory functions
            ('MC', 4, 0, sci_font, sci_color), ('MR', 4, 1, sci_font, sci_color),
            ('M+', 4, 2, sci_font, sci_color), ('M-', 4, 3, sci_font, sci_color),
            ('MS', 4, 4, sci_font, sci_color), ('⌫', 4, 5, btn_font, "#f44336"),
            
            # Row 5: Standard calculator
            ('(', 5, 0, btn_font, btn_color), (')', 5, 1, btn_font, btn_color),
            ('%', 5, 2, btn_font, btn_color), ('C', 5, 3, btn_font, "#f44336"),
            ('±', 5, 4, btn_font, btn_color), ('/', 5, 5, btn_font, op_color),
            
            # Row 6: Numbers
            ('7', 6, 0, btn_font, btn_color), ('8', 6, 1, btn_font, btn_color),
            ('9', 6, 2, btn_font, btn_color), ('*', 6, 3, btn_font, op_color),
            ('1/x', 6, 4, btn_font, btn_color), ('-', 6, 5, btn_font, op_color),
            
            # Row 7: Numbers
            ('4', 7, 0, btn_font, btn_color), ('5', 7, 1, btn_font, btn_color),
            ('6', 7, 2, btn_font, btn_color), ('+', 7, 3, btn_font, op_color),
            ('EE', 7, 4, btn_font, btn_color), ('=', 7, 5, btn_font, op_color),
            
            # Row 8: Numbers and decimal
            ('1', 8, 0, btn_font, btn_color), ('2', 8, 1, btn_font, btn_color),
            ('3', 8, 2, btn_font, btn_color), ('.', 8, 3, btn_font, btn_color),
            ('0', 8, 4, btn_font, btn_color), ('=', 8, 5, btn_font, op_color),
        ]
        
        # Create buttons
        for (text, row, col, font, bg) in buttons:
            btn = tk.Button(
                root, text=text, 
                command=lambda t=text: self.on_button_click(t),
                height=1, width=3 if len(text) <= 2 else 4, 
                font=font, bg=bg, activebackground="#bdbdbd",
                relief="flat", borderwidth=1
            )
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        
        # Configure row/column weights
        for i in range(9):
            root.grid_rowconfigure(i, weight=1)
        for i in range(6):
            root.grid_columnconfigure(i, weight=1)
        
        # Initialize calculator state
        self.current_input = "0"
        self.operation = None
        self.previous_value = None
        self.reset_next_input = False
        self.has_decimal = False
        self.memory = 0
        self.is_degree = True  # True for degree, False for radian
        self.last_operation = None
        
        # Bind keyboard events
        self.root.bind('<Key>', self.handle_key_press)
        
        # Add degree/radian toggle
        self.angle_mode = tk.StringVar(value="DEG")
        mode_btn = tk.Button(
            root, textvariable=self.angle_mode,
            command=self.toggle_angle_mode,
            font=sci_font, bg=sci_color, width=3,
            relief="flat"
        )
        mode_btn.grid(row=1, column=0, sticky="w", padx=5)
    
    def toggle_angle_mode(self):
        self.is_degree = not self.is_degree
        self.angle_mode.set("DEG" if self.is_degree else "RAD")
    
    def on_button_click(self, button_text):
        if button_text.isdigit():
            self.handle_digit(button_text)
        elif button_text == 'C':
            self.handle_clear()
        elif button_text in '+-*/^':
            self.handle_operation(button_text)
        elif button_text == '=':
            self.handle_equals()
        elif button_text == '.':
            self.handle_decimal()
        elif button_text == '√':
            self.handle_square_root()
        elif button_text == '%':
            self.handle_percent()
        elif button_text == '⌫':
            self.handle_backspace()
        elif button_text == '±':
            self.handle_negate()
        elif button_text == 'π':
            self.handle_pi()
        elif button_text == 'e':
            self.handle_e()
        elif button_text == 'n!':
            self.handle_factorial()
        elif button_text in ('sin', 'cos', 'tan'):
            self.handle_trig_function(button_text)
        elif button_text in ('log₁₀', 'ln'):
            self.handle_log_function(button_text)
        elif button_text in ('x²', 'x³'):
            self.handle_power_function(button_text)
        elif button_text == 'x^y':
            self.handle_power_operation()
        elif button_text == '1/x':
            self.handle_reciprocal()
        elif button_text == 'EE':
            self.handle_scientific_notation()
        elif button_text in ('(', ')'):
            self.handle_parentheses(button_text)
        elif button_text.startswith('M'):
            self.handle_memory_operation(button_text)
        
        self.update_display()
    
    def handle_key_press(self, event):
        key = event.char
        keys_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/', '.': '.',
            '\r': '=', '\x08': '⌫', '\x1b': 'C',
            'q': '√', 'p': '%', 's': 'sin', 'c': 'cos',
            't': 'tan', 'l': 'log₁₀', 'n': 'ln', '!': 'n!',
            '^': 'x^y', 'r': '1/x', 'm': '±', 'e': 'EE',
            '(': '(', ')': ')'
        }
        
        if key in keys_mapping:
            self.on_button_click(keys_mapping[key])
        elif event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif event.keysym == 'Return':
            self.on_button_click('=')
    
    def handle_digit(self, digit):
        if self.reset_next_input:
            self.current_input = "0"
            self.reset_next_input = False
            self.has_decimal = False
            
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
    
    def handle_clear(self):
        self.current_input = "0"
        self.operation = None
        self.previous_value = None
        self.reset_next_input = False
        self.has_decimal = False
        self.last_operation = None
    
    def handle_operation(self, op):
        if self.operation and not self.reset_next_input:
            self.calculate_result()
        
        self.previous_value = float(self.current_input)
        self.operation = op
        self.reset_next_input = True
        self.has_decimal = False
        self.last_operation = None
    
    def handle_equals(self):
        if self.operation and not self.reset_next_input:
            self.calculate_result()
            self.operation = None
            self.reset_next_input = True
        elif self.last_operation:  # Repeat last operation
            self.calculate_result(repeat=True)
    
    def handle_decimal(self):
        if self.reset_next_input:
            self.current_input = "0"
            self.reset_next_input = False
            self.has_decimal = False
            
        if not self.has_decimal:
            self.current_input += "."
            self.has_decimal = True
    
    def handle_square_root(self):
        try:
            value = float(self.current_input)
            if value >= 0:
                result = sqrt(value)
                self.current_input = self.format_result(result)
                self.last_operation = ('√', value)
                self.reset_next_input = True
            else:
                self.current_input = "Error"
                self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_percent(self):
        try:
            value = float(self.current_input)
            result = value / 100
            self.current_input = self.format_result(result)
            self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_backspace(self):
        if len(self.current_input) == 1 or (self.current_input[0] == '-' and len(self.current_input) == 2):
            self.current_input = "0"
            self.has_decimal = False
        else:
            if self.current_input[-1] == '.':
                self.has_decimal = False
            self.current_input = self.current_input[:-1]
    
    def handle_negate(self):
        if self.current_input[0] == '-':
            self.current_input = self.current_input[1:]
        else:
            self.current_input = '-' + self.current_input
    
    def handle_pi(self):
        self.current_input = str(pi)
        self.reset_next_input = True
    
    def handle_e(self):
        self.current_input = str(e)
        self.reset_next_input = True
    
    def handle_factorial(self):
        try:
            value = int(float(self.current_input))
            if value >= 0:
                result = factorial(value)
                self.current_input = self.format_result(result)
                self.last_operation = ('n!', value)
                self.reset_next_input = True
            else:
                self.current_input = "Error"
                self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_trig_function(self, func):
        try:
            value = float(self.current_input)
            angle = radians(value) if self.is_degree else value
            
            if func == 'sin':
                result = sin(angle)
            elif func == 'cos':
                result = cos(angle)
            elif func == 'tan':
                result = tan(angle)
            
            self.current_input = self.format_result(result)
            self.last_operation = (func, value)
            self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_log_function(self, func):
        try:
            value = float(self.current_input)
            if value > 0:
                if func == 'log₁₀':
                    result = log10(value)
                else:  # 'ln'
                    result = log(value)
                
                self.current_input = self.format_result(result)
                self.last_operation = (func, value)
                self.reset_next_input = True
            else:
                self.current_input = "Error"
                self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_power_function(self, func):
        try:
            value = float(self.current_input)
            if func == 'x²':
                result = value ** 2
            else:  # 'x³'
                result = value ** 3
            
            self.current_input = self.format_result(result)
            self.last_operation = (func, value)
            self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_power_operation(self):
        self.handle_operation('^')
    
    def handle_reciprocal(self):
        try:
            value = float(self.current_input)
            if value != 0:
                result = 1 / value
                self.current_input = self.format_result(result)
                self.last_operation = ('1/x', value)
                self.reset_next_input = True
            else:
                self.current_input = "Error"
                self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_scientific_notation(self):
        try:
            value = float(self.current_input)
            self.current_input = "{:.4e}".format(value)
            self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def handle_parentheses(self, paren):
        # Basic implementation - could be enhanced for full expression evaluation
        self.current_input += paren
    
    def handle_memory_operation(self, op):
        try:
            current_value = float(self.current_input)
            
            if op == 'MC':  # Memory Clear
                self.memory = 0
            elif op == 'MR':  # Memory Recall
                self.current_input = self.format_result(self.memory)
                self.reset_next_input = True
            elif op == 'M+':  # Memory Add
                self.memory += current_value
            elif op == 'M-':  # Memory Subtract
                self.memory -= current_value
            elif op == 'MS':  # Memory Store
                self.memory = current_value
            
            self.memory_var.set(f"M: {self.memory}" if self.memory != 0 else "")
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def calculate_result(self, repeat=False):
        try:
            current_value = float(self.current_input)
            
            if repeat and self.last_operation:
                # Repeat last operation with current value
                op, prev_val = self.last_operation
                if op in ('+', '-', '*', '/', '^'):
                    current_value = prev_val
                elif op == '√':
                    result = sqrt(current_value)
                elif op == 'n!':
                    result = factorial(int(current_value))
                elif op in ('sin', 'cos', 'tan'):
                    angle = radians(current_value) if self.is_degree else current_value
                    if op == 'sin':
                        result = sin(angle)
                    elif op == 'cos':
                        result = cos(angle)
                    elif op == 'tan':
                        result = tan(angle)
                elif op == '1/x':
                    result = 1 / current_value
                else:
                    result = current_value
            else:
                # Normal operation
                if self.operation == '+':
                    result = self.previous_value + current_value
                elif self.operation == '-':
                    result = self.previous_value - current_value
                elif self.operation == '*':
                    result = self.previous_value * current_value
                elif self.operation == '/':
                    result = self.previous_value / current_value
                elif self.operation == '^':
                    result = self.previous_value ** current_value
            
            # Format result
            self.current_input = self.format_result(result)
            self.previous_value = result
            self.has_decimal = '.' in self.current_input
            
            if not repeat:
                self.last_operation = (self.operation, current_value)
        except ZeroDivisionError:
            self.current_input = "Error: Div by 0"
            self.reset_next_input = True
        except OverflowError:
            self.current_input = "Error: Too large"
            self.reset_next_input = True
        except:
            self.current_input = "Error"
            self.reset_next_input = True
    
    def format_result(self, value):
        # Format the result for display
        if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
            return str(int(value))
        else:
            # Show up to 10 digits, remove trailing zeros
            formatted = "{:.10f}".format(value).rstrip('0').rstrip('.')
            return formatted if formatted else "0"
    
    def update_display(self):
        self.display_var.set(self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()