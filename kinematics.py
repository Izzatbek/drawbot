#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Gael Ecorchard <galou_breizh@yahoo.fr>             *
#*          Contributor: Izzatbek Mukhanov <izzatbek@gmail.com             *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__ = "DrawBot v 1.0 beta - Symoro+"

from joint import Joint
from loop_solver import LoopSolver

def table_ok(table):
    # Comparator function to order according to the antecedant index,
    # which is the first element in a joint description of the table
    # notation.
    cmp_antc = lambda j1, j2: cmp(j1[0], j2[0])
    sorted_table = sorted(table, cmp=cmp_antc)
    return (sorted_table == list(table))

def get_joints_from_table(table):
    joints = []
    if not(table_ok):
        raise ValueError('Antecedants should be sorted in the table')
    for j, row in enumerate(table):
        if (row[0] == 0):
            antc = None
        else:
            antc = joints[row[0] - 1]
        if (row[1] == 0):
            sameas = None
        else:
            sameas = joints[row[1] - 1]
        jnt = Joint(
                j=j + 1,
                antc=antc,
                sameas=sameas,
                mu=row[2],
                sigma=row[3],
                gamma=row[4],
                b=row[5],
                alpha=row[6],
                d=row[7],
                theta=row[8],
                r=row[9],
                )
        joints.append(jnt)
    # TODO: add recursion detection for antecedants
    return joints

class Kinematics():
    def __init__(self, table, base_t=None, tool_t=None):
        self.table = table
        if base_t is None:
            self.base_t = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
        else:
            self.base_t = base_t
        if tool_t is None:
            self.tool_t = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
        else:
            self.tool_t = tool_t
        self.joints = get_joints_from_table(self.table)
        # List of actuated joints
        self.ajoints = self.get_ajoints()
        # List of passive joints
        self.pjoints = self.get_pjoints()
        # List of moving joints
        self.mjoints = self.get_mjoints()
        # List of cut joints (With Virtual ones)
        self.cjoints = self.get_cjoints()

        from numpy import inf
        self.ub_prismatic = inf
        self.solver = LoopSolver(self.joints, self.pjoints, self.mjoints)

        # List of transformation matrices from the base
        self.transforms = []
        from numpy import identity
        for i in range(len(self.joints)):
            self.transforms.append(identity(4))

    def get_ajoints(self):
        """Return the list of active joints, always in the same order"""
        ajoints = []
        for jnt in self.joints:
            if (jnt.isactuated()):
                ajoints.append(jnt)
        return ajoints

    def get_pjoints(self):
        """Return the list of passive joints, always in the same order"""
        pjoints = []
        for jnt in self.joints:
            if (jnt.ispassive()):
                pjoints.append(jnt)
        return pjoints

    def get_cjoints(self):
        """Return the list of cut joints, always in the same order"""
        cjoints = []
        for jnt in self.joints:
            if not(jnt.sameas is None):
                cjoints += [jnt.sameas, jnt]
        return cjoints

    def get_q(self, index=None):
        """Returns the list of joint variables of active joints"""
        if (index is None):
            return [jnt.q for jnt in self.ajoints]
        else:
            return self.ajoints[index].q

    def get_mjoints(self):
        """Return the list of cut joints, always in the same order"""
        return [jnt for jnt in self.joints if not jnt.isfixed()]

    def set_q(self, q, index=None):
        if (index is None):
            index = range(len(self.ajoints))
        try:
            self.ajoints[index].q = q
        except (AttributeError, TypeError):
            for i in index:
                self.ajoints[i].q = q[i]

    def random_qm(self):
        from math import pi
        from random import uniform
        for i, jnt in enumerate(self.mjoints):
            (lb, ub) = (-pi, pi) if jnt.isrevolute() else (0, self.ub_prismatic)
            jnt.q = uniform(lb, ub)

    def get_joint_transforms(self, solve_loops=True):
        """Return the joint frame calculated from the base"""
        from numpy import dot
        cost = 0
        if solve_loops:
            cost = self.solver.solve()
        for i, jnt in enumerate(self.joints):
            if jnt.antc:
                self.transforms[i] = dot(self.transforms[self.joints.index(jnt.antc)], jnt.T)
            else:
                self.transforms[i] = jnt.T
        return self.transforms, cost

    def get_last_joints_indices(self):
        """Return indices of the joints which are not antecedents of others"""
        indices = []
        antcs = [jnt.antc for jnt in self.joints]
        for i, jnt in enumerate(self.joints):
            if not (jnt in antcs or jnt in self.cjoints):
                indices.append(i)
        return indices

    def is_last_joint(self, joint):
        antcs = [jnt.antc for jnt in self.joints]
        return not (joint in antcs or joint in self.cjoints)

    def contains_loops(self):
        return len(self.cjoints) != 0

    def set_ub(self, ub_prismatic):
        self.solver.set_ub(ub_prismatic)
        self.ub_prismatic = ub_prismatic

    def find_random(self, max_cost):
        self.solver.find_random(max_cost)

    def find_close(self):
        self.solver.find_close()