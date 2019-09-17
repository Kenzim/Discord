import msgpack
import discord.ext.commands
from essentials import ensure_file_existence  # https://github.com/Kenzim/Discord/blob/master/essentials.py


"""
Copyright Kenzi Marcel - 2018
This is a proprietary library used to easily store dictionaries using 'with' syntax
into MsgPack file. This library can also take ctx as an argument, to split up storage
files saved with the same name into guild folders.
https://github.com/Kenzim/Discord
"""


class Get:
    def __init__(self, ctx: discord.ext.commands.Context = None, name=None):
        self.ctx = ctx
        self.name = name
        self.data = None
        if isinstance(ctx, str):
            self.filename = f"data/Bot/{self.ctx}.msgpack"
            try:
                ensure_file_existence(self.filename)
                with open(self.filename, "rb") as fp:
                    if fp.read():
                        fp.seek(0)
                        self.data = msgpack.unpack(fp, encoding="utf-8")
                    else:
                        self.data = {}
            except FileNotFoundError:
                self.data = {}
        else:
            self.filename = f"data/{self.ctx.guild.id}/{self.name}.msgpack"
            try:
                ensure_file_existence(self.filename)
                with open(self.filename, "rb") as fp:
                    if fp.read():
                        fp.seek(0)
                        self.data = msgpack.unpack(fp, encoding="utf-8")
                    else:
                        self.data = {}
            except FileNotFoundError:
                self.data = {}

    def __enter__(self):
        return self

    def dump(self, data):
        self.data = data

    def __exit__(self, exc_type, exc_value, tb):

        ensure_file_existence(self.filename)
        with open(self.filename, "wb") as fp:
            msgpack.pack(self.data, fp)
