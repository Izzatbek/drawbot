from math import pi

from joint import REVOLUTE_JOINT, PRISMATIC_JOINT, FIXED_JOINT
from joint import PASSIVE_JOINT as PJOINT
from joint import ACTUATED_JOINT as AJOINT

table1 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (1, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, 0, 0, pi, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    )

table_tree = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, 0, 0, 50, 0),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 1, 150, 0.5, 50),
    (2, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, 0, 200, pi / 2, -220),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, pi / 2, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        1, 100, 0, 200, -pi / 2, 0),
    (5, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, pi / 2, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        1, 0, pi/4, 200, pi / 4, 100),
    (7, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, pi / 2, 0),
    )

D3 = 300
RL4 = 400
table_rx90 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi / 2, 0, 0, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, D3, 0, 0),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, 0, 0, RL4),
    (4, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi / 2, 0, 0, 0),
    (5, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, 0, 0, 0)
    )

table_stanford = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, 0, 0, 200),
    (2, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, pi / 2, 0, 0, 400),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (4, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, 0, 0, 0),
    (5, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi / 2, 0, 0, 0)
    )

# SR400
d2 = 400
d3 = 800
d4 = -200
rl4 = 1000
d8 = 1000
table_sr400 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),  # 1
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, d2, -pi/2, 0),  # 2
    (2, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, d3, 0, 0),  # 3
    (3, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, d4, 0, rl4),  # 4
    (4, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi / 2, 0, 0, 0),  # 5
    (5, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, 0, 0, 0),  # 6
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi / 2, d2, 0, 0),  # 7
    (7, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, d8, 0, 0),  # 8
    (8, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, d3, 0, 0),  # 9
    (3, 9, 0, FIXED_JOINT,
        pi / 2, 0, 0, -d8, 0, 0),  # 10
        )

d3 = -200
d4 = 200
r5 = 300
r6 = 300
d7 = 300
r8 = 500
d13 = 200
d14 = 300
table_akr3000 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),              # 1
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 0, 0, 0),           # 2
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, d3, 0, 0),          # 3
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, d4, 0, 0),          # 4
    (3, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, -pi/2, 0, 0, r5),         # 5
    (4, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, -pi/2, 0, 0, r6),         # 6
    (2, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, d7, 0, 0),             # 7
    (7, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi/2, 0, 0, r8),         # 8
    (8, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 0, 0, 0),           # 9
    (9, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi/2, 0, 0, 0),          # 10
    (5, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 0, 0, 0),           # 11
    (6, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 0, 0, 0),           # 12
    (7, 11, PJOINT, FIXED_JOINT,
        pi/1.6, 0, 0, d13, 0, 0),            # 13
    (2, 12, PJOINT, FIXED_JOINT,
        -pi/5, 0, 0, d14, 0, 0)             # 14
)

table_testloop_r4 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 0, FIXED_JOINT,
        0, 0, 0, 0, 0, 0),              # 1
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),              # 2
    (2, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 3
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 4
    (3, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 5
    (4, 5, 0, FIXED_JOINT,
        pi/2, 0, 0, 100, 0, 0)          # 6
)

table_testloop2 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 0, FIXED_JOINT,
        0, 0, 0, 0, 0, 0),              # 1
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),              # 2
    (2, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 3
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 4
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, -100, 0, 0),           # 5
    (3, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 6
    (3, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, -100, 0, 0),           # 7
    (4, 6, 0, FIXED_JOINT,
        pi/2, 0, 0, 100, 0, 0),         # 8
    (5, 7, 0, FIXED_JOINT,
        -pi/2, 0, 0, 100, 0, 0)         # 9
)

table_test_shapes = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi / 2, 0, 0, 0)
)

table_scara = (
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 200, 0, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 400, 0, 0),
    (3, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, 0, 0, 0, -300)
)

table_exam = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 200),
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 200, 0, 0),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 400, 0, 0),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi/2, 300, 0, 300),
    (4, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, -pi/2, 0, 0, 300)
)

table_exam2 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 200),
    (1, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, 0, 0, 0, 200),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, pi/2, 0, 0, 0)
)

l5 = 10
r1 = 10
r2 = 10
table_dr = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, AJOINT, PRISMATIC_JOINT,
        -pi/2, 0, -pi/2, 0, -pi/2, r1),
    (1, 0, AJOINT, PRISMATIC_JOINT,
        0, 0, pi/2, 0, pi/2, r2),
    (2, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, l5),
    (3, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, -l5),
    (4, 0, PJOINT, FIXED_JOINT,
        -0.5, 0, 0, -10, 0, 0)
)


table_inner_loop = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 0, FIXED_JOINT,
        0, 0, 0, 0, 0, 0),              # 1
    (1, 0, AJOINT, REVOLUTE_JOINT,
        0, 0, 0, 0, 0, 0),              # 2
    (2, 0, PJOINT, REVOLUTE_JOINT,
        pi/2, 0, 0, 100, 0, 0),         # 3
    (3, 0, PJOINT, REVOLUTE_JOINT,
        pi/4, 0, 0, 100, 0, 0),         # 4
    (1, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 5
    (5, 0, PJOINT, REVOLUTE_JOINT,
        pi/4, 0, 0, 100, 0, 0),         # 6
    (3, 0, PJOINT, REVOLUTE_JOINT,
        0, 0, 0, 100, 0, 0),            # 7
    (4, 0, PJOINT, REVOLUTE_JOINT,
        -pi/4, 0, 0, 100, 0, 0),        # 8
    (5, 7, 0, FIXED_JOINT,
        pi/2, 0, 0, 100, 0, 0),         # 9
    (6, 8, 0, FIXED_JOINT,
        pi/4, 0, 0, 100, 0, 0)          # 10
)