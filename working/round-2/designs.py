"""Hand-drawn symbol variants on the module grid (row 0 = top).
Digits: 1 Sage (low) · 2 Lichen (high) · 3 Chalk (summit) · 9 Flag (observation) · . empty"""
S1 = {  # contour: one closed contour around a summit, runs broken at the diagonals
"S1a": """
...222..
.2....2.
2....3.2
2.....2.
2......2
.2....2.
..2222..""",
"S1b": """
..2222..
.2....2.
2...3..2
2......2
.2.....2
..2...2.
...222..""",
"S1c": """
...2222.
..2....2
.2...3.2
2......2
2.....2.
.2...2..
..222...""",
"S1d": """
..22....
.2..22..
2.....2.
2...3..2
2......2
.2....2.
..2222..""",
}
S2 = {  # raster: the summit as a small heightmap, one observation flagged
"S2a": """
...11...
..1221..
.112321.
1122221.
.11221..
..11.9..""",
"S2b": """
....11..
..11221.
.1123221
11222211
.1111.9.""",
"S2c": """
...1....
..121...
.12321..
1122221.
.111129.""",
"S2d": """
..11....
.1221.1.
1123211.
.122221.
..1119..""",
}
S3 = {  # profile: the ridge surface plotted as one measured line
"S3a": """
.....3..
....2.2.
....2..2
..12....
11......
........""",
"S3b": """
.....3..
....22..
...2..2.
.11....2
1.......""",
"S3c": """
......3.
.....2.2
..2.2...
.1.2....
1.......""",
"S3d": """
....3...
...2.2..
..2...2.
.1.....1
1.......""",
}
def parse(s):
    rows = [r for r in s.strip("\n").split("\n")]
    w = max(len(r) for r in rows)
    return [[0 if ch == "." else int(ch) for ch in r.ljust(w, ".")] for r in rows]
ALL = {**{k: parse(v) for k, v in S1.items()}, **{k: parse(v) for k, v in S2.items()}, **{k: parse(v) for k, v in S3.items()}}

S1 |= {  # elongated, valley-notched contours — avoid the eye / Pac-Man reading
"S1e": """
....222.
...2...2
..2..3.2
.2....2.
2....2..
2...2...
.222....""",
"S1f": """
.....22.
..222..2
.2...3.2
2.....2.
.2..22..
..22....""",
"S1g": """
...2222.
..2....2
.2..3..2
2....22.
2...2...
.222....""",
"S1h": """
......2.
....22.2
..22.3.2
.2.....2
2.....2.
.22222..""",
}
S2 |= {  # heat-map silhouettes with a valley so they are not a pyramid or a blob
"S2e": """
.....11.
...1122.
..11232.
.1122.2.
1112...9
.11.....""",
"S2f": """
......1.
....1121
..11232.
.1122.9.
1121....
.1......""",
"S2g": """
...11...
..1221..
.112321.
1122.221
.11.9.11""",
"S2h": """
.....1..
....121.
...12321
..1122.1
.1121.9.
1111....""",
}
S3 |= {  # refinements of S3a: approach, summit, short drop; optional flag on the line
"S3e": """
.....3..
....2.2.
...2...2
.11.....
1.......""",
"S3f": """
.....3..
....2.2.
....2..2
..19....
11......""",
"S3g": """
......3.
.....2.2
....2...
..12....
11......""",
"S3h": """
.....3..
....2.2.
...2...9
.11.....
1.......""",
}
ALL = {**{k: parse(v) for k, v in S1.items()}, **{k: parse(v) for k, v in S2.items()}, **{k: parse(v) for k, v in S3.items()}}

S3 |= {  # bold cut: the surface band two cells deep
"S3e2": """
.....3..
....232.
...22.22
.112..2.
112.....
11......""",
}
ALL = {**{k: parse(v) for k, v in S1.items()}, **{k: parse(v) for k, v in S2.items()}, **{k: parse(v) for k, v in S3.items()}}
