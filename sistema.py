import random

class Emojis:
    sucesso = '<:sucesso:1512846827962237121>'
    falha = '<:falha:1512846801290530948>'
    critico = '<:critico:1512846854608650311>'
    fcritica = '<:falhacritica:1512846843183104031>'

def rolar(dados):
    fracassos = 0
    criticos = 0
    resultados = []
    resultados_emoji = []
    sucessos = 0

    for i in range(dados):
        rolagem = random.randint(1,10)
        resultados.append(rolagem)

        calculo_regras = regras(rolagem)

        if calculo_regras['fracasso']:
            fracassos += 1
        
        if calculo_regras['critico']:
            criticos += 1

        if calculo_regras['sucesso']:
            sucessos += 1

        resultados_emoji.append(calculo_regras['emoji']) 

    resultados = {
        'resultados':resultados,
        'fracassos':fracassos,
        'criticos':criticos,
        'sucessos':sucessos,
        'emoji':resultados_emoji
        }  
    
    return resultados

def alterar_dificuldade(valores, dificuldade):
    fracassos = 0
    criticos = 0
    resultados_emoji = []
    sucessos = 0

    for valor in valores:
        calculo_regras = regras(valor, dificuldade)

        if calculo_regras['fracasso']:
            fracassos += 1
        
        if calculo_regras['critico']:
            criticos += 1

        if calculo_regras['sucesso']:
            sucessos += 1

        resultados_emoji.append(calculo_regras['emoji']) 

    resultados = {
        'resultados':valores,
        'fracassos':fracassos,
        'criticos':criticos,
        'sucessos':sucessos,
        'emoji':resultados_emoji
        }  
    



def regras(rolagem, valor_corte=6):
    corte = valor_corte
    fracasso = False
    falha = False
    critico = False
    sucesso = False

    if rolagem >= corte:
        sucesso = True
        if rolagem == 10:
            resultados_emoji = Emojis.critico
            critico = True
        else:
            resultados_emoji = Emojis.sucesso

    if rolagem < corte:
        falha = True
        if rolagem == 1:
            fracasso = True
            resultados_emoji = Emojis.fcritica
        else:
            resultados_emoji = Emojis.falha
    
    resultados = {
        'fracasso':fracasso,
        'critico':critico,
        'sucesso':sucesso,
        'emoji':resultados_emoji,
        'falha':falha
        }
    
    return resultados
        
