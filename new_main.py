import sistema
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

print('arquivo iniciado')

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

@bot.event
async def on_ready():
    print('bot inicializado com sucesso')

@bot.command()
async def vr(ctx:commands.Context, *dados: int):

    total = sum(dados)

    if total > 65:
        return await ctx.send('O limite de dados é 65')

    resultado = sistema.rolar(total)

    if resultado['resultado_final'] != 0:
        if resultado['criticos'] == 0:
            embed = discord.Embed(
        title = 'Rolagem',
        colour = discord.Colour.green()
        )
        else:
            embed = discord.Embed(
        title = 'Rolagem',
        colour = discord.Colour.teal()
        )
    else:
        embed = discord.Embed(
            title = 'Rolagem',
            colour = discord.Colour.red()
        )
    
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url
    )

    dados = ' '.join(map(str, resultado['resultados']))

    embed.add_field(
        name='Dados',
        value=f'`{dados}`',
        inline=False
    )
    embed.add_field(name='Sucessos', value=resultado['sucessos'], inline=False)
    embed.add_field(name='Críticos', value=resultado['criticos'], inline=False)
    embed.add_field(name='Falhas Críticas', value=resultado['fracassos'], inline=False)
    embed.add_field(name='Resultado Final', value=f'`{resultado['resultado_final']}`', inline=False)
    embed.add_field(name='',value='+-'*22)

    view = discord.ui.View()

    await ctx.send(content=''.join(resultado['emoji']),embed=embed, view=view)

bot.run(DISCORD_TOKEN)