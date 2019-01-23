#!/usr/bin/env python3
import sys
import pprint
import re

def neg(effect):
    return (-1, effect)

class Action(object):
    def __init__(self, name, parameters=(), preconditions=(),add_effects=(),del_effects=(),
                 unique=False, no_permute=False):
        self.name = name
        if len(parameters) > 0:
            self.types, self.arg_names = zip(*parameters)
        else:
            self.types = tuple()
            self.arg_names = tuple()
        for i in del_effects:
            add_effects.append(neg(i))

        self.preconditions = preconditions
        self.effects = add_effects
        self.unique = unique
        self.no_permute = no_permute

        def ground(self, *args):
            return _GroundedAction(self, *args)

        def __str__(self):
            arglist = ', '.join(['%s - %s' % pair for pair in zip(self.arg_names, self.types)])
            return '%s(%s)' % (self.name, arglist)

# class Action:
#
#     def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects, cost = 0):
#         self.name = name
#         self.parameters = parameters
#         self.positive_preconditions = positive_preconditions
#         self.negative_preconditions = negative_preconditions
#         self.add_effects = add_effects
#         self.del_effects = del_effects
#         self.cost = cost

    # def __str__(self):
    #     return 'action: ' + self.name + \
    #     '\n  parameters: ' + str(self.arg_names) + \
    #     '\n  positive_preconditions: ' + str(self.preconditions) + \
    #     '\n  effects: ' + str(self.effects)
    #
    # def __eq__(self, other):
    #     return self.__dict__ == other.__dict__

class PDDL_Parser:

    # ------------------------------------------
    # Tokens
    # ------------------------------------------

    def scan_tokens(self, filename):
        '''
        Scan the entire PDDL file and store in the form of list
        '''
        # open PDDL file and convert into lower case
        with open(filename,'r') as f:
            str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()
        # Tokenize
        stack = []
        list = []
        # iterate throught the entire PDDL file
        for t in re.findall(r'[()]|[^\s()]+', str):
            # append temp list from open parantheses
            if t == '(':
                stack.append(list)
                list = []
            # pop temp list and append to main list
            elif t == ')':
                if stack:
                    l = list
                    list = stack.pop()
                    list.append(l)
                else:
                    raise Exception('Missing open parentheses')
            else:
                list.append(t)
        if stack:
            raise Exception('Missing close parentheses')
        if len(list) != 1:
            raise Exception('Malformed expression')
        return list[0]

    #-----------------------------------------------
    # Parse domain
    #-----------------------------------------------

    def parse_domain(self, domain_filename):
        tokens = self.scan_tokens(domain_filename)
        if type(tokens) is list and tokens.pop(0) == 'define':
            self.domain_name = 'unknown'
            self.actions = []
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if   t == 'domain':
                    self.domain_name = group[0]
                elif t == ':requirements':
                    pass # TODO
                elif t == ':predicates':
                    pass # TODO
                elif t == ':action':
                    self.parse_action(group)
                else: print(str(t) + ' is not recognized in domain')
        else:
            raise 'File ' + domain_filename + ' does not match domain pattern'

    #-----------------------------------------------
    # Parse action
    #-----------------------------------------------

    def parse_action(self, group):
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Action without name definition')
        for act in self.actions:
            if act.name == name:
                raise Exception('Action ' + name + ' redefined')
        parameters = []
        positive_preconditions = []
        negative_preconditions = []
        add_effects = []
        del_effects = []
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = group.pop(0)
            elif t == ':precondition':
                self.split_propositions(group.pop(0), positive_preconditions, negative_preconditions, name, ' preconditions')
            elif t == ':effect':
                self.split_propositions(group.pop(0), add_effects, del_effects, name, ' effects')
            else: print(str(t) + ' is not recognized in action')
        self.actions.append(Action(name, parameters, positive_preconditions, add_effects, del_effects))

    #-----------------------------------------------
    # Parse problem
    #-----------------------------------------------

    def parse_problem(self, problem_filename):
        tokens = self.scan_tokens(problem_filename)
        if type(tokens) is list and tokens.pop(0) == 'define':
            self.problem_name = 'unknown'
            self.objects = []
            self.state = []
            self.positive_goals = []
            self.negative_goals = []
            while tokens:
                group = tokens.pop(0)
                t = group[0]
                if   t == 'problem':
                    self.problem_name = group[-1]
                elif t == ':domain':
                    if self.domain_name != group[-1]:
                        raise Exception('Different domain specified in problem file')
                # elif t == ':requirements':
                #     pass # TODO
                elif t == ':objects':
                    group.pop(0)
                    self.objects = group
                elif t == ':init':
                    group.pop(0)
                    self.state = group
                elif t == ':goal':
                    self.split_propositions(group[1], self.positive_goals, self.negative_goals, '', 'goals')
                else: print(str(t) + ' is not recognized in problem')

    #-----------------------------------------------
    # Split propositions
    #-----------------------------------------------

    def split_propositions(self, group, pos, neg, name, part):
        if not type(group) is list:
            raise Exception('Error with ' + name + part)
        if group[0] == 'and':
            group.pop(0)
        else:
            group = [group]
        for proposition in group:
            if proposition[0] == 'not':
                if len(proposition) != 2:
                    raise Exception('Unexpected not in ' + name + part)
                neg.append(proposition[-1])
            else:
                pos.append(proposition)

class _GroundedAction(object):
    """
    An action schema that has been grounded with objects
    """
    def __init__(self, action, *args):
        self.name = action.name
        ground = _grounder(action.arg_names, args)

        # Ground Action Signature
        self.sig = ground((self.name,) + action.arg_names)

        # Ground Preconditions
        self.preconditions = list()
        self.num_preconditions = list()
        for pre in action.preconditions:
            if pre[0] in NUM_OPS:
                operands = [0, 0]
                for i in range(2):
                    if type(pre[i + 1]) == int:
                        operands[i] = pre[i + 1]
                    else:
                        operands[i] = ground(pre[i + 1])
                np = _num_pred(NUM_OPS[pre[0]], *operands)
                self.num_preconditions.append(np)
            else:
                self.preconditions.append(ground(pre))

        # Ground Effects
        self.add_effects = list()
        self.del_effects = list()
        self.num_effects = list()
        for effect in action.effects:
            if effect[0] == -1:
                self.del_effects.append(ground(effect[1]))
            elif effect[0] == '+=':
                function = ground(effect[1])
                value = effect[2]
                self.num_effects.append((function, value))
            elif effect[0] == '-=':
                function = ground(effect[1])
                value = -effect[2]
                self.num_effects.append((function, value))
            else:
                self.add_effects.append(ground(effect))

    def __str__(self):
        arglist = ', '.join(map(str, self.sig[1:]))
        return '%s(%s)' % (self.sig[0], arglist)
