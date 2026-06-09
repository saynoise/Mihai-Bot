class Emojis:
    sucesso = '<:sucesso:1512846827962237121>'
    falha = '<:falha:1512846801290530948>'
    critico = '<:critico:1512846854608650311>'
    fcritica = '<:falhacritica:1512846843183104031>'

def regras(rolagem):
    corte = 6
    fracasso = False
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
        }
    
    return resultados
        
