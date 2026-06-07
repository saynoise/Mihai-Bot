import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

class Emojis:
    sucesso = '<:sucesso:1512846827962237121>'
    falha = '<:falha:1512846801290530948>'
    critico = '<:critico:1512846854608650311>'
    fcritica = '<:falhacritica:1512846843183104031>'

@bot.event
async def on_ready():
    print('bot inicializado com sucesso')

@bot.command()
async def vr(ctx:commands.Context, *dados:int):
    fracassos = 0
    criticos = 0
    resultados = []
    resultados_emoji = []
    sucessos = 0
    dados_total = sum(dados)
    view = discord.ui.View()
    botao = discord.ui.Button(
        label='Rerolar Falhas',
        style=discord.ButtonStyle.primary
    )

    for i in range(dados_total):

        rolagem = random.randint(1,10)
        resultados.append(rolagem)

        if rolagem >= 6: 
            sucessos += 1
            if rolagem == 10:
                criticos += 1
                resultados_emoji.append(Emojis.critico)
            else:
                resultados_emoji.append(Emojis.sucesso)

        if rolagem < 6:
            if rolagem == 1:
                fracassos += 1
                resultados_emoji.append(Emojis.fcritica)
            else:
                resultados_emoji.append(Emojis.falha)
    
    resultado_final = (sucessos + criticos) - fracassos
    show_dados = ' '.join(str(x) for x in resultados)

    if resultado_final != 0:
        if criticos == 0:
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
        name = str(ctx.author.display_name),
        icon_url = ctx.author.display_avatar.url
    )

    embed.add_field(
        #0
        name = 'Dados',
        value = f'`{show_dados}`',
        inline = False
    )

    embed.add_field(
        #1
        name = 'Sucessos',
        value = f'Rolou: **{sucessos}** Sucessos.',
        inline = False
    )

    embed.add_field(
        #2
        name='Criticos',
        value=f'Rolou: **{criticos}** Criticos.',
        inline=False
    )

    embed.add_field(
        #3
        name='Falhas Criticas',
        value=f'Rolou: **{fracassos}** Falhas Criticas.',
        inline=False
    )

    embed.add_field(
        #4
        name='Resultado final',
        value=f'`{resultado_final}`',
        inline=False
    )

    embed.add_field(
        #5
        name='',
        value='+-'*25
    )
    
    async def callback(interaction: discord.Interaction):
        fracassos = 0
        criticos = 0
        sucessos = 0

        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message(
                'Você não pode usar esse botão!',
                ephemeral=True
            )
            return

        for chave, valor in enumerate(resultados):
            if valor < 6:
                resultados[chave] = random.randint(1, 10)
            if resultados[chave] >= 6: 
                sucessos += 1
                if resultados[chave] == 10:
                    criticos += 1 
                    resultados_emoji[chave] = Emojis.critico
                else:
                    resultados_emoji[chave] = Emojis.sucesso

            if resultados[chave] < 6:
                if resultados[chave] == 1:
                    fracassos += 1
                    resultados_emoji[chave] = Emojis.fcritica
                else:
                    resultados_emoji[chave] = Emojis.falha

        resultado_final = (sucessos + criticos) - fracassos

        show_dados = ' '.join(str(x) for x in resultados)
        embed.set_field_at(
            index=0,
            name='Dados',
            value=f'`{show_dados}`',
            inline=False
        )
        embed.set_field_at(
            index=1,
            name = 'Sucessos',
            value = f'Rolou: **{sucessos}** Sucessos.',
            inline = False
        )
        embed.set_field_at(
            index=2,
            name='Criticos',
            value=f'Rolou: **{criticos}** Criticos.',
            inline=False
        )
        embed.set_field_at(
            index=3,
            name='Falhas Criticas',
            value=f'Rolou: **{fracassos}** Falhas Criticas.',
            inline=False
        )
        embed.set_field_at(
            index=4,
            name='Resultado final',
            value=f'`{resultado_final}`',
            inline=False
        )

        botao.disabled = True
        await interaction.response.edit_message(
            content=''.join(str(i) for i in resultados_emoji),
            embed=embed,
            view=view)
    
    botao.callback = callback
    view.add_item(botao)

    await ctx.send(
        content=''.join(str(i) for i in resultados_emoji),
        embed=embed,
        view=view)

@vr.error
async def vr_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply('VALOR INVÁLIDO!')

bot.run(DISCORD_TOKEN)