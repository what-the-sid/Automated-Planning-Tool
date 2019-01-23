# Automated-Planning-Tool

The goal of the practical sessions is to implement a planning tool. This tool will take as input the fragment of PDDL that is used in planning competitons 1 . It will use the A* algorithm to solve planning problems. One heuristic has to be implemented. You will have to evaluate the efficiency of your implementation.

# Work to be done

## Reading PDDL file
As a first step you have to implement a tool that can read a PDDL file written with the subset of PDDL that involves STRIPS, action costs, negative preconditions, and conditional effects. This tool should output (in any format you like) a grounded version of the planning problem given in input as a PDDL file.

## A* algorithm
As a second step you have to implement the A* algorithm (for the moment, just use a trivial heuristic, for example the one that associates an estimated cost of 0 to each state). The algorithm should run on the grounded version of a planning problem obtained with the tool you developed at first step (in fact,ideally, the problem should be grounded on-the-fly, grounding operators and atoms only when needed). At the end you should have a single tool that takes as input a planning problem described as PDDL files and outputs a cost-optimal plan for this problem. Your tool should run on any benchmark from the IPC 2018 

## Heuristic
As a third step, you should implement one of the heuristics studied during lectures and use it with your implementation of A star. You have to do it alone, and you must implement a different heuristic than the other members of the group with which you developed your tool. It is certainly a good idea to read the paper on the heuristic you choose (references are given in the lecture slides, ask me if you do not find a paper).

##  Evaluation of the efficiency of your tool
Finally, you have to evaluate the efficiency of your tool. You should propose (and justify) an evaluation protocol and apply it (you can take inspiration from the planning competitions). You should also compare the different heuristics that have been implemented in your group.