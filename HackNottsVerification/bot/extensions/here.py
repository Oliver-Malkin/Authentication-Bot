import hikari, lightbulb, re, mysql.connector

from HackNottsVerification.bot import Bot

plugin = lightbulb.Plugin("here", default_enabled_guilds=977197096094564453)

@plugin.command
@lightbulb.command("here", "Use this to get the 'I was here' role!", auto_defer = True, ephemeral = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def here(ctx: lightbulb.SlashContext):
    role_id = 1058732186804695170
    with open("./secrets/sqlserver_pass", "r") as file:
        sql_pass = file.read().strip()

    with open("./secrets/sqlserver_user", "r") as file:
        sql_user = file.read().strip()

    db = mysql.connector.connect(
        host="localhost",
        user=sql_user,
        password=sql_pass,
        database="HackNotts"
    )
    db_cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM `People` WHERE `DiscordTag` = %s"
    db_cursor.execute(sql, (f"{ctx.user.username}#{ctx.user.discriminator}",))
    result: dict = db_cursor.fetchall()[0]
    db.close()

    if result['CheckedIn'] == 0:
        await ctx.respond("You have not checked in yet!")
    elif result['CheckedIn'] == 1:
        await plugin.bot.rest.add_role_to_member(977197096094564453, ctx.user.id, role_id)
        await ctx.respond("*You're in* <:software:1024699991933063190>")
    else:
        ctx.respond("An error occured! Try again later :smiley:")

def load(bot: Bot) -> None:
    bot.add_plugin(plugin)

def unload(bot: Bot) -> None:
    bot.remove_plugin("here")
