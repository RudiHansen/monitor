#!/usr/bin/python
# coding=utf-8
from urwid import raw_display


def get_screen_cols():
    cols, rows = raw_display.Screen().get_cols_rows()
    
    return cols

def get_screen_rows():
    cols, rows = raw_display.Screen().get_cols_rows()
    
    return rows
