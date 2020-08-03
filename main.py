import discord, os, asyncio, random
from keep_alive import keep_alive

app = discord.Client()
prefix = '='

minigames = [
    ["🖐️ 가위바위보", "봇과 가위바위보 게임을 합니다."],
    ["↕️ 업다운", "봇이 정한 숫자로 업다운 게임을 합니다."],
    ["🔠 16 슬라이딩 퍼즐", "랜덤으로 섞인 숫자들을 정렬합니다."]
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

    elif message.content == "z.ping":
        tmpembed = discord.Embed(title = "🏓 Pong!", description = f"{str(app.latency * 1000)[:6]}ms")
        await message.channel.send(embed = tmpembed)

    elif message.content.startswith("z.play"):
        gamenumber = message.content[7:]
        if gamenumber == "1":
            tmpembed = discord.Embed(title = "🖐️ 가위바위보", description = "각자 가위 또는 바위 또는 보를 내서 승부를 결정하는 게임입니다. 가위는 보를, 바위는 가위를, 보는 묵을 이길 수 있습니다. 두 명이 같은 손을 낼 시 비깁니다.")
            await message.channel.send(embed = tmpembed)
            tmpembed = discord.Embed(title = "가위, 바위, 보 중 하나를 선택하세요")
            main = await message.channel.send(embed = tmpembed)
            await main.add_reaction("✌️")
            await main.add_reaction("✊")
            await main.add_reaction("🖐️")
            hands = ["✌️", "✊", "🖐️"]
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in hands
            try:
                reaction, user = await app.wait_for('reaction_add', timeout = 5, check = check)
            except asyncio.TimeoutError:
                tmpembed = discord.Embed(title = "당신은 패배하였습니다!", description = "선택하는 데 시간이 너무 오래 걸렸습니다!")
                await message.channel.send(embed = tmpembed)
                return
            else:
                choiceOfCpu = random.choice(hands)
                if choiceOfCpu == str(reaction.emoji):
                    tmpembed = discord.Embed(title = "비겼습니다!", description = f"봇도 {choiceOfCpu}를 냈습니다!")
                    await message.channel.send(embed = tmpembed)
                    return
                winlist = ["✊✌️", "✌️🖐️", "🖐️✊"]
                if str(reaction.emoji) + choiceOfCpu in winlist:
                    tmpembed = discord.Embed(title = "당신이 이겼습니다!", description = f"봇은 {choiceOfCpu}를 냈습니다!")
                    await message.channel.send(embed = tmpembed)
                    return
                else:
                    tmpembed = discord.Embed(title = "봇이 이겼습니다!", description = f"봇은 {choiceOfCpu}를 냈습니다!")
                    await message.channel.send(embed = tmpembed)
                    return
        
        elif gamenumber == "2":
            tmpembed = discord.Embed(title = "↕️ 업다운", description = "1~100까지 숫자중 하나를 골랐을 때 그것을 맞추는 게임입니다. 기회는 총 5번 있습니다. 숫자를 추측하면 봇이 생각한 숫자보다 큰지 작은지 알려줍니다.")
            await message.channel.send(embed = tmpembed)

            choiceOfCpu = random.randint(1, 100)
            before = ""

            for x in range(5):
                tmpembed = discord.Embed(title = f"{before}{5 - x}번의 기회가 남았습니다.", description = "1~100까지 숫자중 하나를 고르세요.")
                await message.channel.send(embed = tmpembed)
                def check(msg):
                    return msg.author == message.author
                try:
                    msg = await app.wait_for('message', timeout = 10, check = check)
                except asyncio.TimeoutError:
                    tmpembed = discord.Embed(title = "봇이 승리하였습니다!", description = "선택하는 데 시간이 너무 오래 걸렸습니다!")
                    await message.channel.send(embed = tmpembed)
                    return
                else:
                    try: a = int(msg.content)
                    except: before = "숫자를 입력해 주세요. "
                    else:
                        if choiceOfCpu == a:
                            tmpembed = discord.Embed(title = "당신이 이겼습니다!", description = f"봇이 생각한 숫자는 {choiceOfCpu}였습니다.")
                            await message.channel.send(embed = tmpembed)
                            return
                        elif choiceOfCpu > a:
                            before = f"{a}보다 큽니다! "
                        else:
                            before = f"{a}보다 작습니다! "
            
            tmpembed = discord.Embed(title = "봇이 이겼습니다!", description = f"봇이 생각한 숫자는 {choiceOfCpu}였습니다.")
            await message.channel.send(embed = tmpembed)

        elif gamenumber == "3":
            tmpembed = discord.Embed(title = "🔠 16 슬라이딩 퍼즐", description = "각각의 타일을 밀어서 1부터 15까지 숫자를 순서대로 정렬하는 퍼즐입니다.")
            await message.channel.send(embed = tmpembed)

            xpt, ypt = 3, 3
            doneBoard = [ [1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16] ]
            board =     [ [1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16] ]
            
            def moveTo(mx, my, xpt, ypt):
                if not(0 <= (xpt + mx) < 4): return False
                if not(0 <= (ypt + my) < 4): return False
                tmp = board[ypt + my][xpt + mx]
                board[ypt + my][xpt + mx] = board[ypt][xpt]
                board[ypt][xpt] = tmp
                return True

            def boardStr():
                strs = ""
                for y in range(4):
                    for x in range(4):
                        if board[y][x] == 16:
                            strs += "🟪"
                        else:
                            strs += ":regional_indicator_" + ("abcdefghijklmno")[board[y][x] - 1] + ":"
                    strs += "\n"
                return strs

            tmpembed = discord.Embed(title = "타일을 섞는 중입니다.")
            main = await message.channel.send(embed = tmpembed)
            await main.add_reaction("⬆")
            await main.add_reaction("⬇")
            await main.add_reaction("⬅")
            await main.add_reaction("➡")
            await main.add_reaction("🚫")

            cntMix, cntSolv = 0, 0
            moving = ""

            for x in range(random.randint(30, 50)):
                canmove = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                movedirc = ["⬅", "➡", "⬆", "⬇"]
                wantmove = random.randint(0, 3)
                if moveTo(canmove[wantmove][0], canmove[wantmove][1], xpt, ypt) == True:
                    xpt += canmove[wantmove][0]
                    ypt += canmove[wantmove][1]
                    moving += movedirc[wantmove]
                    cntMix += 1

            while 1:
                tmpembed = discord.Embed(title = "타일을 밀 방향을 선택하세요. [포기: 🚫]", description = boardStr())
                await main.edit(embed = tmpembed)

                arrows = ["⬆", "⬇", "⬅", "➡", "🚫"]
                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in arrows
                try:
                    reaction, user = await app.wait_for('reaction_add', timeout = 40, check = check)
                except asyncio.TimeoutError:
                    tmpembed = discord.Embed(title = "실패하였습니다!", description = "생각하는 데 시간이 너무 오래 걸렸습니다!")
                    await message.channel.send(embed = tmpembed)
                    return
                else:
                    if str(reaction.emoji) == arrows[4]:
                        tmpembed = discord.Embed(title = "봇이 이겼습니다!", description = f"봇이 타일을 섞은 과정은 {moving}이었습니다.")
                        await message.channel.send(embed = tmpembed)
                        return
                    if str(reaction.emoji) == arrows[0]:
                        if moveTo(0, 1, xpt, ypt) == True:
                            ypt += 1
                            cntSolv += 1
                    if str(reaction.emoji) == arrows[1]:
                        if moveTo(0, -1, xpt, ypt) == True:
                            ypt += -1
                            cntSolv += 1
                    if str(reaction.emoji) == arrows[2]:
                        if moveTo(1, 0, xpt, ypt) == True:
                            xpt += 1
                            cntSolv += 1
                    if str(reaction.emoji) == arrows[3]:
                        if moveTo(-1, 0, xpt, ypt) == True:
                            xpt += -1
                            cntSolv += 1
                    await reaction.remove(message.author)

                    if board == doneBoard: break
            
            tmpembed = discord.Embed(title = "타일을 밀 방향을 선택하세요. [포기: 🚫]", description = boardStr())
            await main.edit(embed = tmpembed)
            tmpembed = discord.Embed(title = "당신이 이겼습니다!", description = f"섞으면서 타일을 움직인 횟수는 {cntMix}이고 풀면서 타일을 움직인 횟수는 {cntSolv}입니다.")
            await message.channel.send(embed = tmpembed)

        else:
            tmpembed = discord.Embed(title = "Unknown Minigame Number", description = "Send `z.help`to show minigames list")
            await message.channel.send(embed = tmpembed)
        
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