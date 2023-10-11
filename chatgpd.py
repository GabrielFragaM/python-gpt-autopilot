import requests
import json
import random

def generate_animal_info():
    return {
        "tamanho": random.randint(50, 150),
        "vida": random.randint(50, 150),
        "fome": random.randint(0, 100),
        "energia": random.randint(50, 150),
        "ataque": random.randint(10, 70),
        "defesa": random.randint(10, 70)
    }

def next_round(your_animal, other_animal):
    baseUrl = 'https://api.openai.com/v1/chat/completions'
    print('Iniciando integração com o chatgpt-3.5-turbo-16k')
    
    chatMessages = []
    
    chatMessages.append({"role": "assistant", "content": 'Você é um animal escolha uma das opções que ajude a você ganhar mais energia e diminuir a fome.'})
    chatMessages.append({
        "role": "user", 
        "content": f'Informações sobre você: Tamanho atual: {your_animal["tamanho"]}/150 Vida atual: {your_animal["vida"]}/150 Fome atual: {your_animal["fome"]}/100 Energia atual: {your_animal["energia"]}/100 Ataque: {your_animal["ataque"]}/70 Defesa: {your_animal["defesa"]}/70 Informações Animal Próximo: Vida atual: {other_animal["vida"]}/150 Fome atual: {other_animal["fome"]}/100 Energia atual: {other_animal["energia"]}/100 Ataque: {other_animal["ataque"]}/70 Defesa: {other_animal["defesa"]}/70 Considerações: Se você ficar com 100/100 de fome você perde -5 a cada rodada de vida! Escolha uma das opções: A: Atacar animal próximo perde -60 de energia. B: Buscar comida perde -35 de energia. Reponda somenta "A" ou "B" de acordo com suas informações!'
    })
    
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer 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'
    }

    body = {
        "messages": chatMessages,
        "max_tokens": 4000,
        "model": "gpt-4"
    }

    response = requests.post(baseUrl, headers=headers, json=body)
    responseJson = response.json()
   
    messageChatResult = responseJson['choices'][-1]['message']['content']
    
    return messageChatResult

def update_animal_stats(your_animal, other_animal, decision):
    if decision == "A":  # Atacar animal próximo
        energy_gain = random.randint(0, other_animal["energia"])
        your_animal["energia"] = min(your_animal["energia"] + energy_gain, 100)  # Respeitando o limite máximo de 100
        hunger_reduction = random.randint(0, other_animal["tamanho"])
        your_animal["fome"] = max(your_animal["fome"] - hunger_reduction, 0)  # Respeitando o limite mínimo de 0
    elif decision == "B":  # Buscar comida
        energy_change = random.randint(-20, 20)
        your_animal["energia"] = min(max(your_animal["energia"] + energy_change, 0), 100)  # Respeitando os limites de 0 e 100
        hunger_change = random.randint(-20, 20)
        your_animal["fome"] = min(max(your_animal["fome"] + hunger_change, 0), 100)  # Respeitando os limites de 0 e 100

    # Se a fome atingir 100, o animal perde vida
    if your_animal["fome"] >= 100:
        your_animal["vida"] -= 5

    return your_animal


def game():
    your_animal = generate_animal_info()
    for _ in range(1):
        other_animal = generate_animal_info()
        decision = next_round(your_animal, other_animal)
        print('Animal atual ----')
        print(your_animal)
        print('Animal mais proximo ----')
        print(other_animal)
        # Update animal stats based on decision
        your_animal_update = update_animal_stats(your_animal, other_animal, decision)
        print('Animal atual depois da ação----')
        print(your_animal_update)

game()

