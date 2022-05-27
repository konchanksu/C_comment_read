# c_comment_read
read aloud C source code

## Version
0.9.1

## System Requirements
### Macintosh  
12.0 or higher
### Python
3.8 or higher
### Bash
3.2 or higher  

## Author
KONDO Hidemasa

## Files
```
.
├── README.md          # readme!
├── c_comment_read.sh  # main file
├── c_programs
│   └── tmp.c          # soruce code for operation check
└── src
    ├── MANIFEST.in    # python's MANIFEST File
    ├── Makefile       # python's build file
    └── packages
        └── comment.py # python file (comment analyzer)
```

## Usage
c_comment_read.sh [-h] [-l] [-s <time_ms>] c_filename ...  

## Args and options
**-h**  
> Display help  

**-l**  
> with number of line  

**-s**
> sleep for specified time (number)

**c_filename**  
> C言語のソースコードファイル  

## Example
```terminal
$ ./c_comment_read.sh c_programs/tmp.c
#include <stdio.h>

// プログラムを読み上げます
int main(void) {
    return 0; // 終了します
}
$
```
