# c_comment_read
C言語ソースコードコメント読み上げプログラム

## バージョン
0.9.1

## 作成者
近藤 英雅 (KONDO Hidemasa)

## 内容物
- README.txt  
これ
- c_comment_read.sh  
C言語ソースコード読み上げの処理を行うshell script
- comment.py  
ソースコード内のコメントとその行番号を列挙する内部処理
- tmp.c  
テスト用のC言語ソースコード

## 書式
./c_comment_read.sh [-h] [-l] c_filename ...

## 引数とオプション
**-h**  
> Display help  

**-l**  
> with number of line  

**c_filename**  
> C言語のソースコードファイル  

## 実例
```
$ ./c_comment_read.sh tmp.c
#include <stdio.h>

// プログラムを読み上げます
int main(void) {
    return 0; // 終了します
}
$
```
