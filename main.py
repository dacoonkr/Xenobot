import discord, os, asyncio
from keep_alive import keep_alive

app = discord.Client()
prefix = '='

@app.event
async def on_ready():
    print("Ready.")
    statuses = [
        discord.Game("z.help"),
        discord.Game("0 minigames"),
        discord.Game(str(len(app.users)) + " users | " + str(len(app.guilds)) + " guilds")
    ]
    while 1:
        for x in range(3):
            await app.change_presence(activity = statuses[x])
            await asyncio.sleep(4)

@app.event
async def on_message(message):
    if message.content == "z.info":
        tmpembed = discord.Embed(title = "XenoBot", description = "a0.0.1")
        tmpembed.set_thumbnail(url = app.user.avatar_url)
        await message.channel.send(embed = tmpembed)

keep_alive()
app.run(os.getenv("token"))