##
## OwlMind - Platform for Education and Experimentation with Generative Intelligent Systems
## context.py :: Context Represenation, Contextualized Record, and Contextualized Store.
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
# Documentation:
#    https://github.com/GenILab-FAU/owlmind
#
# Disclaimer: 
# Generative AI has been used extensively while developing this package.
# 

import re
import random
from collections.abc import Iterable

class Context(dict):
    """
    Context representation as a group of facts (key:value).

    @EXAMPLE
    How to use this class

    # Create from dict or add new facts
    c = Context({'code':'3333', 'name': 'FK'})
    c['other'] = 'new value'
    c += {'example': ['e1','e2']}
    print(c['code'])

    # Context match (does test exists with Context?)
    test = Context({'code': '*3'})
    if test in c:
        print(test.result)

    # String compilation
    print(c.compile('Hello $code and $name'))

    @REQUIRED
    @TODO must be able to match values of different types (https://github.com/GenILab-FAU/owlmind/issues/6)
    @TODO must be able to handle sub-context e.g. namespace/subkey/sub-subkey (https://github.com/GenILab-FAU/owlmind/issues/7)
    """

    _ = '_' # wildcard flag
    MAX_CLAUSE = 100.0
    CASE_SENSITIVE = False
    DEBUG = True

    def __init__(self, facts=None, namespace=None):
        """
        Init Context
        param: facts as dict, str, list, or tuple
        """
        self.namespace = namespace
        self.result = None
        if facts:
            self.__iadd__(facts=facts)
        return

    def __hash__(self):
        """
        Return hash value
        """
        return hash(tuple(sorted(self.items())))

    def __getitem__(self, key:str):
        """
        Overload __getitem__; if key not in super().dict, return None
        """
        return super().get(key, None)
    
    def __iadd__(self, facts:dict):
        """
        Add one or more new facts.
        params: facts:dict if not dict, add under Context._
        """
        self.hash = None
        if facts and isinstance(facts, dict):
            self.update(facts)
        elif Context.DEBUG: 
            print(f'ERROR: Context.__iadd__: fact is missing or invalid type, {type(facts)}')
        return self
    
    def __contains__(self, test:dict) -> bool:
        """
        Context-mathcing logic.
        This is the key logic behind Context-matching and ContextRepos for the whole 
        implementation.

        The process matches Context-keys from test-Context and this Context as:
        - Exact-match, when the two strings are the same (not-context sensitive)
        - Wildcard-match with '*' or '_'
        - Star-matching for *value, value*, *value*
        - Regex-matching for r/regex/
        - Match-score increases the more content is matched
        """
        # TODO : Overall I think the logic here is very bloated for what it's trying to do, and I'm fairly certain
        # this entire method could be refactored to be both more readable and concise. 

        # CUT-SHORT conditions
        if not test or not isinstance(test, Context):
            if Context.DEBUG: print(f'WARNING: Context.__contains__, test must be Context: {type(test)}')
            return False
        test.result = None

        # Processing
        match_score = 0.0
        match_subs = {}
        cut = True # it thinks it will CUT, unless proven otherwise
        
        # @NOTE heuristic for key-value match rate
        for key, value in test.items():
            if super().__contains__(key):

                # Setup parameters
                local_score = Context.MAX_CLAUSE 
                target = self[key] if Context.CASE_SENSITIVE else self[key].lower()
                value_str = isinstance(value, str)
                # why bother checking if the type is a string, if you're just going to call a string method on it anyways?
                value = value if value_str and Context.CASE_SENSITIVE else value.lower()

                # (2) Process context-match

                # @TODO it should test for type() here and have different logics for str/str, int/int, list/list, and combinations.

                # (2.1) Exact value-match
                if target == value: 
                    local_score += 1.0 

                # (2.2) Wildcard match
                elif value == Context._ or (value_str and value == '*'): 
                    local_score += 0.25

                 # (2.3) Start-matching
                elif value_str and (value.startswith('*') or value.endswith('*')):
                    begin_with = value.endswith('*')
                    stripped_value = value.strip('*')
                    target_value = str(target)
                    if (begin_with and target_value.startswith(stripped_value)) or \
                        target_value.endswith(stripped_value):
                        # @NOTE proximity calculation in Star-match
                        local_score += 0.50 + (0.49 * (len(stripped_value) / len(target_value))) 

                # (2.4) regex matching with r/regex/
                elif value_str and value.startswith('r/'): 
                    pattern = value[2:-1] if value.endswith('/') else value[2:] 
                    try:
                        # TODO : I'm almost certain fullmatch() isn't the method we want to use here for partial matching with regex as fullmatch needs to match the entire target.
                        if re.fullmatch(pattern, str(target)):
                            # @NOTE arbitrary value for regex-matching
                            local_score += 0.75 
                    except re.error:
                        if Context.DEBUG: print(f'WARNING: Context.__contains__, regex expection: {pattern}')
                        continue
            
                # if there was a value-match, annotate; otherwise CUT
                if local_score > Context.MAX_CLAUSE:
                    match_subs[key] = self[key]
                    match_score += local_score
                else: 
                    break

            ## CUT if key does not exist in target
            else: 
                break
        ## For-loop-else will happen in case Context-match was not CUT
        ## note: this proves the initial belief to be false
        # TODO : Remove for-else construct, this is not idiomatic python, use flags instead
        else: 
            cut = False 

        # (3) Load (or reset) Context-match values 
        if not cut:
            test.result = match_subs
            test.score = match_score
        
        return bool(test.result)
    
    @staticmethod
    def _compile(sentence: object, subs: dict):
        result = ""
        if isinstance(sentence, (list, tuple, set)):
            result = tuple(Context._compile(sentence=element, subs=subs) for element in sentence)
        elif isinstance(sentence, str):
            result = re.sub(r"\$(\w+)", lambda match: str(subs.get(match.group(1), match.group(0))), sentence)
        return result
    
    def compile(self, sentence):
        """ 
        Compile a sentence (str or sequence of strings) replacing variables marked as $var_id with values from this Context.
        Examaple: 
            context = {'code': '33344', 'name': 'FK', ...}
        
            context.compile('code: $code') -> 'code 33344'
            context.compile(['My name is $name'], ['I am working at room $code']) -> \
                ('My name is FK', 'I am working at room 33344')
        """
        return Context._compile(sentence=sentence, subs=self)

