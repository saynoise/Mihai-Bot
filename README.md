# Mihai-Bot

Bot de Discord para rolagens de dados com sucessos, falhas críticas, rerrolagem
de falhas e alteração de dificuldade.

## Requisitos

- Python 3.10 ou superior
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications)
- As intents necessárias ativadas no portal do Discord

## Instalação

Instale as dependências:

```bash
pip install discord.py python-dotenv
```

Crie um arquivo `.env` na raiz do projeto e informe o token do bot:

```env
DISCORD_TOKEN=seu_token_aqui
```

Nunca compartilhe o token nem faça commit do arquivo `.env`.

## Execução

Inicie o bot com:

```bash
python new_main.py
```

## Comando de rolagem

Use o prefixo `!` seguido da quantidade de dados:

```text
!vr 5
```

O bot rola os dados, exibe os resultados e calcula o resultado final. O limite
atual é de 65 dados por rolagem.

## Interações da rolagem

- **Rerolar Falhas**: rola novamente os dados abaixo da dificuldade atual e
  desativa o botão depois do uso.
- **Dificuldade**: abre um modal para informar uma dificuldade de 1 a 9. Os
  dados já rolados são recalculados com o novo valor, sem gerar novas rolagens.

Somente a pessoa que executou o comando pode usar os botões da mensagem. As
interações ficam disponíveis por cinco minutos.

## Estrutura

- `main.py`: inicialização do bot, comando e interações do Discord.
- `sistema.py`: rolagem, regras e cálculo da dificuldade.
- `main_old.py`: versão anterior do main antes de refatorar.