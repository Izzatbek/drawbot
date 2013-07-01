#!/usr/bin/python
# -*- encoding: utf-8 -*-

def get_base(joints):
    """Return the base joint, i.e. joints without antecedent"""
    base = None
    for jnt in joints:
        if not(jnt.antc in joints):
		    # if antecedent is not in the joint list ==> base joint
            base = jnt
    return base

def get_tools(joints):
    """Return the end joints, i.e. joints that are antecedent of nothing"""
	# list of antecedents
    antc = [jnt.antc for jnt in joints]
    # A joint is an end joint if is antecedent of no other joints.
	# for each joint, if it is not in the antecedent list ==> end effector
    tools = [jnt for jnt in joints if not(jnt in antc)]
    return tools

def get_children(joints, joint):
    """Return a list of joints which have the given joint as antecedent"""
	# list of branches from joint
    return [jnt for jnt in joints if (jnt.antc is joint)]

def is_unique_child(joint, joints):
    """Return True is no other joint has the same antecedent"""
	# list of antecedents
    antc = [jnt.antc for jnt in joints]
	# counts number of times joint.antc occurs in the list
	#if 1, then the joint is not a branch of its antecedent
    return (antc.count(joint.antc) == 1)

# function is recursive. list starts from the base to the endeffector
def get_subchain_to(joint, joints):
    """Return the subchain ending at joint"""
    if not(joint.antc in joints):
        return [joint]
    l = []
	# recursion
    l.extend(get_subchain_to(joint=joint.antc, joints=joints))
    l.append(joint)
    return l

class Chain(object):
	# constructor: sets up the properties joints, base and tools
    def __init__(self, joints):
        self.joints = joints
        self._base = get_base(joints)
        if self._base is None:
            raise ValueError('Chain has no base joint')
        self._tools = get_tools(joints)

    @property
    def base(self):
        """The base joint, i.e. joints without antecedent"""
        return self._base

    @property
    def tools(self):
        """The end joints, i.e. joints that are antecedent of nothing"""
        return self._tools

	# recursive function
    def get_subchain_from(self, joint):
        """Return the subchain starting at joint"""
		# check how many joints are next
        subjnts = get_children(self.joints, joint)
        if (len(subjnts) == 0):
			# end effector
            return [joint]
        elif (len(subjnts) == 1):
			# serial chain: current joint + subchain from next joint
            return [joint] + self.get_subchain_from(subjnts[0])
        else:
			# in the case of braches, list section is defined as [common joint, branch1, branch2, ..]
            l = [joint]
            l.append([self.get_subchain_from(jnt) for jnt in subjnts])
            return l

    def get_subchain_to(self, joint):
        """Return the subchain ending at joint"""
        return get_subchain_to(joint=joint, joints=self.joints)

	# defines entire robot as one chain from the base
    def get_chain(self):
        return self.get_subchain_from(self.base)