###
### CONTEXTUALIZED ELEMENT
### 

class ContextRecord():
    """
    Contextualized Records to be used with ContextRepo.
    They represent goal({condition})->{action} structures, which can be used e.g. in Rule Base Stores.
    """
    def __init__(self, condition, action, goal:str = None):
        self.namespace : str = goal if goal else Context._
        self.context : Context = condition if isinstance(condition,Context) else Context(condition)
        self.action : list = action
        return 

    def __hash__(self):
        result = ''
        for field in [self.namespace, self.context, self.action]:
            #result = hash( (result, tuple(field) if field and isinstance(field, Iterable) else '_' ))
            result = hash((result, field.__hash__)) 
        return result
 
    def __repr__(self):
        return f'{self.__class__.__name__}({self.context}, {self.action})'
    

###
### CONTEXTUALIZED REPO
###

class ContextRepo():
    """
    Store of Contextualized Records.
    
    @EXAMPLE
    How to use this class:

    cr = ContextRepo()
    cr += ContextRecord(condition={'code':'*'}, action=('@print','$code'))
    cr += ContextRecord(condition={'name':'*'}, action=('@print','$name'))

    s = Context({'code':'3333', 'name': 'FK'})
    if s in cr:
        print(s.result)

    """
    def __init__(self, valid_class=ContextRecord):
        self.valid_class = valid_class
        self._lenght = 0
        self._repo = dict()
        return 
   
    def __len__(self):
        return self._lenght
    
    def __iadd__(self, obj):
        """
        Adds an object to the repository.
        """

        # CUT-SHORT conditions
        if not obj:
            return self
        elif not isinstance(obj, self.valid_class):
            raise ValueError(f'ContextRepo.__iadd__: invalid type for {self.__class__.__name__}, type {type(obj)}')
        
        # Processing
        namespace = getattr(obj, 'namespace', Context._) or Context._
        obj_hash = hash(obj)
        
        if namespace not in self._repo:
            self._repo[namespace] = dict()

        if obj_hash not in self._repo[namespace]:
            self._repo[namespace][obj_hash] = obj
            self._lenght+=1
        else:
            if Context.DEBUG: print(f'ContextRepo.__iadd__: obj already in the store {self.__class__.__name__}, {self._repo[namespace][obj_hash]}')
        return self
    
    def __getitem__(self, namespace):
        """ 
        Retrieve Contextualized Records stored under a namespace 
        """
        return self._repo[namespace].values() if namespace in self._repo else None 

    def __contains__(self, target:Context):
        """
        Context-matching against ContextRepo.
        Checkes if target-Context (current-Condition) matches any test-Condition stored in Repo.
        narrows the search using test.namespace if loaded, otherwise check default to Context._
        """

        # CUT-SHORT conditions
        if target is None:
            return None
        elif not (isinstance(target, Context) or isinstance(target, str)):
            raise ValueError(f"ContextRepo.__contains__: expected Context or str, got {type(target)}")

        # Processing
        matching_plans = []

        # Consider target.{namespace_field} if loaded 
        namespace = getattr(target, 'namespace', Context._) or Context._

        # For every stored 'obj' insize {target.{namespace_field}}
        if namespace in self._repo:
            for record in self._repo[namespace].values():
                record_ctx : Context = getattr(record, 'context', Context._) or Context._

                ## @NOTE
                # Does record_ctx (test) matches the target?
                # If so, record_ctx was loaded with (check Context.__contains__):
                #               record_ctx.results : substitutions aplied during the match process
                #               record_ctx.match_score
                if record_ctx in target:
                    record.action = Context._compile(sentence=record.action, subs=record_ctx.result)
                    matching_plans.append( (record.action, record_ctx.score) )

        # Sort in descending order by score
        matching_plans.sort(key=lambda x: x[1], reverse=True)  

        # Pick among the plans with the highest ranking
        highest_score = matching_plans[0][1] if matching_plans else None
        best_plans = [plan for plan in matching_plans if plan[1] == highest_score]

        # Load Plans and random select when more than one option
        target.all_results = [plan[0] for plan in best_plans]
        target.best_result = random.choice(target.all_results) if target.all_results else None
        target.match_score = highest_score if best_plans else 0
        return len(target.all_results)


    def __repr__(self):
        """ Return string representation """
        output = []
        for namespace, PlanRules in self._repo.items():
            output.append(f"{namespace}:")
            for PlanRule in PlanRules.values():
                output.append(f"    {PlanRule}")
        return f"{self.__class__.__name__}(\n{chr(10).join(output)}\n)"

