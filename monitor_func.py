#!/usr/bin/python
# coding=utf-8
from urwid import raw_display

s = raw_display.Screen()

def get_screen_cols():
    cols, rows = s.get_cols_rows()
    
    return cols

def get_screen_rows():
    cols, rows = s.get_cols_rows()
    
    return rows
