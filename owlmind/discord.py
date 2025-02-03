##
## OwlMind - Platform for Education and Experimentation with Generative Intelligent Systems
## discord.py :: Bot Runner for Discord
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

import re
import discord
from .botengine import BotMessage, BotBrain

class DiscordBot(discord.Client):
    """
    DiscordBot provides logic to connect the Discord Runner with OwlMind's BotMind, 
    forming a multi-layered context in BotMessage by collecting elements of the Discord conversation
    (layer1=user, layer2=thread, layer3=channel, layer4=guild), and aggregating attachments, reactions, and other elements.

    @EXAMPLE
    How to use this class:

    brain = MyBotMind(.) # Check documentation in botmind.py
    TOKEN = {My Token}
    bot = DiscordBot(token=TOKEN, brain=MyBotMind, debug=True)
    bot.run()

    @REQUIRED
    Help needed:
    @TODO Need to collect attachments, reactions, etc. (currently only loading text)
    @TODO Need to return attachments, issue reactions, etc.
    """
    def __init__(self, token, brain:BotBrain, promiscous:bool=False, debug:bool=False):
        self.token = token
        self.promiscous = promiscous
        self.debug = debug
        self.brain = brain
        if self.brain: self.brain.debug = debug

        ## Discord attributes
        intents = discord.Intents.default()
        intents.messages = True
        intents.reactions = True
        intents.message_content = True
        #intents.guilds = True
        #intents.members = True

        super().__init__(intents=intents)
        return 

    async def on_ready(self):
        print(f'Bot is running as: {self.user.name}.')
        if self.debug: print(f'Debug is on!')
        if self.brain: 
            print(f'Bot is connected to {self.brain.__class__.__name__}({self.brain.id}).') 
            if self.brain.announcement: print(self.brain.announcement)
            self.brain.debug = self.debug
        
    async def on_message(self, message):
        # CUT-SHORT conditions
        # Only process if message does not come from itself, the bot is configured as promiscous, or this is a DM or mentions the bot
        if message.author == self.user or \
            (not self.promiscous and not (self.user in message.mentions or isinstance(message.channel, discord.DMChannel))):
           if self.debug: print(f'IGNORING: orig={message.author.name}, dest={self.user}') 
           return

        # Remove calling @Mention if in the message
        text = re.sub(r"<@\d+>", "", message.content,).strip()

        # Collect attachments, reactions and others.
        attachments = [attachment.url for attachment in message.attachments] if message.attachments else None
        reactions = [str(reaction.emoji) for reaction in message.reactions] if message.reactions else None

        # Create context
        context = BotMessage(
                layer1       = message.guild.id if message.guild else 0,
                layer2       = message.channel.id if hasattr(message.channel, 'id') else 0,
                layer3       = message.channel.id if isinstance(message.channel, discord.Thread) else 0,
                layer4       = message.author.id,
                server_name  = message.guild.name if message.guild else '#dm',
                channel_name    = message.channel.name if hasattr(message.channel, 'name') else '#dm',
                thread_name     = message.channel.name if isinstance(message.channel, discord.Thread) else '',
                author_name     = message.author.name,
                author_fullname = message.author.global_name,
                message         = text,
                attachments     = attachments,
                reactions       = reactions)

        if self.debug: print(f'PROCESSING: ctx={context}')
                              
        # Process through Brain
        if self.brain:
            self.brain.process(context)

        # If the immediate processing of Context generated a result (sync mode), return it through the bot interface
        if context.response:
            await message.channel.send(context.response)
            if context.attachments:
                for attachment in context.attachments:
                    await message.channel.send(attachment)
            if context.reactions:
                for reaction in context.reactions:
                    await message.add_reaction(reaction)
        return

    def run(self):
        super().run(self.token)
