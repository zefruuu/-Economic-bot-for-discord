import discord
from discord.ext import commands
import sqlite3
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True 
intents.guilds = True 
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)


conn = sqlite3.connect("eso.sqlite")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS eco (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER,
                    bank INTEGER
                    
                )""")
conn.commit()
conn.close()

@bot.command(aliases=["bal", "баланс","бал"])
async def balance(ctx, member: discord.Member = None):
   
    conn = sqlite3.connect("eso.sqlite")
    cursor = conn.cursor()

    
    if member is None:
        member = ctx.author

    cursor.execute("SELECT balance, bank FROM eco WHERE user_id = ?", (member.id,))
    bal = cursor.fetchone()
    try:
        if bal:
            balance, bank = bal
        else:
            balance = 0
            bank = 0
    except Exception as e:
        print(f"Error fetching balance: {e}")
        balance = 0
        bank = 0

    user_mention = member.mention
    reply_message = f" >>> **Big World RP:earth_africa:**\n\n**Баланс игрока** {user_mention} \n\n**Баланс: {balance}:moneybag:\n\nБанк: {bank}:moneybag:**\n\n"
    await ctx.reply(reply_message, mention_author=False)


@bot.command(aliases=["коллект", "колект", "Колект", "Collection"])
@commands.cooldown(1, 5400, commands.BucketType.user)  
async def collect(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    coll_ranges = {
        "Очень слабая экономика": (1000000, 2000000),
        "Слабая экономика": (2500000, 3500000),
        "Средняя экономика": (4200000, 6000000),
        "Сильная экономика": (8000000, 11000000),
        "Экономический бум": (13000000, 18000000)
    }

    coll = 0

    for role in member.roles:
        if role.name in coll_ranges:
            coll = random.randint(*coll_ranges[role.name])
            break  

    if coll == 0:
        coll = random.randint(1000000, 2000000)

    conn = sqlite3.connect("eso.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (member.id,))
    bal = cursor.fetchone()

    if bal is not None:
        bal = bal[0]
    else:
        cursor.execute("INSERT INTO eco (user_id, balance, bank) VALUES (?, ?, ?)", (member.id, 0, 0))
        bal = 0

    new_bal = bal + coll 

    cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (new_bal, member.id))
    conn.commit()
    conn.close()

    await ctx.reply(f">>> **Big World RP:earth_africa:\n\nСбор налогов\n\nnВаша страна заработала:{coll}:moneybag:\n\n Ваш новый баланс: {new_bal}:moneybag:.**")

    if ctx.command.get_cooldown_retry_after(ctx) > 0:  
        await ctx.reply(f">>> **Тихо, не спеши! Команда на кулдауне. Пожалуйста, подождите еще {ctx.command.get_cooldown_retry_after(ctx):.2f} секунд.**")




@bot.command()
@commands.has_role("Глава")  
async def clearbalance(ctx, member: discord.Member):
    db = sqlite3.connect("eso.sqlite")
    cursor = db.cursor()

    cursor.execute("UPDATE eco SET balance = 0 WHERE user_id = ?", (member.id,))
    db.commit()

    cursor.close()
    db.close()

    reply_message = f"**Баланс игрока {member.mention} успешно очищен.**"
    await ctx.send(reply_message, reference=ctx.message)

@clearbalance.error
async def clear_balance_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        reply_message = "**У вас недостаточно прав для выполнения этой команды.**"
        await ctx.send(reply_message, reference=ctx.message)
    elif isinstance(error, commands.BadArgument):
        reply_message = "**Пожалуйста, укажите участника для очистки баланса.**"
        await ctx.send(reply_message, reference=ctx.message)

@bot.command(aliases=["мут"])
@commands.has_any_role("Глава", "Заместитель Главы", "Администратор 1 LVL", "Администратор 3 LVL", "Администратор 2 LVL")
@commands.has_permissions(manage_messages=True)


async def mute(ctx, member: discord.Member, duration: int, *, reason: str):
    mute_role = discord.utils.get(ctx.guild.roles, name="Мuted")  
    if not mute_role:
       
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

   
    await member.add_roles(mute_role)

   
    muty_channel = discord.utils.get(ctx.guild.channels, name="【🚫】наказания")
    if muty_channel:
        await muty_channel.send(f"> **{member.mention} был замучен на {duration} секунд по причине: {reason}!**")

   
    await asyncio.sleep(duration)
    await member.remove_roles(mute_role)

   
    if muty_channel:
        await muty_channel.send(f"> **Мут у {member.mention} был снят!**")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**У вас недостаточно прав для использования этой команды.**", reference=ctx.message)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Пожалуйста, укажите участника для мута, длительность в секундах и причину.**", reference=ctx.message)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("**Указанный участник не найден или длительность мута должна быть целым числом.**", reference=ctx.message)

conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    count INTEGER
                )""")
