#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Gael Ecorchard <galou_breizh@yahoo.fr>             *
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

from chain import Chain

def remove_upto_root(chain, root):
    """Remove all joints before root and root itself in a chain"""
    for jnt in chain:
        if not(jnt is root):
            chain.pop(0)
        else:
            break
    # Also remove root
    chain.pop(0)

def get_looproot(joints, joint):
    """Return the loop root for loop ending at joint

    Argument 2, joint, must be the end joint with non-None sameas attribute.
    The loop root is the last common joints of the two subchains ending at,
    respectively joint and joint.sameas.
    """
    chain = Chain(joints)
    subchain1 = chain.get_subchain_to(joint)
    subchain2 = chain.get_subchain_to(joint.sameas)

    #returns the first common antecedant for both loops
    for jnt in subchain2[::-1]:
        if (jnt in subchain1):
            return jnt
    return None

def get_loops(joints):
    """Returns a list of tuples with roots and ends (cut joints) of loops"""
    ends = []
    roots = []
    for jnt in joints:
        # If jnt's sameas attribute is another joint and that this latter is
        # not already in the list of end joints, add jnt.
        end = jnt.sameas
        if (not(end is None) and
                not(end in ends)):
            ends += [end, jnt]
            root = get_looproot(joints, jnt)
            roots += [root, root]
    return zip(roots, ends)

class LoopSolver():
    def __init__(self, joints, pjoints, mjoints):
        self.joints = joints
        self.pjoints = pjoints
        self.mjoints = mjoints
        from numpy import inf
        self.ub_prismatic = inf

        # Chains
        self.chain = Chain(self.joints)
        self.loops = get_loops(self.joints)

        #self.end_joints = self.get_end_joints()
        self.chains = self.get_chains()

    def get_qm(self, index=None):
        """Returns the list of joint variables of moving joints"""
        if (index is None):
            return [jnt.q for jnt in self.mjoints]
        else:
            return self.mjoints[index].q

    def get_qp(self, index=None):
        """Returns the list of joint variables of passive joints"""
        if (index is None):
            return [jnt.q for jnt in self.pjoints]
        else:
            return self.pjoints[index].q

    def set_qp(self, q):
        """Sets the joint variables of passive joints"""
        for i, jnt in enumerate(self.pjoints):
            jnt.q = q[i]

    def set_qm(self, q):
        """Sets the joint variables of moving joints"""
        for i, jnt in enumerate(self.mjoints):
            jnt.q = q[i]

    def get_end_joints(self):
        """Return the list of self.end and all joints with sameas == end."""
        ends = []
        for start, end in self.loops:
            l = ([end] +
                [jnt for jnt in self.joints if jnt.sameas is end])
            ends += l
        return ends

    def get_chains(self):
        """Return a list of serial chains constituting the mechanism

        Each serial chain starts with the joint following self.root and
        ends with self.end or a joint with sameas == self.end.
        """
        chains = []
        for root, end in self.loops:
            subchain = self.chain.get_subchain_to(end)
            remove_upto_root(subchain, root)
            chains.append(subchain)
        return chains

    def J(self, x):
        """Returns the squared difference of transformation matrices
        calculated from the common root for 2 chains of a loop as a cost function
        Is calculated for each loop at the same time."""
        from numpy import identity
        from numpy import dot, sum

        J = 0
        matrices = []
        for chain in self.chains:
            T = identity(4)
            for jnt in chain:
                T = dot(T, jnt.T)
            matrices.append(T)

        # There are 2 chains for each loop starting as transformation matrix from the common joint
        for i in range(0, len(matrices), 2):
            J += sum((matrices[i] - matrices[i+1])**2)
        return J

    def least_J(self, x):
        from numpy import identity
        from numpy import dot

        J = 0
        matrices = []
        for chain in self.chains:
            T = identity(4)
            for jnt in chain:
                T = dot(T, jnt.T)
            matrices.append(T)

	    from numpy import zeros
	    dy = zeros(12 * (len(matrices) // 2))
        for i in range(0, len(matrices), 2):
            dy[(i // 2) * 12: ((i // 2) + 1) * 12] = ((matrices[i][:3, :] - matrices[i+1][:3, :])**2).flatten()
        return dy

    def cost(self, x):
        self.set_qp(x)
        return self.J(x)

    def set_ub(self, ub_prismatic):
        self.ub_prismatic = ub_prismatic

    def solve(self):
        if len(self.pjoints) == 0:
            return
        from numpy import array
        from scipy.optimize import minimize
        qs = self.get_qp()
        x0 = array(qs)
        #bounds = self.set_bounds(self.pjoints)
        obj = minimize(self.cost, x0, tol=1e-7, method='L-BFGS-B')#, bounds=bounds)
        x = obj.x
        self.set_qp(x)
        return obj.fun

    def cost_all(self, x):
        self.set_qm(x)
        return self.J(x)

    def set_bounds(self, jnts):
        from math import pi
        bounds = []
        for i, jnt in enumerate(jnts):
            b = (-pi, pi) if jnt.isrevolute() else (0, self.ub_prismatic)
            bounds.append(b)
        return bounds

    def find_close(self):
        """Finds a solution by including active joints into optimization problem"""
        from numpy import array
        from scipy.optimize import minimize
        qs = self.get_qm()
        x0 = array(qs)
        #bounds = self.set_bounds(self.mjoints)
        obj = minimize(self.cost_all, x0, tol=1e-7, method = 'L-BFGS-B')
        x = obj.x
        self.set_qm(x)
        return obj.fun

    def find_random(self, max_cost):
        """Finds a solution by including active joints and initializing all the joints randomly"""
        from numpy import array
        from scipy.optimize import minimize
        qs = self.get_qm()
        x0 = array(qs)
        bounds = self.set_bounds(self.mjoints)
        from random import uniform
        for j in range(10):
            for i, jnt in enumerate(self.mjoints):
                x0[i] = uniform(bounds[i][0], bounds[i][1])
            obj = minimize(self.cost_all, x0, tol=1e-7, method = 'L-BFGS-B')
            if obj.fun < max_cost:
                break
        x = obj.x
        self.set_qm(x)
        return obj.fun