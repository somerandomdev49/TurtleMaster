import turtle as t
import tkinter as tk
import tkinter.simpledialog as tkmsgbox
import sys, re, os

VERSION_MAJ = 2000
VERSION_MIN = 200

class Stack:
    def __init__(self):
        self.__list = []
    def push(self, e):
        self.__list.append(e)
    def top(self):
        return self.__list[len(self.__list)-1]
    def pop(self):
        t = top()
        self.__list.pop()
        return t

# Main function.
def run(instructions_):
    data = {}
    instructions = []
    stack = Stack()

    def run_arg(arg):
        if arg[0:len("[string]")] == '[string]':
            return arg[1:] \
                .replace("\\n", "\n") \
                .replace("\\t", "\t") \
                .replace("\\r", "\r")
        arg = arg.strip()
        if arg[0] == '%':
            if not arg[1:] in data:
                print("No such data entry: " + argument + "!", file=sys.stderr)
                instr_idx += 1
            return data[arg[1:]]
        elif arg[0] == '$': return float(arg[1:])
        elif arg[0] == '=': return arg[1:]
        elif arg[0] == '@': return stack.top()
        else: raise KeyError("Unknown value type: " + arg[0])
    
    # If no file provided, ask user for the instructions
    if instructions_ is None:
        # Ask for instructions.
        root = tk.Tk()
        root.withdraw()
        path_str = tkmsgbox.askstring("[CODE-ONLY] Turtle Master " + str(VERSION_MAJ + VERSION_MIN), "Enter your code:")
        root.destroy()

        # Create all of the instructions.
        instructions_ = path_str.replace("\n", " ").replace("\t", " ").split(" ")
    else:
        instructions_ = instructions_.replace("\t", " ")
        code_lines = []
        mode = ""
        for line in instructions_.split("\n"):
            line = re.sub(' +', ' ', line)
            # print("uh,", "'" + line.strip() + "'")
            if line.strip() == "data:":
                mode = "data"
            elif line.strip() == "code:":
                mode = "code"
            else:
                if len(line.strip()) != 0 and line.strip()[0] == '#': continue
                if mode == "data" and len(line.strip()) != 0:
                    # print("DATA MODE LINE")
                    entry = line.split("=")
                    data[entry[0].strip()] = run_arg(entry[1])
                elif mode == "code":
                    # print("CODE MODE LINE")
                    code_lines.append(line)
        instructions = '\n'.join(code_lines).split("\n")

    labels = {}
    
    

    # print(instructions)

    # Create a turtle.
    pen = t.Pen()

    stack.push(False)

    if '__speed' in data: pen.speed(float(data['__speed']))

    ## LABEL SEARCH
    instr_idx = 0
    while instr_idx < len(instructions):
        i = instructions[instr_idx]

        if len(i.strip()) == 0:
            instr_idx += 1
            continue

        # Split the instruction with colons, the first is command, the second is the argument.
        code = i.split(":")
        command = code[0].strip()
        argument = code[1].strip()

        if command == 'label':
            labels[argument] = instr_idx
        instr_idx += 1

    ## RUNTIME
    instr_idx = 0
    while instr_idx < len(instructions):
        i = instructions[instr_idx]
        if len(i.strip()) == 0:
            instr_idx += 1
            continue

        # Split the instruction with colons, the first is command, the second is the argument.
        code = i.split(":")
        command = code[0].strip()
        argument = code[1].strip()

        # Why there are no switch statements in python?!
        if command == 'left':
            pen.left(run_arg(argument))
        elif command == 'right':
            pen.right(run_arg(argument))
        elif command == 'up':
            pen.up()
        elif command == 'down':
            pen.down()
        elif command == 'forward':
            pen.forward(run_arg(argument))
        elif command == 'backward':
            pen.backward(run_arg(argument))
        elif command == 'color':
            pen.color(argument)
        elif command == 'begin-fill':
            pen.begin_fill()
        elif command == 'end-fill':
            pen.end_fill()
        elif command == 'circle':
            pen.circle(run_arg(argument))
        elif command == 'goto':
            position = argument.split(';') # split the argument with semicolon, so we have x and y position.
            x = run_arg(position[0])
            y = run_arg(position[1])
            pen.goto(x, y)
        elif command == 'movex':
            pen.goto(pen.xcor() + run_arg(argument), pen.ycor()) # change x by the argument.
        elif command == 'movey':
            pen.goto(pen.xcor(), pen.ycor() + run_arg(argument)) # change x by the argument.
        elif command == 'heading': pen.seth(run_arg(argument))
        elif command == 'set-font-size': data['__font_size'] = int(run_arg(argument))
        elif command == 'set-font-name': data['__font_name'] = str(run_arg(argument))
        elif command == 'set-font-form': data['__font_form'] = str(run_arg(argument))
        elif command == 'set-speed': data['__speed'] = run_arg(argument)
        elif command == 'print':
            tmp = run_arg(argument)
            fname = 'Arial'
            fsize = 8
            fform = 'normal'
            if '__font_name' in data: fname = data['__font_name']
            if '__font_size' in data: fsize = data['__font_size']
            if '__font_form' in data: fform = data['__font_form']
            f = (fname, fsize, fform)
            pen.write(tmp, font=f)

        elif command == 'jump':
            instr_idx = labels[argument.strip()] - 1
            continue
        
        elif command == 'label': pass

        elif command == 'cond-jump':
            if stack.top(): instr_idx = labels[argument.strip()] - 1

        elif command == 'set':
            bits = argument.strip().split(";")
            data[run_arg(bits[0].strip())] = run_arg(bits[1].strip())

        elif command == 'get':
            stack.push(data[run_arg(argument.strip())])

        elif command == 'expr':
            if   argument == '>': data.push(data.pop() > data.pop())
            elif argument == '<': data.push(data.pop() < data.pop())
            elif argument == '=': data.push(data.pop() == data.pop())
            elif argument == '|': data.push(data.pop() or data.pop())
            elif argument == '&': data.push(data.pop() and data.pop())
            elif argument == '!': data.push(not data.pop())
            elif argument == 'dup': data.push(data.top())

            elif argument == '+': data.push(data.pop() + data.pop())
            elif argument == '-': data.push(data.pop() - data.pop())
            elif argument == '*': data.push(data.pop() * data.pop())
            elif argument == '/': data.push(data.pop() / data.pop())

            else:
                print("No such method: '" + argument + "', skipping (please note that the stack is unchanged)", file=sys.stderr)

        else:
            print("Warning! Unknown command '" + command + "', skipping", file=sys.stderr)
        instr_idx += 1
        if instr_idx >= len(instructions): break

    print("Finished! Click on window to close.")

    # Make sure turtle doesn't close.
    pen.getscreen().exitonclick()

# If we run the script and not use it as a library
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        print("Usage:")
        print("python", __file__, " --file <.tmi file>",   "   ->   Run file")
        print("python", __file__, " --help",               "   ->   Show help (you are looking at it now)")
        print("python", __file__, " --verion",             "   ->   Display version")

    elif len(sys.argv) == 2 and sys.argv[1] == '--version':
        print("Turtle Master " + str(VERSION_MAJ + VERSION_MIN))

    elif len(sys.argv) == 3 and sys.argv[1] == '--file':
        if not os.path.exists(sys.argv[2]):
            print("No such file: " + sys.argv[2], file=sys.stderr)
            exit(1)
        instruction_file = open(sys.argv[2], "r")
        code = instruction_file.read()
        run(code)
        instruction_file.close()
    else:
        run(None)
