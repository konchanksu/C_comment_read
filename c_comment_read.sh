#!/bin/bash

# 作成：2022/05/24：近藤 英雅 (KONDO HIDEMASA)
# 修正：2022/05/24：近藤 英雅 (KONDO HIDEMASA)
#    -l -h オプションの追加

: << EOF_COMMENT
-----------------------------------------------------------
c_comment_read.sh

C言語のファイルを渡すと、プログラムの中身を表示しながら、
その行に書かれているコメント文をsayコマンドで読み上げるプログラム。

====================== tmp.c ======================
#include <stdio.h>

// プログラムを読み上げます
int main(void) {
    return 0; // 終了します
}
プログラムの読み上げを終了します。
===================================================

$ ./c_comment_read.sh c_programs/tmp.c
#include <stdio.h>

// プログラムを読み上げます (このコメントは音声で読み上げられる)
int main(void) {
    return 0; // 終了します (このコメントは音声で読み上げられる)
}
$
-----------------------------------------------------------
EOF_COMMENT

# usageを表示
function usage {
    cat << EOM
Usage: $(basename "$0") [-h] [-l] [-s <time_ms>] c_filename ...
  -h           Display help
  -l           with number of line
  -s           sleep for specified time (number)
EOM

  exit 2
}

# プログラム読み上げ処理
function c_comment_read() {
    file=$1
    sleep_ms=$2
    python_file=`find . -name comment.py`

    # コメントの行番号と文字列を整理する
    strings=()
    numbers=()
    while read number string
    do
        strings+=("${string}")
        numbers+=(${number})
    done << EOS
    $(cat "$file" | python "$python_file")
EOS

    # echo ${strings[@]}
    # echo ${numbers[@]}

    # 行の表示を行う
    line_count=1
    max_number_of_line=(`wc -l ${file}`)
    max_number_of_line=${#max_number_of_line}
    echo "======== $file ========"
    cat "$file" | while IFS= read -r line; do
        # 行番号オプションあるなら行番号表示
        if "$number_of_line"; then
            printf "%${max_number_of_line}d: " "${line_count}"
        fi

        echo "$line"

        # 行にコメントがあるなら文字列読み上げ
        if [ 0 -lt ${#numbers[@]} ]; then
            if [ $line_count -eq ${numbers[0]} ]; then
                say "${strings[0]}"
                numbers=("${numbers[@]:1}")
                strings=("${strings[@]:1}")
            fi
        fi
        line_count=`expr $line_count + 1`
        sleep $sleep_ms
    done
}

# 引数の有無を確認する
if [ $# -eq 0 ]; then
    usage
fi

python_file=`find . -name comment.py`
# 必要なpythonプログラムの存在を確かめる
if [ ! -f $python_file ]; then
    echo '内部処理を行うpythonプログラムが存在しません'
    exit 1
fi

type python > /dev/null 2>&1
# pythonのコマンドが存在するかどうか
if [ $? -ne 0 ]; then
    echo "pythonのコマンドが存在しません"
    exit 1
fi

# 引数用の変数
number_of_line=false
sleep_ms=0
args_count=0
args=($@)

# 引数別の処理
while getopts 'hls:' opt_key; do
    case "$opt_key" in
        'l')
            number_of_line=true
            args_count=`expr ${args_count} + 1`
            ;;
        's')
            echo "${OPTARG}" | grep -E "[0-9]+\.[0-9]+|[0-9]+" > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                sleep_ms=${OPTARG}
            else
                usage
            fi
            args_count=`expr ${args_count} + 2`
            ;;
        'h'|*)
            usage
            ;;
    esac
done

# 各ファイルに対して実行
for file in "${args[@]:${args_count}}"; do
    # ファイルが存在する時
    if [ -f $file ]; then
        c_comment_read $file $sleep_ms
    else
        # 存在しない時
        echo "$file は存在しません"
    fi
done

echo 'プログラムの読み上げを終了します。'
say 'プログラムの読み上げを終了します。'
