import random

class Emojis:
    sucesso = '<:sucesso:1512846827962237121>'
    falha = '<:falha:1512846801290530948>'
    critico = '<:critico:1512846854608650311>'
    fcritica = '<:falhacritica:1512846843183104031>'

def rolar(dados):
    fracassos = 0
    criticos = 0
    lista_resultados = []
    sucessos = 0

    for i in range(dados):
        rolagem = random.randint(1,10)
        lista_resultados.append(rolagem)

        calculo_regras = regras(rolagem)

        if calculo_regras['fracasso']:
            fracassos += 1
        
        if calculo_regras['critico']:
            criticos += 1

        if calculo_regras['sucesso']:
            sucessos += 1
    
    resultado_final = (sucessos + criticos) - fracassos

    lista_resultados = sorted(lista_resultados, reverse=True)

    emojis_sorted = [regras(key)['emoji'] for key in lista_resultados]

    resultados = {
        'resultados':lista_resultados,
        'fracassos':fracassos,
        'criticos':criticos,
        'sucessos':sucessos,
        'emoji':emojis_sorted,
        'resultado_final':resultado_final
        }  
    
    return resultados

def alterar_dificuldade(valores, dificuldade):
    fracassos = 0
    criticos = 0
    sucessos = 0

    for valor in valores:
        calculo_regras = regras(valor, dificuldade)

        if calculo_regras['fracasso']:
            fracassos += 1
        
        if calculo_regras['critico']:
            criticos += 1

        if calculo_regras['sucesso']:
            sucessos += 1

    resultado_final = (sucessos + criticos) - fracassos

    valores = sorted(valores, reverse=True)

    emojis_sorted = [regras(key, dificuldade)['emoji'] for key in valores]

    resultados = {
        'resultados':valores,
        'fracassos':fracassos,
        'criticos':criticos,
        'sucessos':sucessos,
        'emoji':emojis_sorted,
        'resultado_final':resultado_final
        }  
    return resultados
    
def regras(rolagem:int, valor_corte=6):
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
        
