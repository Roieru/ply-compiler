# PLY Compiler

To execute this program, run
```python3 .\plytac.py```

The program takes its input from the file ```input.txt```.
The 3AC output is generated into the file ```output.txt```.

**Special considerations**

 - Since it was an optional feature, `print` statements are not supported.
 - Only int2float convertions are implicit, num2string has to be made explicit by surrounding the expresion with `string( )`
 - Operator precedence is followed
 - Some operations are simplified when converted to 3AC

| Regex | Use |
|--|--|
| and, or | Boolean operations |
| boolean, int, float, string | Variable declaration |
| !=, ==, <, >, <=, >= | Comparison |
| if, elif, else | If statements |
| do, while, for | Loops |
| [A-Za-z_]\[A-Za-z_0-9]* | Variable names |
| ".*" | String values |
| [0-9]+ | Integer values|
| [0-9]+\\.[0-9]+ | Float values |
| true, false| Boolean values |
| +, -, *, ^, / | Operators |
| (, ), {, } | Flow control |
| ; | End of statement |
| = | Assignation |

![alt text](https://media.tenor.com/images/5bd5282f3ceae2a96a880c3f7c70e8fb/tenor.gif "My friends if I get a 100")
My friends if I get a 100