conn.commit()

import sqlite3


conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    count INTEGER
                )""")
conn.commit()

import sqlite3
import asyncio

conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    count INTEGER
                )""")
conn.commit()

@bot.command()
async def пред(ctx, member: discord.Member, *, reason: str):
    punishments_channel = discord.utils.get(ctx.guild.channels, name="【🚫】наказания")

    cursor.execute("SELECT count FROM warnings WHERE user_id = ?", (member.id,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO warnings (user_id, count) VALUES (?, ?)", (member.id, 0))
        conn.commit()
        count = 0
    else:
        count = result[0]

    count += 1
    cursor.execute("UPDATE warnings SET count = ? WHERE user_id = ?", (count, member.id))
    conn.commit()

    if punishments_channel:
        await punishments_channel.send(f"**{member.mention}, у вас теперь {count} предупреждений. Причина: {reason}**")

    if count == 1:
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role:
            await member.add_roles(mute_role)
            await asyncio.sleep(2400)  
            await member.remove_roles(mute_role)
            if punishments_channel:
                await punishments_channel.send(f"> **{member.mention} был замучен на 40 минут за первое предупреждение. Причина: {reason}**")
    elif count == 2:
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role:
            await member.add_roles(mute_role)
            await asyncio.sleep(7200) 
            await member.remove_roles(mute_role)
            if punishments_channel:
                await punishments_channel.send(f"> **{member.mention} был замучен на 120 минут за второе предупреждение. Причина: {reason}**")
    elif count >= 3:
        await ctx.guild.ban(member, reason="**Три предупреждения**")
        if punishments_channel:
            await punishments_channel.send(f"> **{member.mention} был забанен за три предупреждения! Причина: {reason}**")
        cursor.execute("DELETE FROM warnings WHERE user_id = ?", (member.id,))
        conn.commit()


    await ctx.send(f"**У {member.mention} теперь {count} предупреждений.**")

@bot.command()
async def снятьпред(ctx, member: discord.Member):
    punishments_channel = discord.utils.get(ctx.guild.channels, name="【🚫】наказания")

    cursor.execute("SELECT count FROM warnings WHERE user_id = ?", (member.id,))
    result = cursor.fetchone()

    if result:
        count = result[0]
        if count > 0:
            count -= 1
            cursor.execute("UPDATE warnings SET count = ? WHERE user_id = ?", (count, member.id))
            conn.commit()

            if punishments_channel:
                await punishments_channel.send(f"> **{member.mention}, одно предупреждение было снято. Теперь у вас {count} предупреждений.**")

    await ctx.send(f"**У {member.mention} теперь {count} предупреждений.**")




@bot.event
async def on_ready():
    rules_channel = discord.utils.get(bot.guilds[0].channels, name="【⛔️】правила-проекта")

    if rules_channel:
        rules_message = await rules_channel.send(
            " > **Правила войны: 1**\n\n"
            " > **Правила общения: 2**\n\n"
            " > **Правила вассалов и автономии: 3**"
        )

        await rules_message.add_reaction("1️⃣")
        await rules_message.add_reaction("2️⃣")
        await rules_message.add_reaction("3️⃣")

        print("Сообщение с правилами успешно отправлено.")
    else:
        print("Канал с правилами не найден.")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == False and reaction.message.channel.name == "【⛔️】правила-проекта":
        if str(reaction.emoji) == "1️⃣":
            rule_text = "Правила войны: ..."
        elif str(reaction.emoji) == "2️⃣":
            rule_text = """ >>> **Правила общения: Правила общения: Правила общения: 2 Раздел: Правила чата
1.1. В чате запрещено обсуждать политические темы. Наказание: мут на 30 минут.
1.2. В текстовом чате запрещено оскорблять родных другого человека. Наказание: мут от 30 минут до более 2 часов(По решению администратора).
1.3. Запрещен спам. Наказание: мут на 1 час.
1.4. Запрещено рекламировать другие проекты в чате нашего проекта. Наказание: от 1 предупреждения до бана на 2 дня.(По решению администратора)
1.5. Запрещена реклама по типу "Free 50$ to Steam:"Скам ссылка". Наказание: 1 предупреждение.
1.6. Запрещено оскорблять национальность. Наказание: Мут на 2 часа.
1.7. Запрещено оскорблять наш проект. Наказание: От 1 предупреждения до черного списка проекта(По решению администратора).**"""
        elif str(reaction.emoji) == "3️⃣":
            rule_text = "Правила вассалов и автономии: ..."
        
        rule_message = await user.send(rule_text)
        await asyncio.sleep(500)
        await rule_message.delete()

        await reaction.remove(user)
@bot.command()
async def pay(ctx, recipient: discord.Member, amount: int, *, comment: str = None):
    if amount <= 0:
        await ctx.send("Вы не можете перевести отрицательное количество денег или ноль.")
        return

    try:
        db = sqlite3.connect("eso.sqlite")
        cursor = db.cursor()

 
        cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (ctx.author.id,))
        sender_balance = cursor.fetchone()

        if sender_balance is None or sender_balance[0] < amount:
            await ctx.send("У вас недостаточно денег для выполнения этой операции.")
            return

     
        cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (recipient.id,))
        recipient_balance = cursor.fetchone()

        if recipient_balance is None:
            cursor.execute("INSERT INTO eco (user_id, balance, bank) VALUES (?, ?, 0)", (recipient.id, 0))
            db.commit()
            recipient_balance = (0,)
        else:
            recipient_balance = recipient_balance[0]

     
        sender_new_balance = sender_balance[0] - amount
        recipient_new_balance = recipient_balance + amount


        cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (sender_new_balance, ctx.author.id))
        cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (recipient_new_balance, recipient.id))
        db.commit()

      
        if comment:
            await ctx.send(f"Вы перевели {amount} единиц валюты игроку {recipient.mention}. Комментарий: {comment}")
        else:
            await ctx.send(f"Вы перевели {amount} единиц валюты игроку {recipient.mention}.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка: {e}")
    finally:
        db.close()

        @bot.event
        async def on_member_join(member):
    
            async for entry in member.guild.audit_logs(action=discord.AuditLogAction.invite_create, limit=5):
                if entry.target == member:
                    inviter = entry.user
                break
            else:
             inviter = None

    
    if inviter:
        conn = sqlite3.connect("eso.sqlite")
        cursor = conn.cursor()

        
        cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (inviter.id,))
        inviter_balance = cursor.fetchone()
        if inviter_balance:
            balance = inviter_balance[0] + 2000000
        else:
            balance = 2000000  

        
        cursor.execute("INSERT OR REPLACE INTO eco (user_id, balance, bank) VALUES (?, ?, 0)", (inviter.id, balance))
        conn.commit()

       
        inviter_user = bot.get_user(inviter.id)
        if inviter_user:
            await inviter_user.send(f"**Вы успешно пригласили {member.name} на сервер! Ваш баланс увеличен на 2кк кредитов.**")

    
    await member.send(f"**Добро пожаловать на сервер! Вас пригласил {inviter.name if inviter else 'кто-то'}. **")
                      
