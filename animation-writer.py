#!/usr/bin/python3
import re

def format_value(v):
    if re.match(r'^\d', v):
        return v
    return f'var(--{v})'
# XOR: C=A^B ->
#   (('C', 'dest', 1),),
#   (('C', 'dest', 0), ('A', 'src', 1), ('B', 'src', 1)),
#   (('C', 'dest', 0), ('A', 'src', 0), ('B', 'src', 0)),
# AND
#   
# OR
commands = (
    # init
    (('a', 'dest', 1),),
    (('b', 'dest', 1),),
    (('c', 'dest', 1),),
    (('temp-1', 'dest', 0),),
    (('temp-2', 'dest', 0),),
    (('temp-3', 'dest', 0),),
    (('sum', 'dest', 0),),
    (('carry', 'dest', 1),),
    # temp-1 = a XOR b
    (('temp-1', 'dest', 1),),
    (('temp-1', 'dest', 0), ('a', 'src', 1), ('b', 'src', 1)),
    (('temp-1', 'dest', 0), ('a', 'src', 0), ('b', 'src', 0)),
    # sum = temp-1 XOR c
    (('sum', 'dest', 1),),
    (('sum', 'dest', 0), ('temp-1', 'src', 1), ('c', 'src', 1)),
    (('sum', 'dest', 0), ('temp-1', 'src', 0), ('c', 'src', 0)),
    # temp-2 = temp-1 AND c
    (('temp-2', 'dest', 1), ('temp-1', 'src', 1), ('c', 'src', 1)),
    # temp-3 = a AND b
    (('temp-3', 'dest', 1), ('a', 'src', 1), ('b', 'src', 1)),
    # carry = temp-2 OR temp-3
    (('carry', 'dest', 0), ('temp-2', 'src', 0), ('temp-3', 'src', 0)),
    tuple()
)

keyframes = {}
for index, items in enumerate(commands):
    # print(index, items)
    for command in items:
        # print(index, command)
        name = command[0]
        percent = f'{index}%'
        keyframes.setdefault(name, {})
        keyframes[name].setdefault(percent, {})
        current = keyframes[name][percent]

        if command[1] == 'dest':
            current['top'] = 'accept-input-top'
            current['z-index'] = 'accept-input-z'

            if command[2] == 0:
                current['left'] = 'write-0-if-1'
            else:
                current['left'] = 'write-1-if-0'

        elif command[1] == 'move':
            current['top'] = 'accept-input-top'
            current['z-index'] = 'accept-input-z'
            current['left'] = 'active-move'

        elif command[1] == 'src':
            current['top'] = 'perform-output-top'
            current['z-index'] = 'perform-output-z'
            
            if command[2] == 0:
                current['left'] = 'read-from-if-0'
            else:
                current['left'] = 'read-from-if-1'
        # print(index, name, percent, current)

for name, frames in keyframes.items():
    print(f'@keyframes {name}-path {{')
    for index in range(len(commands)):
        percent = f'{index}%'
        frames.setdefault(percent, {
            'left': '0',
            'top': f'{name}-home',
            'z-index': '0'
        })
        frame = frames[percent]
        left = format_value(frame['left'])
        top = format_value(frame['top'])
        z_index = format_value(frame['z-index'])
        print(f'  {index}% {{ left: {left}; top: {top}; z-index: {z_index}; }}')
    print('}')