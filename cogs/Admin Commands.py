# Import libraries
import discord
import os
from datetime import datetime
from discord.ext import commands
import traceback
import sqlite3
import sys
# Connect to database
database = sqlite3.connect('./database/dB.db')
cursor = database.cursor()

# Create class for admin commands
class Admin_Commands(commands.Cog, name='👑 Admin Commands'):
    """Admin Commands: Load/unload cogs and shut the bot down."""
    # ^ Docstring
    def __init__(self, client):
        self.client = client

    # Loads a cog
    @commands.has_role(737604230759841792)
    @commands.command(description='Loads a specified cog.')
    async def load(self, ctx, module : str):
        try:
            self.client.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Loaded cog.')

    # Unloads a cog
    @commands.has_role(737604230759841792)
    @commands.command(description='Unloads a specified cog.')
    async def unload(self, ctx, module : str):
        try:
            self.client.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Unloaded cog.')

    # Reloads a cog
    @commands.has_role(737604230759841792)
    @commands.command(aliases=['reload'], description='Reloads a specified cog.')
    async def _reload(self, ctx, module : str):
        try:
            self.client.unload_extension(f'cogs.{module}')
            self.client.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Successfully reloaded cog.')

    # Shuts bot down
    @commands.has_role(737604230759841792)
    @commands.command(aliases=['goodnight', 'jaljjayo', 'sd', 'snowwhendubu', 'maliwhensunoo', 'JaljayoUriKkumsogeseo'], description='Shuts down the bot.')
    async def shutdown(self, ctx):
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot has been shut down.')
        await ctx.send('Shutting down...')
        await self.client.close()
        exit()

    # Manually perform a query for the database
    @commands.has_role(737604230759841792)
    @commands.command(description='Query the database. Please don\'t abuse this.')
    async def query(self, ctx, *query: str):
        # If an argument is given
        if query:
            query = ' '.join(query)
            try:
                cursor.execute(query)
            # If there is an issue because of a primary key
            except sqlite3.IntegrityError as e:
                if e[:24] == 'UNIQUE constraint failed':
                    await ctx.reply('That group is already in the database.')
                else:
                    await ctx.reply(e)
            # For any other exception
            except Exception as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                await ctx.reply('Unexpected error:\n\n' + ''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
            # If all is good
            else:
                # If they used a SELECT query
                if query[:6].lower() == 'select':
                    msg = ''
                    result = cursor.fetchall()
                    for i in range(len(result)):
                        for j in result[i]:
                            msg += f"{j}, "
                        msg = msg[:-2] + '\n'
                    if msg:
                        await ctx.reply(msg)
                    else:
                        await ctx.reply('Nothing found.')
                else:
                    database.commit()
                    await ctx.reply('Successfully comitted changes.')
        else:
            await ctx.reply('Please give a query.')

# Called when loading cog
def setup(client):
    client.add_cog(Admin_Commands(client))
# gareth was here 👀
# indeed he was
