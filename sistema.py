import random


class Emojis:
    sucesso = '<:sucesso:1512846827962237121>'
    falha = '<:falha:1512846801290530948>'
    critico = '<:critico:1512846854608650311>'
    fcritica = '<:falhacritica:1512846843183104031>'

def _validar_dificuldade(dificuldade):
    if not isinstance(dificuldade, int) or isinstance(dificuldade, bool):
        raise ValueError('A dificuldade deve ser um inteiro entre 1 e 9.')
    if not 1 <= dificuldade <= 9:
        raise ValueError('A dificuldade deve estar entre 1 e 9.')


def rolar(dados):
    if not isinstance(dados, int) or isinstance(dados, bool) or dados < 1:
        raise ValueError('A quantidade de dados deve ser um inteiro positivo.')

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
    _validar_dificuldade(dificuldade)
    valores = list(valores)
    if not valores or any(
        not isinstance(valor, int)
        or isinstance(valor, bool)
        or not 1 <= valor <= 10
        for valor in valores
    ):
        raise ValueError('Os valores devem ser inteiros entre 1 e 10.')

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
    if not isinstance(rolagem, int) or isinstance(rolagem, bool):
        raise ValueError('A rolagem deve ser um inteiro entre 1 e 10.')
    if not 1 <= rolagem <= 10:
        raise ValueError('A rolagem deve estar entre 1 e 10.')
    _validar_dificuldade(valor_corte)

    corte = valor_corte
    fracasso = False
    falha = False
    critico = False
    sucesso = False

    if rolagem == 1:
        falha = True
        fracasso = True
        resultados_emoji = Emojis.fcritica
    elif rolagem >= corte:
        sucesso = True
        if rolagem == 10:
            resultados_emoji = Emojis.critico
            critico = True
        else:
            resultados_emoji = Emojis.sucesso

    elif rolagem < corte:
        falha = True
        resultados_emoji = Emojis.falha
    
    resultados = {
        'fracasso':fracasso,
        'critico':critico,
        'sucesso':sucesso,
        'emoji':resultados_emoji,
        'falha':falha
        }
    
    return resultados
        
