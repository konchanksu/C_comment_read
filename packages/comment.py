#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C言語のソースコードを入力し、ソースコード内に含まれているコメントを解析して、出力するプログラム
"""

__author__ = "KONDO Hidemasa"
__date__ = "2022/05/24"
__version__ = "0.9.0"

import os
import sys
from copy import copy
from enum import Enum
from typing import List
import unittest


class StringAndNumberOfLine():
    # pylint: disable=too-few-public-methods
    """
    文字列とその行番号を扱うクラス
    """
    def __init__(self, strings, number_of_line) -> None:
        """
        コンストラクタ

        Args:
            string (str, optional): 文字列. Defaults to "".
            number_of_line (int, optional): 行番号. Defaults to 1.
        """
        self.strings = strings
        self.number_of_line = number_of_line

    def __str__(self) -> str:
        """
        文字列に変換する

        Returns:
            str: 文字列
        """
        return f"{self.number_of_line} {''.join(self.strings)}"

class CommentAnalyzer():
    """
    C言語のコメントの解析を行うクラス
    """
    EMPTY_STRING = (" ", "\t")
    ASTERISK = "*"
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    SLASH = "/"
    BACK_SLASH = "\\"
    LINE_SEP = os.linesep

    class CommentState(Enum):
        """ 文字 状態 """
        DEFAULT = 1
        IN_DOUBLE_QUARTS = 2
        IN_SINGLE_QUARTS = 3
        IN_MULTIPLE_COMMENT = 4
        IN_SINGULAR_COMMENT = 5
        IN_ONE_SLASH = 6

    class MultipleCommentState(Enum):
        """ 複数コメント状態 """
        NONE = 1
        DEFAULT = 2
        LINE_SEP = 3
        ASTERISK = 4

    def __init__(self):
        """ コンストラクタ """
        self.state: self.CommentState = self.CommentState.DEFAULT
        self.multiple_comment_state: self.MultipleCommentState = self.MultipleCommentState.NONE
        self.comment: List[str] = []
        self.comments: List[StringAndNumberOfLine] = []
        self._state_func_dictionary = {
            self.CommentState.DEFAULT: self._in_state_default,
            self.CommentState.IN_ONE_SLASH: self._in_state_on_slash,
            self.CommentState.IN_SINGLE_QUARTS: self._in_single_quarts,
            self.CommentState.IN_DOUBLE_QUARTS: self._in_double_quarts,
            self.CommentState.IN_SINGULAR_COMMENT: self._in_singular_comment,
            self.CommentState.IN_MULTIPLE_COMMENT: self._in_multiple_comment,
        }

    def run(self, source_code: str):
        """
        アナライザを実行する

        Args:
            source_code (str): C言語のソースコード文字列
        """
        for number_of_line, string in enumerate(source_code.split(os.linesep), start=1):
            if self.state != self.CommentState.IN_MULTIPLE_COMMENT:
                self.comment = []
            else:
                self.comment = [""]
            for char in string + os.linesep:
                self._state_func_dictionary[self.state](char)
            if len(self.comment) != 0 and not (len(self.comment) == 1 and self.comment[0] == ""):
                self.comments.append(StringAndNumberOfLine(self.comment, copy(number_of_line)))

    def get_result(self) -> List[str]:
        """
        アナライズ結果を返却する

        Returns:
            List[str]: 解析されされて得た文字列
        """
        return self.comments

    def reset(self):
        """ 解析結果をリセットして初期状態にする """
        self.state = self.CommentState.DEFAULT
        self.multiple_comment_state= self.MultipleCommentState.NONE
        self.comments = []
        self.comment = []

    def _in_state_default(self, char: str):
        """
        ステータスが何も起きていない状態の時の処理

        Args:
            char (str): 入力された一文字
        """
        if char == '"':
            self.state = self.CommentState.IN_DOUBLE_QUARTS
        elif char == "'":
            self.state = self.CommentState.IN_SINGLE_QUARTS
        elif char == "/":
            self.state = self.CommentState.IN_ONE_SLASH

    def _in_state_on_slash(self, char: str):
        """
        スラッシュが一つついた時の状態の処理

        Args:
            char (str): 入力された一文字
        """
        if char == CommentAnalyzer.SLASH:
            self._change_for_singular_comment_state()
        elif char == CommentAnalyzer.ASTERISK:
            self._change_for_multiple_comment_state()
        elif char == CommentAnalyzer.SINGLE_QUOTE:
            self.state = self.CommentState.IN_SINGLE_QUARTS
        elif char == CommentAnalyzer.DOUBLE_QUOTE:
            self.state = self.CommentState.IN_DOUBLE_QUARTS
        else:
            self.state = self.CommentState.DEFAULT

    def _in_double_quarts(self, char: str):
        """
        ダブルクォートの文字列の中の処理

        Args:
            char (str): 入力された一文字
        """
        if char == CommentAnalyzer.DOUBLE_QUOTE:
            self._change_for_default_state()

    def _in_single_quarts(self, char: str):
        """
        シングルクォートの文字列の中の処理

        Args:
            char (str): 入力された一文字
        """
        if char == CommentAnalyzer.SINGLE_QUOTE:
            self._change_for_default_state()

    def _in_singular_comment(self, char: str):
        """
        1行コメントの時の処理

        Args:
            char (str): 入力された一文字
        """
        if char == CommentAnalyzer.LINE_SEP:
            self._change_for_default_state()
            return
        self.comment[-1] += char

    def _in_multiple_comment(self, char: str):
        """
        複数行コメントの時の処理

        Args:
            char (str): 入力された一文字
        """
        if self.multiple_comment_state == self.MultipleCommentState.DEFAULT:
            self._in_multiple_comment_default(char)
        elif self.multiple_comment_state == self.MultipleCommentState.LINE_SEP:
            self._in_multiple_comment_line_sep(char)
        elif self.multiple_comment_state == self.MultipleCommentState.ASTERISK:
            self._in_multiple_comment_asterisk(char)

    def _in_multiple_comment_default(self, char: str):
        """
        複数コメント中かつデフォルトの処理

        Args:
            char (str): 文字
        """
        if char == "*":
            self.multiple_comment_state = self.MultipleCommentState.ASTERISK
            self.comment[-1] += char
        elif char == CommentAnalyzer.LINE_SEP:
            self.multiple_comment_state = self.MultipleCommentState.LINE_SEP
        else:
            self.comment[-1] += char

    def _in_multiple_comment_line_sep(self, char: str):
        """
        複数コメント中かつ改行文字後の処理

        Args:
            char (str): 文字
        """
        if char in CommentAnalyzer.EMPTY_STRING:
            pass
        elif char == "*":
            self.multiple_comment_state = self.MultipleCommentState.ASTERISK
        elif char == os.linesep:
            self.multiple_comment_state = self.MultipleCommentState.LINE_SEP
        else:
            self.multiple_comment_state = self.MultipleCommentState.DEFAULT
            self.comment[-1] += char

    def _in_multiple_comment_asterisk(self, char: str):
        """
        複数コメント中かつアスタリスクの処理

        Args:
            char (str): 文字
        """
        if char == CommentAnalyzer.SLASH:
            self._change_for_default_state()
        elif char == CommentAnalyzer.ASTERISK:
            pass
        elif char in CommentAnalyzer.EMPTY_STRING:
            pass
        elif char == CommentAnalyzer.LINE_SEP:
            self.multiple_comment_state = self.MultipleCommentState.LINE_SEP
        else:
            self.comment[-1] += char
            self.multiple_comment_state = self.MultipleCommentState.DEFAULT


    def _change_for_singular_comment_state(self):
        """ 1行コメント状態への遷移 """
        self.state = self.CommentState.IN_SINGULAR_COMMENT
        self.comment.append("")

    def _change_for_multiple_comment_state(self):
        """ 複数行コメント状態への遷移 """
        self.state = self.CommentState.IN_MULTIPLE_COMMENT
        self.multiple_comment_state = self.MultipleCommentState.ASTERISK
        self.comment.append("")

    def _change_for_default_state(self):
        """ 通常状態への遷移 """
        self.multiple_comment_state = self.MultipleCommentState.NONE
        self.state = self.CommentState.DEFAULT


class TestCommentAnalyzer(unittest.TestCase):
    """
    テストケースを確認するクラス

    Args:
        unittest: ユニットテストクラス
    """
    def test__通常コメントが解析できる(self):
        """
        単行コメント解析テスト
        """
        analyzer = CommentAnalyzer()
        analyzer.run("// コメントです")
        self.assertEqual([" コメントです"], analyzer.get_result()[0].strings)

    def test__複数行コメントが解析できる(self):
        """
        複数行コメント解析テスト
        """
        analyzer = CommentAnalyzer()
        analyzer.run(
"""
ああああ
/*
 * 複数行コメント
 * hogehoge
 */
いいいい
"""
        )
        self.assertEqual(["複数行コメント"], analyzer.get_result()[0].strings)
        self.assertEqual(["hogehoge"], analyzer.get_result()[1].strings)

    def test__文字列が含まれた時の処理_正しく解析できる(self):
        """
        文字列解析テスト
        """
        string_single = "'aaaa//test/*  */'//test"
        string_double = '"aaaa//test/*  */"//test'

        analyzer = CommentAnalyzer()
        analyzer.run(string_single)
        self.assertEqual(["test"], analyzer.get_result()[0].strings)

        analyzer.reset()
        analyzer.run(string_double)
        self.assertEqual(["test"], analyzer.get_result()[0].strings)

def stdin_string() -> str:
    """ 標準入力から文字列をとってきます """
    return "".join(sys.stdin)

def main():
    """ メイン関数 """
    analyzer = CommentAnalyzer()
    string = stdin_string()
    analyzer.run(string)
    sys.stdout.write(os.linesep.join(map(str, analyzer.get_result())))

if __name__ == "__main__":
    sys.exit(main())