import sqlite3

@bot.command()
async def вложить(ctx, category: str, amount: int):
    roles = {
        "Очень слабая экономика⛔️": (25000000, 25000001),
        "Слабая экономика🚨": (40000000, 40000001),
        "Средняя экономика🚧": (60000000, 60000001),
        "Сильная экономика💹": (80000000, 80000001),
        "Экономический бум💸": (130000000, 130000001)
    }

    category_lower = category.lower()
    if category_lower != "economy":
        await ctx.send(">>> **Неправильная категория. Используйте `economy`.**")
        return

    current_role = None
    for role in ctx.author.roles:
        if role.name in roles:
            current_role = role.name
            break

    if current_role is None:
        await ctx.send(">>> **Вы должны начать с роли очень слабая экономика.**")
        return

    if current_role != "Очень слабая экономика⛔️":
        await ctx.send(">>> **Вы уже вложены в экономику и имеете другую роль.**")
        return

    current_range = roles[current_role]
    if not isinstance(current_range, tuple):
        await ctx.send(">>> **Неправильная категория ролей. Пожалуйста, свяжитесь с администратором.**")
        return
    
    min_amount, max_amount = current_range

    if amount < min_amount or amount > max_amount:
        await ctx.send(f">>> **Сумма вклада должна быть между {min_amount} и {max_amount}.**")
        return

    
    conn = sqlite3.connect("eso.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM eco WHERE user_id = ?", (ctx.author.id,))
    user_balance = cursor.fetchone()

    if user_balance is None:
        cursor.execute("INSERT INTO eco (user_id, balance) VALUES (?, ?)", (ctx.author.id, 0))
        user_balance = (0,)

    if user_balance[0] < amount:
        await ctx.send(f">>> **{ctx.author.mention}, у вас недостаточно денег на балансе для вложения {amount}.**")
        cursor.close()
        conn.close()
        return

    new_balance = user_balance[0] - amount
    cursor.execute("UPDATE eco SET balance = ? WHERE user_id = ?", (new_balance, ctx.author.id))
    conn.commit()

    await ctx.send(f">>> **{ctx.author.mention}, ваш вклад в экономику завершен. С вашего баланса было списано {amount}.**")

    cursor.close()
    conn.close()


