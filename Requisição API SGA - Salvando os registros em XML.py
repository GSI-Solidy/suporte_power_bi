import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Parâmetros de autenticação
token_usuario = 'Bearer 37ecb511c60b6ff90cb2fbbb22eb0e4575acc25a620429d434ad0a1b68120e831889536ea763d8ef6b08c0b85e822df89a32d8febb34f2fe6710232eb8af5b526f5ed9e2cc4e16a952684e9398d63551c71737c0b6b04f22575c2da8bbc3bd7ada5bde918a4712fd787d972596a24ab8eb88123d05151692232edaca62c4166aa2a84922e5c8ac4c31d956a7d9d84098'

# Parâmetros de filtragem e paginação
dias_antes = 30
data_emissao_inicial = (datetime.now() - timedelta(days=dias_antes)).strftime('%d/%m/%Y')
data_emissao_final = datetime.now().strftime('%d/%m/%Y')
inicio_paginacao = 0

# Endpoint que retorna a lista de registros
registros_url = 'https://api.hinova.com.br/api/sga/v2/listar/boleto-associado/periodo'

# Payload para a requisição
payload = {
    "data_emissao_inicial": data_emissao_inicial,
    "data_emissao_final": data_emissao_final,
    "inicio_paginacao": inicio_paginacao
}

# Cabeçalho da requisição
headers = {
    'Authorization': token_usuario,
    'Content-Type': 'application/json'
}

# Faz a primeira requisição para obter os registros
response = requests.post(registros_url, json=payload, headers=headers)
data = response.json()
print(data)
# Lista para armazenar os registros
boletos = []

# Continua fazendo requisições enquanto houver mais páginas
while 'boletos' in data:
    # Adiciona os registros da página atual à lista de boletos
    boletos += data['boletos']

    # Avança para a próxima página
    inicio_paginacao += 1
    payload['inicio_paginacao'] = inicio_paginacao

    # Faz uma nova requisição para obter os registros da próxima página
    response = requests.post(registros_url, json=payload, headers=headers)
    data = response.json()

# Cria o elemento raiz do XML
root = ET.Element('boletos')

# Cria um elemento para cada boleto e seus respectivos veículos
for boleto in boletos:
    boleto_xml = ET.SubElement(root, 'boleto')
    for key, value in boleto.items():
        if key == 'veiculos':
            veiculos_xml = ET.SubElement(boleto_xml, 'veiculos')
            for veiculo in value:
                veiculo_xml = ET.SubElement(veiculos_xml, 'veiculo')
                for veiculo_key, veiculo_value in veiculo.items():
                    veiculo_xml.set(veiculo_key, str(veiculo_value))
        else:
            boleto_xml.set(key, str(value))

    # Cria um elemento "valor_total" para cada boleto
    valor_total_xml = ET.SubElement(boleto_xml, 'valor_total')
    valor_total = 0.0
    valor_total_xml.text = str(valor_total)

# Salva os registros em um arquivo XML
caminho_arquivo = r'C:\Users\Solidy-TI\PycharmProjects\pythonProject\registros.xml'

with open(caminho_arquivo, 'wb') as f:
    f.write(ET.tostring(root))

