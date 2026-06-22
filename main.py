import sistema
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

@bot.event
async def on_ready():
    print('bot inicializado com sucesso')

@bot.command()
async def vr(ctx:commands.Context, *dados:int):
    dados_total = sum(dados)

    if dados_total > 65:
        return await ctx.send(
            content='O limite de dados atualmente é 66.'
        )
    
    resultado_dados = sistema.rolar(dados_total)

    resultados = resultado_dados['resultados']

    resultado_final = (resultado_dados['sucessos'] + resultado_dados['criticos']) - resultado_dados['fracassos']

    view = discord.ui.View()
    botao = discord.ui.Button(
        label='Rerolar Falhas',
        style=discord.ButtonStyle.secondary
    )

    dificuldade = discord.ui.Button(
        label='Dificuldade',
        style=discord.ButtonStyle.secondary
    )

    show_dados = ' '.join(str(x) for x in resultado_dados['resultados'])

    if resultado_final != 0:
        if resultado_dados['criticos'] == 0:
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
        value = f'Rolou: **{resultado_dados['sucessos']}** Sucessos.',
        inline = False
    )

    embed.add_field(
        #2
        name='Criticos',
        value=f'Rolou: **{resultado_dados['criticos']}** Criticos.',
        inline=False
    )

    embed.add_field(
        #3
        name='Falhas Criticas',
        value=f'Rolou: **{resultado_dados['fracassos']}** Falhas Criticas.',
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
        value='+-'*22
    )
    
    async def callback(interaction: discord.Interaction):
        fracassos = 0
        criticos = 0
        sucessos = 0
        rerolar = False

        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message(
                'Você não pode usar esse botão!',
                ephemeral=True
            )
            return

        for chave, valor in enumerate(resultados):
            if valor < 6:

                rerolar = sistema.rolar(1)
                resultado_dados['emoji'][chave] = rerolar['emoji'][0]
                resultado_dados['resultados'][chave] = rerolar['resultados'][0]
                sucessos += rerolar['sucessos']
                criticos += rerolar['criticos']
                fracassos += rerolar['fracassos']
        
        sucessos += resultado_dados['sucessos']
        criticos += resultado_dados['criticos']
        fracassos += resultado_dados['fracassos']

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
        try:
            await interaction.response.edit_message(
                content=''.join(str(i) for i in resultado_dados['emoji']),
                embed=embed,
                view=view)
        except discord.HTTPException as e:
            print(f'Erro ao editar mensagem: {e}')
    
    class DificuldadeModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(title='Dificuldade')
            self.mensagem = mensagem
        
        dificuldade = discord.ui.TextInput(label='Dificuldade',max_length=1,placeholder='Digite um número de 1 a 9')

        def alterar_dificuldade(self):
            print('ativou a func')
            nova_dificuldade = sistema.alterar_dificuldade(resultado_dados['resultados'],int(self.dificuldade.value))

            print(nova_dificuldade)

            resultado_final = (nova_dificuldade['sucessos'] + nova_dificuldade['criticos']) - nova_dificuldade['fracassos']
            show_dados = ' '.join(str(x) for x in nova_dificuldade['resultados'])

            embed.set_field_at(
                index=0,
                name='Dados',
                value=f'`{show_dados}`',
                inline=False
            )
            embed.set_field_at(
                index=1,
                name = 'Sucessos',
                value = f'Rolou: **{nova_dificuldade['sucessos']}** Sucessos.',
                inline = False
            )
            embed.set_field_at(
                index=2,
                name='Criticos',
                value=f'Rolou: **{nova_dificuldade['criticos']}** Criticos.',
                inline=False
            )
            embed.set_field_at(
                index=3,
                name='Falhas Criticas',
                value=f'Rolou: **{nova_dificuldade['fracassos']}** Falhas Criticas.',
                inline=False
            )
            embed.set_field_at(
                index=4,
                name='Resultado final',
                value=f'`{resultado_final}`',
                inline=False
            )

        async def on_submit(self, interaction: discord.Interaction):
            self.alterar_dificuldade()
            print (f'isso aqui é o print {self.alterar_dificuldade()}')
            await self.mensagem.edit(
                content=''.join(str(i) for i in resultado_dados['emoji']),
                embed=embed,
                view=view
            )

    async def interacao_teste(interaction: discord.Interaction):
        await interaction.response.send_modal(DificuldadeModal())
        print('funcionou')

    dificuldade.callback = interacao_teste

    botao.callback = callback
    view.add_item(botao)
    view.add_item(dificuldade)
    
    try:
        mensagem = await ctx.send(
            content=''.join(str(i) for i in resultado_dados['emoji']),
            embed=embed,
            view=view)
    except discord.HTTPException as e:
        print(f'Erro mensagem: {e}')

@vr.error
async def vr_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply('VALOR INVÁLIDO!')

bot.run(DISCORD_TOKEN)