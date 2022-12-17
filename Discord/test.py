import discord
from discord import app_commands
from discord.ext import commands
# from config import TOKEN

bot = commands.Bot(command_prefix="uno!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synched {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey! ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ {interaction.user.mention}!",
    ephemeral=True)

@bot.tree.command(name="repeat")
@app_commands.describe(thing_to_say = "what should i say?")
async def repeat(interaction: discord.Interaction, thing_to_say: str, type: int = 0):
    if type == 0:
        await interaction.response.send_message(f"Squack! {thing_to_say}! Squack!", ephemeral=False)
    elif type == 1234567890:
        await interaction.response.send_message(f"{thing_to_say}", ephemeral=False)
    else:
        await interaction.response.send_message(f"Squack! No I won't say that! Squack! {interaction.user.mention} we don't support that behaviour here! Squack!", ephemeral=False)

bot.run(token="")