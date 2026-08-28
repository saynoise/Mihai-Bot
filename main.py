import os

import discord
import sistema
from discord.ext import commands
from dotenv import load_dotenv


MAX_DADOS = 65


def criar_embed(ctx: commands.Context, resultado: dict, dificuldade: int = 6) -> discord.Embed:
    resultado_final = resultado['resultado_final']
    if resultado_final > 0:
        cor = discord.Colour.teal() if resultado['criticos'] else discord.Colour.green()
    else:
        cor = discord.Colour.red()

    embed = discord.Embed(title='Rolagem', colour=cor)
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url,
    )
    embed.add_field(
        name='Dados',
        value=f"`{' '.join(map(str, resultado['resultados']))}`",
        inline=False,
    )
    embed.add_field(name='Sucessos', value=f"**{resultado['sucessos']}**", inline=False)
    embed.add_field(name='Críticos', value=f"**{resultado['criticos']}**", inline=False)
    embed.add_field(name='Falhas Críticas', value=f"**{resultado['fracassos']}**", inline=False)
    embed.add_field(name='Resultado Final', value=f"`{resultado_final}`", inline=False)
    embed.add_field(name='Dificuldade', value=f'`{dificuldade}+`', inline=False)
    embed.set_footer(text='--DESENVOLVIDO POR SAYNOISE/MIHAI')
    return embed


class DificuldadeModal(discord.ui.Modal, title='Alterar dificuldade'):
    dificuldade = discord.ui.TextInput(
        label='Dificuldade',
        placeholder='Digite um número de 1 a 9',
        min_length=1,
        max_length=1,
    )

    def __init__(self, view: 'RolagemView'):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            dificuldade = int(self.dificuldade.value)
        except ValueError:
            await interaction.response.send_message(
                'A dificuldade deve ser um número de 1 a 9.', ephemeral=True
            )
            return

        if not 1 <= dificuldade <= 9:
            await interaction.response.send_message(
                'A dificuldade deve estar entre 1 e 9.', ephemeral=True
            )
            return

        self.view.dificuldade = dificuldade
        self.view.resultado = sistema.alterar_dificuldade(
            self.view.resultado['resultados'], dificuldade
        )
        await interaction.response.edit_message(
            content=''.join(self.view.resultado['emoji']),
            embed=criar_embed(self.view.ctx, self.view.resultado, dificuldade),
            view=self.view,
        )


class RolagemView(discord.ui.View):
    def __init__(self, ctx: commands.Context, resultado: dict):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.resultado = resultado
        self.dificuldade = 6

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                'Você não pode usar esse botão!', ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label='Rerolar Falhas', style=discord.ButtonStyle.secondary)
    async def rerolar(self, interaction: discord.Interaction, button: discord.ui.Button):
        valores = self.resultado['resultados'][:]
        for indice, valor in enumerate(valores):
            if valor < self.dificuldade:
                nova_rolagem = sistema.rolar(1)
                valores[indice] = nova_rolagem['resultados'][0]

        self.resultado = sistema.alterar_dificuldade(valores, self.dificuldade)
        button.disabled = True
        await interaction.response.edit_message(
            content=''.join(self.resultado['emoji']),
            embed=criar_embed(self.ctx, self.resultado, self.dificuldade),
            view=self,
        )

    @discord.ui.button(label='Dificuldade', style=discord.ButtonStyle.secondary)
    async def alterar_dificuldade(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DificuldadeModal(self))


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)


@bot.event
async def on_ready():
    print('bot inicializado com sucesso')


@bot.command()
async def vr(ctx: commands.Context, *dados: int):
    total = sum(dados)
    if total == 0:
        return await ctx.send('Você não digitou nenhum valor!')
    if total > MAX_DADOS:
        return await ctx.send(f'O limite de dados atualmente é {MAX_DADOS}.')

    resultado = sistema.rolar(total)
    view = RolagemView(ctx, resultado)
    await ctx.send(
        content=''.join(resultado['emoji']),
        embed=criar_embed(ctx, resultado),
        view=view,
    )


@vr.error
async def vr_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply('VALOR INVÁLIDO!')


bot.run(DISCORD_TOKEN)