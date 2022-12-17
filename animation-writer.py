#!/usr/bin/python3
import re

def format_value(v):
    if re.match(r'^\d', v):
        return v
    return f'var(--{v})'
def dest(name: str, value: int):
    return (name, 'dest', value)
def src(name: str, value: int):
    return (name, 'src', value)

# XOR: C=A^B ->
#   (('C', 'dest', 1),),
#   (('C', 'dest', 0), ('A', 'src', 1), ('B', 'src', 1)),
#   (('C', 'dest', 0), ('A', 'src', 0), ('B', 'src', 0)),
def doXor(output: str, input1: str, input2: str):
    return (
        (dest(output, 1),),
        (dest(output, 0), src(input1, 1), src(input2, 1)),
        (dest(output, 0), src(input1, 0), src(input2, 0)),
    )

def doAnd(output: str, input1: str, input2: str):
    return (
        (dest(output, 0),),
        (dest(output, 1), src(input1, 1), src(input2, 1))
    )

def doOr(output: str, input1: str, input2: str):
    return (
        (dest(output, 1),),
        (dest(output, 0), src(input1, 0), src(input2, 0))
    )
def doSet(name: str, value: int):
    return (dest(name, value),)

# AND
#   
# OR
program = (
    # init
    doSet('a', 1),
    doSet('b', 1),
    doSet('c', 1),
    # add
    *doXor('temp-1', 'a', 'b'),
    *doXor('sum', 'temp-1', 'c'),
    # carry
    *doAnd('temp-2', 'temp-1', 'c'),
    *doAnd('temp-3', 'a', 'b'),
    *doOr('carry', 'temp-2', 'temp-3'),
    tuple()
)

keyframes = {}
for index, items in enumerate(program):
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

        # elif command[1] == 'move':
        #     current['top'] = 'accept-input-top'
        #     current['z-index'] = 'accept-input-z'
        #     current['left'] = 'active-move'

        elif command[1] == 'src':
            current['top'] = 'perform-output-top'
            current['z-index'] = 'perform-output-z'
            
            if command[2] == 0:
                current['left'] = 'read-from-if-0'
            else:
                current['left'] = 'read-from-if-1'
        # print(index, name, percent, current)

# TODO: keyhole optimization: skip frame if same as previous and next
for name, frames in keyframes.items():
    print(f'@keyframes {name}-path {{')
    for index in range(len(program)):
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