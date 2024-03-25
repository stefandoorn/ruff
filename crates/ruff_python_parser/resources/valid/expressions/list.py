# Simple lists
[]
[1]
[1,]
[1, 2, 3]
[1, 2, 3,]

# Mixed with indentations
[
]
[
        1
]
[
    1,
        2,
]

# Nested
[[[1]]]
[[1, 2], [3, 4]]

# Named expression
[x := 2]
[1, x := 2, 3]

# Random expressions
[1 + 2, [1, 2, 3, 4], (a, b + c, d), {a, b, c}, {a: 1}, x := 2]
[call1(call2(value.attr()) for element in iter)]