@bot.command()
@commands.has_any_role("Глава", "Заместитель Главы", "Следящий за персоналом")
async def clear_channel(ctx):
    channel = ctx.channel
    await channel.purge()
    await ctx.send("Все сообщения в этом канале были удалены.", delete_after=5)  

@bot.command()
@commands.has_any_role("Глава", "Заместитель Главы", "Следящий за персоналом")
async def limit(ctx, char_limit: int):
    channel = ctx.channel
    await ctx.message.delete() 

    def check(message):
        return len(message.content) < char_limit and message.author != bot.user

    await ctx.send(f">>> **Ограничение на длину сообщений в этом канале установлено на {char_limit} символов.**", delete_after=10)

    while True:
        try:
            message = await bot.wait_for("message", check=check, timeout=60)  
            await ctx.send(f">>> **{message.author.mention}, новость про вашу страну должна содержать минимум {char_limit} символов.**", delete_after=10)
            await message.delete()  
        except asyncio.TimeoutError:
            break 

@bot.command()
@commands.has_any_role("Глава", "Заместитель Главы", "Следящий за регистрацией📃")
async def рег(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")
        return

 
    roles_to_assign = [
        ".................................Статус.................................",
        "Государство🚩",
        "Очень слабая экономика⛔️",
        ".................................Уровень жизни.................................",
        ".................................Экономика.................................",
        "Ужасный уровень жизни🆘",
        ".................................Медицина.................................",
        "Очень ужасная медицина♿️",
        ".................................Наука.................................",
        "Ужасная наука👩‍🔬",
        ".................................Образование.................................",
        "Ужасное образование👨‍🏫",
        ".................................Преступность.................................",
        "Очень опасная преступность🚨",
        ".................................Инфраструктура.................................",
        "Ужасная инфраструктура🚧",
        ".................................Экология.................................",
        "Ужасная экология🌄",



        
    ]

    for role_name in roles_to_assign:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            try:
                await member.add_roles(role)
                await ctx.send(f"Роль {role.name} успешно выдана пользователю {member.mention}.")
            except discord.Forbidden:
                await ctx.send(f"У меня нет прав для выдачи роли {role.name}.")
            except discord.HTTPException:
                await ctx.send(f"Произошла ошибка при выдаче роли {role.name}.")
        else:
            await ctx.send(f"Роль {role_name} не найдена на сервере.")


with open("key.txt","r") as token:
    bot.run(token.read())
