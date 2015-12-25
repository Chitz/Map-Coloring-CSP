Map Coloring - Constraint Satisfaction Problem

An alternative version to Map Coloring Problem, a classic Constraint Satisfaction Problem.

Problem Statement - 
To assigns a frequency A, B, C, and D to each 50 states, subject to the constraints that 
(1) no two adjacent states share the same frequency, and 
(2) the states that have legacy equipment that supports only one frequency are assigned to that frequency. 

Command line: python radio.py legacy_constraints_file

where legacy constraints file is an input to your program and has the legacy constraints listed in a format like this:Indiana ANew_York BWashington A

adjacent-states - lists the states that are adjacent to other states 