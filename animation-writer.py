#!/usr/bin/python3

commands = (
    (('a', 'dest', 1),),
    (('b', 'dest', 1),),
    (('c', 'dest', 1),),
    (('temp-1', 'dest', 0),),
    (('temp-2', 'dest', 0),),
    (('temp-3', 'dest', 0),),
    (('sum', 'dest', 0),),
    (('carry', 'dest', 1),),
    (('temp-1', 'move'), ('a', 'src', 1)),
    (('temp-1', 'move'), ('b', 'src', 1)),
    (('sum', 'move'), ('temp-1', 'src', 1)),
    (('sum', 'move'), ('c', 'src', 1)),
    (('temp-2', 'dest', 1), ('temp-1', 'src', 1), ('c', 'src', 1)),
    (('temp-3', 'dest', 1), ('a', 'src', 1), ('b', 'src', 1)),
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
            current['top'] = 'var(--accept-input-top)'
            current['z-index'] = 'var(--accept-input-z)'

            if command[2] == 0:
                current['left'] = 'var(--write-0-if-1)'
            else:
                current['left'] = 'var(--write-1-if-0)'

        elif command[1] == 'move':
            current['top'] = 'var(--accept-input-top)'
            current['z-index'] = 'var(--accept-input-z)'
            current['left'] = 'var(--active-move)'

        elif command[1] == 'src':
            current['top'] = 'var(--perform-output-top)'
            current['z-index'] = 'var(--perform-output-z)'
            
            if command[2] == 0:
                current['left'] = 'var(--read-from-if-0)'
            else:
                current['left'] = 'var(--read-from-if-1)'
        # print(index, name, percent, current)

for name, frames in keyframes.items():
    print(f'@keyframes {name}-path {{')
    for index in range(len(commands)):
        percent = f'{index}%'
        frames.setdefault(percent, {
            'left': '0',
            'top': f'var(--{name}-home)',
            'z-index': '0'
        })
        frame = frames[percent]
        print(f'  {index}% {{ left: {frame["left"]}; top: {frame["top"]}; z-index: {frame["z-index"]}; }}')
    print('}')