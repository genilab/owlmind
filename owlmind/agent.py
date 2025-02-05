##
## OwlMind - Platform for Education and Experimentation with Generative Intelligent Systems
## agent.py :: Core Agent structure 
## 
## These components implement Context-Aware Reasoning and Rule Base Inference
## at the core of Agent-based systems.
#  
# Copyright (c) 2024 Dr. Fernando Koch, The Generative Intelligence Lab @ FAU
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Documentation and Getting Started:
#    https://github.com/GenILab-FAU/owlmind
#
# Disclaimer: 
# Generative AI has been used extensively while developing this package.
# 

from collections import deque
from .context import Context, ContextRecord, ContextRepo

class Belief(Context):
    def __init__(self, facts):
        super().__init__(facts=facts)
        return
    pass

class Command(Context):
    def __init__(self, goal=None, context=None):
        super().__init__(namespace=goal, facts=context)
        return
    pass

class Plan(ContextRecord):
    CUT = '!!'
    def __init__(self, action, goal=None, condition=None):
        super().__init__(condition=condition, action=action, goal=goal)
        return
    pass

class PlanBase(ContextRepo):
    def __init__(self):
        super().__init__(valid_class=Plan)
        return
    pass

class Capability(ContextRecord):
    def __init__(self, goal:str, action, condition:Context=None):
        goal = '@'+goal if not goal.startswith('@') else goal 
        super().__init__(condition=condition, action=action, goal=goal)
        return
    pass

class CapabilityBase(ContextRepo):
    def __init__(self):
        super().__init__(valid_class=Capability)
        return
    pass
    
class Agent():
    """
    Implements the core functionality in Rule-based Agentic systems.
    Agents are components that Sense -> Deliberate -> Act.
    In this component, Deliberate is implemented through Rule-based deliberation, that is:
        - Receives a Command with a gola and local Context (parameters)
        - Deliberate about rules that could process that Command
        - Execute the Actions (=Capabilities) related to these Rules
        
    Actions can be:
        - internal actions such as 'learn new Belief', 'learn new Rule', forget X, etc
        - external actions, implement throgh functional calling
        - communication actions, sending messages to other agents.

    Internal structures include:
        Beliefs: Belief Base, storing Agent's long-term Memory, used during Deliberation.
        Plans: Rule Base, storing Deliberation Rules as 'goal({condition})->{action}'.
        Capabilites: Capability Base, cataloguing Actions.
    
    @EXAMPLE
    How to use this class

    ag = Agent(id='ag-1')

    ag += Capability(goal = 'print', action=print)

    ag += Belief(facts = {'code'    : 'need to define code', 
                         'title'    : 'need to define title',
                         'logo'     : 'cen-logo.png'})
    
    ag += Plan(goal = 'print_code',
               condition = {'code': '*'},
               action = '@print($code)')
    
    ag += Command(goal='print_code', parameters={'code' : 'COT6930'})
    ag.run()

    """

    DEBUG : bool = False
    STEPS : int  = 100
    BASE : str = None

    def __init__(self, id):
        """
        Initialization
        param: id as agent identifier.
        """
        self.id = id
        self.beliefs = Context()
        self.plans = PlanBase()
        self.capabilities = CapabilityBase()
        self._current_command : Command = None
        self._delib_queue : deque = deque()
        self._action_queue : deque = deque()
        return 
    
    def __iadd__(self, knowledge):
        """ 
        Add knowledge to internal structures
        """
        if isinstance(knowledge, Plan):
            self.plans += knowledge
        elif isinstance(knowledge, Capability):
            self.capabilities += knowledge
        elif isinstance(knowledge, Command):
            self._delib_queue.append(knowledge)
        elif isinstance(knowledge, Belief) or isinstance(knowledge, dict):
            self.beliefs += knowledge
        else:
            if Agent.DEBUG: print(f'Agent({self.id}).learn: received unnaceptable knowledge type, {type(knowledge)}')
        return self        

    def __repr__(self):
        """ Return string representation """
        return f'{self.__class__.__name__}({self.id})[beliefs={len(self.beliefs)}, plans={len(self.plans)}, capabilities={len(self.capabilities)}]'


    ##
    ## DELIBERATION LOGIC
    ##

    @staticmethod
    def is_action(goal): 
        return (isinstance(goal, str) and goal.startswith('@')) or \
               (isinstance(goal, tuple) and goal[0].startswith('@'))
    
    def deliberate(self):
        """ 
        Deliberation process
        """

        #
        # (1) Execute 'Requests for Deliberation' (Commands) in the deliberation queue

        while self._delib_queue:
            cmd : Command = self._delib_queue.popleft()
            self._local_context = cmd
            goal = cmd.namespace

            if Agent.is_action(goal):
                goal = self.beliefs.compile(sentence=goal)
                self._action_queue.append(goal)
            elif cmd in self.plans:
                for action, weight in cmd.result:
                    self += Command(goal=action, context=self._local_context)
            else:
                if Context.DEBUG: print(f'Agent.run(): there are no Plans for this Command, {cmd}')

        #
        # (2) Execute 'Requests to Act' (Actions) in the action queue, if any
        
        while self._action_queue:
            action, params = self._action_queue.popleft()
            print('--->', action)
        return 
    
    def process(self, goal=None, context=None):
        """
        Deliberate about a Goal within an specific Context
        """
        self += Command(goal=goal, context=context)
        self.deliberate()
        return
    

###
### DEBUG
### 
from pprint import pprint

def process(context):
    print('Here!')

if __name__ == "__main__":
    import random

    ag = Agent(id='ag-1')
    ag += Capability(goal='@print', action=print)
    ag += Capability(goal='@process', action=process)

    ag.process(goal=('@print', 'Hello World!'))





    
    