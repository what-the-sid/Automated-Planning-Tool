#!/usr/bin/env python3
import sys
import pprint
from parser import Action
# from parser import PDDL_Parser
from pddl_parser import PDDL_Parser
# from planner import Astar_planner
# from Astar import Astar
from planner import *

if __name__ == "__main__":
    '''
    PDDL to list
    '''
    # problem = "./PDDL/problem1.pddl"   #contains init and goal states
    # domain = "./PDDL/domain_1.pddl"       #contains problme description
    domain = "./PDDL/domain_2.pddl"   #contains init and goal states
    problem = "./PDDL/problem2.pddl"       #contains problme description
    parser = PDDL_Parser(domain_file = domain, problem_file = problem)
    plan = planner(parser,verbose=True)
    for action in plan:
        print(action)
