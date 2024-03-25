# Double star expression starts with bitwise OR precedence. Make sure we don't parse
# the ones which are higher than that.

{**x := 1}

# TODO(dhruvmanila): Uncomment once the precedence is fixed
# {**x if True else y}
# {**lambda x: x}
# {**x or y}
# {**x and y}
# {**not x}
# {**x in y}
# {**x not in y}
# {**x < y}