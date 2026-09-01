import pandas as pd
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

df = pd.read_csv("dados.csv", skiprows=1)

resultados = []

for cnpj in df.iloc[:, 0]:

    cnpj = str(cnpj).strip()

    print(f"Consultando: {cnpj}")

    url = f"https://api.cnpja.com/simples?taxId={cnpj}"

    headers = {
        "Authorization": api_key
    }

    resposta = requests.get(url, headers=headers)

    # Limite da API
    if resposta.status_code == 429:

        dados = resposta.json()

        ttl = dados.get("ttl", 30)

        print(f"⏳ Limite atingido. Aguardando {ttl} segundos...")

        time.sleep(ttl + 1)

        # tenta novamente
        resposta = requests.get(url, headers=headers)

    if resposta.status_code == 200:

        dados = resposta.json()

        simples = dados.get("simples", {}).get("optant")

        if simples is True:
            resultados.append("SIM")

        elif simples is False:
            resultados.append("NÃO")

        else:
            resultados.append("NÃO INFORMADO")

    else:

        print(f"❌ Erro {resposta.status_code}")
        resultados.append("ERRO")

df["Simples Nacional"] = resultados

df.to_csv("resultado.csv", index=False)

print("\n✅ Consulta finalizada!")