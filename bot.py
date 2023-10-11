import requests
import json
import time

def check_code(code, goal, template, last_record):
    baseUrl = 'https://api.openai.com/v1/chat/completions'
    
    chatMessages = []
    
    chatMessages.append({"role": "system", "content": 'Você é um programdor senior e irá avaliar o código e os registros sobre a tarefa para concluir.'})
    chatMessages.append({
        "role": "user", 
        "content": f'O código está correto e funcional para concluir a tarefa {goal}, o último registro de modificações são {last_record}: {str(code)}. No formato de sua resposta devolva apenas o objeto com as suas respostas dentro dos valores! {template}'
    })
    
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer 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'
    }

    body = {
        "messages": chatMessages,
        "max_tokens": 6000,
        "model": "gpt-4"
    }

    response = requests.post(baseUrl, headers=headers, json=body)
    responseJson = response.json()
 
    messageChatResult = responseJson['choices'][-1]['message']['content']
    messageChatResult = messageChatResult.replace("'", '"')
    messageChatResult = messageChatResult.replace("'", "")
    result = eval(messageChatResult)
    return result

def fix_code(task, code):
    baseUrl = 'https://api.openai.com/v1/chat/completions'
    
    chatMessages = []
    
    chatMessages.append({"role": "system", "content": 'Você é um programador e irá corrigir ou modificar o código a ser recebido.'})
    chatMessages.append({
        "role": "user", 
        "content": f'Me retorne apenas e unicamente o código com a seguite correção: {task}. {code}'
    })
    
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer XXX'
    }

    body = {
        "messages": chatMessages,
        "max_tokens": 5000,
        "model": "gpt-4"
    }
 
    response = requests.post(baseUrl, headers=headers, json=body)
    responseJson = response.json()
    
    result = responseJson['choices'][-1]['message']['content']
    
    return result

template = {'tarefa_concluida': 'Responda true ou false', 'modificacao_necessaria': 'Responda aqui oque precisa ser feito no código para finalizar a tarefa máximo 400 caracteres...'}
goal = 'Criar uma calculadora simples em pythom.'
code = 'print(1 + 1)'
last_record = 'Nenhum'


check_code_result = check_code(code=code, goal=goal, template=template, last_record=last_record)
print('Validação do código...')
print(check_code_result)

print('aguardando 10s')
time.sleep(10)

fixed = fix_code(code=code, task=check_code_result['modificacao_necessaria'])
print('Correção do código...')
print(fixed)

print('aguardando 10s')
time.sleep(10)

check_code_result = check_code(code=fixed, goal=goal, template=template, last_record=check_code_result['modificacao_necessaria'])
print('Validação do código novamente...')
print(check_code_result)

