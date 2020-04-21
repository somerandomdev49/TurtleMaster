# Turtle Master 2200

To get help for the command line interface: `python main.py help`

## Values:
each value, string, anything (except for instruction names) is a value. And because those values have different types, the Turtle Master needs to be able to differentiate between those types. So here are *prefixes* that depict what type the value is:
 *prefix*   | type   | description 
------------|--------|-------------
 `$`        | number | signed float
 `%`        | data   | value of a data entry with a name
 `[string]` | string | string with `\n \r \t` escapes.
 `=`        | name   | returns the *name* of an entry
 `@`        | last   | no value, just the prefix, last compute value

## Instruction set:
```
forward:x go forward by x
backward:x go backward by x
left:x rotate to left by x degrees
right:x rotate to the right by y degrees
up:. pull the pen up
down:. pull the pen down
color:name change the color to name (use [string])
begin-fill: begin filling
end-fill: end filling the shape
circle:r draw a circle with radius of r
goto:x;y change the x coordinate to x and y coordinate to y
movex:dx add dx to the x coordinate value
movey:dy add dy to the y coordinate value
write:s print data from s
jump:lbl jump to a label
cond-jump:lbl jump only if @ is true (python true)
expr:m;a;b sets @ to the result of evaluated expression, see expr command
```

## `expr` command:
| `method; a; b` | python expression |
|----------------|-------------------|
| `+; a; b  `    | `a + b      `     |
| `-; a; b  `    | `a - b      `     |
| `*; a; b  `    | `a * b      `     |
| `/; a; b  `    | `a / b      `     |
| `>; a; b  `    | `a > b      `     |
| `<; a; b  `    | `a < b      `     |
| `=; a; b  `    | `a == b     `     |
| `\|; a; b `    | `a or b     `     |
| `&; a; b  `    | `a and b    `     |
| `!; a     `    | `not a      `     |
| `get; a   `    | `data[a]    `     |
| `set; a; b`    | `data[a] = b`     |

## File Structure:
Code is split into instructions with newlines.<br>
Instructions are split into a name and an argument with colons (`:`)<br>
For some command the argument is split into smaller bits with semi-colons (`;`)<br>
For comments use number symbol (`#`)<br>
1. `optional data segment`<br>
    Example:
    ```
    data:
        name=$10
        str=[string]Hello,\nWorld!
    ```
2. `code segment`<br>
    Example:
    ```
    code:
        forward:$100
        left:$name
    ```


## Files:
* `main.py` - the *Turtle Master 2200*
* `example.tmi` - an example (works only with Turtle Master 2000)
* `homework.tmi` - homework
* `homework.tmi` - homework 2
