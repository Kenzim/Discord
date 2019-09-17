import discord.ext.commands as commands
import json
from essentials import ensure_file_existence


class DiscordBot:
    def __init__(self, *cogs):
        ensure_file_existence("config.json")
        with open("config.json", 'r+') as config_file:
            if config_file.read():
                config_file.seek(0)
                config = json.load(config_file)
            else:
                config = {"discord_token": "none",
                          "command_prefix": "v."}
                json.dump(config, config_file, indent=4)
        self.config = config
        if config["mode"] == "dev":
            self.permissions = False
        else:
            self.permissions = True
        self.bot = commands.Bot(command_prefix=config["command_prefix"])
        for cog in cogs:
            self.bot.add_cog(cog(self))

    def run(self):
        print(self.config["discord_token"])
        self.bot.run(self.config["discord_token"])
