import sys
import os
from solutions.lib.advent import advent, DayNotFoundException, DuplicateKeyError, Result
from solutions.lib.download import download
from argparse import ArgumentParser
from requests import HTTPError


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '
                        'default uses input file from inputs directory.', type=int)
    parser.add_argument('-a', '--all', action='store_true', dest='run_all',
                        default=False, help='Run all days')
    parser.add_argument('-f', '--file', dest='file',
                        help='Specify different input file from default')
    parser.add_argument('-n', '--numruns', dest='num_runs',
                        help='Specify number of runs to get an average time', default=1, type=int)
    parser.add_argument('-x', '--hide', action='store_true', dest='hide',
                        help='Replace answer output with a bunch of X\'s', default=False)
    parser.add_argument('-i', '--input', action='store_true', dest='download_input',
                        help='Only download/print input for day', default=False)
    parser.add_argument('-g', '--generate', action='store_true', dest='generate_day',
                        help='Generate template solution file for given day', default=False)

    options = parser.parse_args()
    if options.day:
        if options.generate_day:
            generate_new_file(options.day)
        if options.download_input:
            res = download(options.day)
        else:
            res = advent.run(options.day, options.file, options.num_runs, options.hide)
            print_table([res])
    elif options.run_all:
        res = advent.run_all(options.num_runs, options.hide)
        print_table(res)


def day_num_file(day_num) -> str:
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def print_table(outputs: list[Result]):
    part1_lines = [str(out.part1).splitlines() for out in outputs]
    part2_lines = [str(out.part2).splitlines() for out in outputs]
    width1 = max(8, len(max(part1_lines, key=lambda l: len(l[0]))[0]))
    width2 = max(8, len(max(part2_lines, key=lambda l: len(l[0]))[0]))
    day_width = 5
    time_width = 12
    print('╭{}┬{}┬{}┬{}╮'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    print('│ {:^{day}} │ {:^{part1}} │ {:^{part2}} │ {:^{time}} │'
          .format('Day #', 'Part 1', 'Part 2', 'Time (ms)',
                  day=day_width, part1=width1, part2=width2, time=time_width))
    print('├{}┼{}┼{}┼{}┤'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    for p1, p2, out in zip(part1_lines, part2_lines, outputs):
        if len(p1) < len(p2):
            for l in range(len(p2)//2):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[len(p2)//2], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
            for l in range(1+len(p2)//2, len(p2)):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
        else:
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[0], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
    
    if len(outputs) > 1:
        print('├{}┴{}┴{}┼{}┤'.format('─'*(day_width+2), '─' *
            (width1+2), '─'*(width2+2), '─'*(time_width+2)))
        print(f'│ {"Total Time":^{day_width+width1+width2+6}} │ {sum([out.time for out in outputs]):>{time_width}.3f} │')
        print(f'╰{"─"*(day_width+width1+width2+8)}┴{"─"*(time_width+2)}╯')
    else:
        print(f'╰{"─"*(day_width+2)}┴{"─"*(width1+2)}┴{"─"*(width2+2)}┴{"─"*(time_width+2)}╯')


def generate_new_file(day_number):
    path = os.path.join(f'solutions', f'd{day_number:0>2}.py')
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(f'''from .lib.advent import advent
from io import TextIOWrapper


@advent.parser({day_number})
def parse(file: TextIOWrapper):
    return file.readlines()


@advent.day({day_number}, part=1)
def solve1(ipt):
    return 0


@advent.day({day_number}, part=2)
def solve2(ipt):
    return 0
''')


if __name__ == '__main__':
    MIN_MINOR_VERSION = 11
    if sys.version_info.minor < MIN_MINOR_VERSION:
        print(f'Min version Python 3.{MIN_MINOR_VERSION} required')
        exit()
    try:
        main()
    except DayNotFoundException as err:
        print(err)
    except DuplicateKeyError as err:
        print(err)
        print(f'Found duplicate solution key {err.key}')
    except HTTPError as err:
        pass
    
