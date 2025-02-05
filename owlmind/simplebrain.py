##
## OwlMind - Platform for Education and Experimentation with Generative Intelligent Systems
## simplebrain.py :: Rule-Based Bot engine with simple deliberation process.
##
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

import csv
from .agent import Plan
from .botengine import BotBrain, BotMessage

class SimpleBrain(BotBrain):
    """
    SimpleBrain provide s avery simple Rule-based message processing from a list of predefined plans (Rules).

    Methods:
        load(file_name):
            Loads plans from a CSV file. Each row in the file should contain conditions as columns (excluding 'action') and an 'action' column specifying the associated action.
            See example for the CVS format in the method documentation.

        process(context):
            Processes a BotMessage context, matches it against the loaded plans, and assigns a response based on the best match.
    """
    VERSION = "1.2"

    def __init__(self, id):
        super().__init__(id)
        self += Plan(condition={'message':'_'}, action='I have no idea how to respond!')
        return 

    def load(self, file_name):
        """
        Load plans from a CSV file.

        The CSV file should have a structure where:
            Header defines the FIELDS for matching and a column named 'response'
            Each line contains the RgEx for matching the FIELD and the RESPONSE for that Rule.
        
        Where the FIELDS available include:

        server_name     : Server name (or '#dm' for direct message)
        channel_name    : Channel name (or '#dm' for DM)
        thread_name     : Thread name (empty if no thread)
        author_name     : Author name (username)
        author_fullname : Author full name (global_name)
        message         : Message content

        Example of CSV file:

        message, response
        *hello*, Hi there!
        *hello*, Hello!
        *, I dont know how to respond to this message.

        """
        row_count = 0
        try:
            with open(file_name, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader((row for row in file if row.strip() and not row.strip().startswith('#')), escapechar='\\')
                for row in reader:
                    condition = {"message" : row["message"].strip()}
                    response = row["response"].strip()
                    self += Plan(condition=condition, action=response)
        except FileNotFoundError:
            if self.debug: print(f'SimpleBrain.load(.): ERROR, file {file_name} not found.')

        ## Update announcement
        self.announcement = f'SimpleBrain {self.id} loaded {row_count} Rules from {file_name}.'
        return 

    def process(self, context:BotMessage):
        """
        Simplified logic to process incoming messages.
        When the message (Context) matches any plan (Rules), collect the top-matching result.
        """
        if context['message'].startswith('/instructions'):
            context.response = f'Version: {SimpleBrain.VERSION}\n'
            context.response += f'I have {len(self.plans)} plans.\n\n'
            plan_str : str = str(self.plans)
            context.response += plan_str[0:1500]

        elif context in self.plans:
            if self.debug: print(f'SimpleBrain: response={context.best_result}, alternatives={len(context.all_results)}, score={context.match_score}')
            if self.is_action(context.best_result):
                context.response = f'it should be an action here: {context.best_result[0], context.best_result[1]}'
            else: 
                context.response = context.best_result
        else:
            context.response = "(DEFAULT) There are no Rules matching this request"
        return 



