#!/usr/bin/env python3
"""
"""
import ast

s = "[(0,0),(0.5,1),(1,0)]"

l = ast.literal_eval(s)
for t in l:
    print(type(t))
