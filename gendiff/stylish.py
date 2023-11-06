from gendiff.gendiff_logic import (
    get_children, get_value1, get_value2,
    get_status1, get_status2, get_name
)


INDENT = '    '


def to_string(value):
    if isinstance(value, bool):
        new_value = str(value).lower()
    elif value is None:
        new_value = 'null'
    else:
        new_value = str(value)
    return new_value


def stylish_value(value, stylish_depth):

    def walk(node, depth):
        if not isinstance(node, dict):
            return to_string(node)
        total_depth = depth + stylish_depth
        lines = []
        for key, val in node.items():
            lines.append(
                f'{INDENT * (total_depth)}{key}: {walk(val, depth + 1)}'
            )
        result = ['{'] + lines + [f'{INDENT * (total_depth - 1)}' + '}']
        return '\n'.join(result)

    return walk(value, 0)


def build_lines(node, depth):
    curr_indent = INDENT * depth
    if node == '}':
        return (curr_indent) + node
    name = get_name(node)
    children = get_children(node)
    stat1 = get_status1(node)
    stat2 = get_status2(node)
    val1 = get_value1(node)
    val2 = get_value2(node)
    lines = []
    if not children:
        lines.append(
            f'{curr_indent}  {stat1} {name}: {stylish_value(val1, depth + 2)}'
        )
    if not children and stat2:
        lines.append(
            f'{curr_indent}  {stat2} {name}: {stylish_value(val2, depth + 2)}'
        )
    if children and name:
        lines.append(f'{curr_indent}    {name}: ' + '{')
    if children:
        lines.extend(
            list(map(lambda child: build_lines(child, depth + 1),
                 children + ['}']))
        )
    return '\n'.join(lines)


def stylish(tree):
    if not tree:
        return '{\n\n}'
    return '{\n' + build_lines(tree, -1)
