import discord, os, asyncio
from keep_alive import keep_alive

app = discord.Client()
prefix = '='

minigames = [
    ["🖐️ 가위바위보", "컴퓨터와 가위바위보 게임을 합니다."]
]

moderators = {
    "534145145109741569" : "다쿤"
}

@app.event
async def on_ready():
    print("Ready.")
    statuses = [
        discord.Game("z.help"),
        discord.Game(f"{len(minigames)} minigames"),
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
        return

    elif message.content == "z.help":
        tmpembed = discord.Embed(title = "Minigames", description = f"There're {len(minigames)} minigames!\n\
        `z.play <Minigame Number>` to play minigame!")
        for x in range(len(minigames)):
            tmpembed.add_field(name = f"{x + 1}. {minigames[x][0]}", value = f"`{minigames[x][1]}`")
        await message.channel.send(embed = tmpembed)
        return


    if message.content.startswith("z.eval") and isModer(message.author):
        await message.channel.send(eval(message.content[7:]))

    elif message.content.startswith("z.exec") and isModer(message.author):
        exec(message.content[7:])
        

def isModer(user):
    if str(user.id) in moderators:
        return True
    return False

keep_alive()
app.run(os.getenv("token"))