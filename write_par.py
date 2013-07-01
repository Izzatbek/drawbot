__author__ = 'Izzat'

from visual import *
from visual.filedialog import save_file

class ParWriter:
    Ant, sameas, Mu, Sigma, gamma, B, Alpha, d, Theta, R = range(10)
    geom_par = ['Ant', 'Sigma', 'B', 'd', 'R', 'gamma', 'Alpha', 'Mu', 'Theta']

    @classmethod
    def header(c):
        return """(*******************************************)
(*                 SYMORO+                 *)
(*            DrawBot v1.0 beta            *)
(*     Numerical parameters of a robot     *)
(*                                         *)
(* Institut de Recherche en Communications *)
(*        et Cybernetique de Nantes        *)
(*                                         *)
(*            Equipe robotique             *)
(*                                         *)
(*                                         *)
(*      web: www.irccyn.ec-nantes.fr       *)
(*******************************************)
"""

    @classmethod
    def get_properties(c, table):
        """Returns NF, NL, NJ
        """
        NF = len(table)
        NJ = 0
        for row in table:
            if row[c.sameas] == 0:
                NJ += 1
        return NF, 2*NJ-NF, NJ

    @classmethod
    def get_type_string(c, table):
        """Returns type of the robot depending on
        the number of end-effectors and the number of loops
        """
        antcs = [row[c.Ant] for row in table]
        n_ends = 0
        n_B = 0
        for i, row in enumerate(table):
            if i + 1 not in antcs:
                n_ends += 1
            if row[c.sameas] != 0:
                n_B += 1
        if n_B > 0:
            return 'Type = 2 (* Closed *)\n\n'
        if n_ends > 1:
            return 'Type = 1 (* Tree *)\n\n'
        return 'Type = 0 (* Simple *)\n\n'

    @classmethod
    def geo_string(c, table):
        """Forms the output string for geometrical parameters
        """
        output = '(* Geometric parameters *)\n'
        for par in c.geom_par:
            cur = par + ' = {\n        '
            for row in table:
                cur += str(row[eval('c.'+par)]) + ','
            output += cur[:-1] + '}\n'
        return output

    @classmethod
    def par_string(c, table, file_name=None, robot_name=None):
        """Generates all the content of the file
        """
        output = c.header() + '\n'
        if file_name:
            output += '(* File ' + file_name + ' *)\n\n'
        output += '(* General parameters *)\n'
        if robot_name:
            output += '(* Robotname = \'' + robot_name + '\' *)\n'
        NF, NL, NJ = c.get_properties(table)
        output += 'NF = ' + str(NF) + '\nNL = ' + str(NL) + '\nNJ = ' + str(NJ) + '\n'
        output += c.get_type_string(table)
        output += c.geo_string(table)
        return output

    @classmethod
    def write_to_file(c, table, robot_name='Robot'):
        fd = save_file('.par')
        if fd:
            name = fd.name[fd.name.rfind('\\') + 1:]
            fd.write(c.par_string(table, name, robot_name))
            fd.close()
            return True
        return False
