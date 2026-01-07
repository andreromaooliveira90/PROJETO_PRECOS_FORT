import requests
import pandas as pd
from datetime import datetime
import time
import os
import sys

# === AJUSTE DE CAMINHO PARA IMPORTAÇÃO ===
# Adiciona a pasta raiz do projeto ao PATH do sistema para encontrar a pasta 'config'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_do_projeto = os.path.abspath(os.path.join(diretorio_atual, ".."))
sys.path.append(raiz_do_projeto)

# Importar configurações da pasta config/
from config.config_url import CEP_PADRAO, LOJA_FIXA, CATEGORIAS

# ==============================
# FUNÇÕES
# ==============================

def criar_sessao():
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    return sess


def buscar_produtos_api(sessao, url):
    resp = sessao.get(url)
    resp.raise_for_status()
    return resp.json()


def extrair_campos_produtos(lista_produtos, categoria_nome):
    resultados = []
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for prod in lista_produtos:
        try:
            nome = prod.get("productName")
            link_text = prod.get("linkText")
            if not nome or not link_text:
                continue

            link_produto = f"https://www.deliveryfort.com.br/{link_text}/p"

            items = prod.get("items") or []
            if items:
                sellers = items[0].get("sellers") or []
                if sellers:
                    offer = sellers[0].get("commertialOffer") or {}
                    preco = offer.get("Price")
                else:
                    preco = None
            else:
                preco = None

            if preco is None:
                continue

            resultados.append({
                "loja": LOJA_FIXA,
                "cep": CEP_PADRAO,
                "categoria_bloco": categoria_nome,
                "nome_produto": nome,
                "preco": preco,
                "link_produto": link_produto,
                "data_coleta": agora,
            })
        except Exception:
            continue

    return resultados


def salvar_csv_append(produtos, nome_arquivo):
    if not produtos:
        print(f"   Nenhum produto para salvar.")
        return

    # === AJUSTE DE CAMINHO PARA SALVAMENTO ===
    # Define o caminho para PROJETO_PRECOS_FORT/data/raw/
    pasta_destino = os.path.join(raiz_do_projeto, "data", "raw")
    
    # Cria a pasta se ela não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    df_novo = pd.DataFrame(produtos)

    try:
        # Tenta ler o arquivo existente
        df_antigo = pd.read_csv(caminho_completo)
        df_total = pd.concat([df_antigo, df_novo], ignore_index=True)
        print(f"   Adicionando {len(df_novo)} registros ao histórico em data/raw.")
    except FileNotFoundError:
        # Se não existir, cria um novo
        df_total = df_novo
        print(f"   Criando novo histórico em data/raw.")

    df_total.to_csv(caminho_completo, index=False, encoding="utf-8-sig")
    print(f"   Arquivo atualizado: {nome_arquivo}")


# ==============================
# FLUXO PRINCIPAL
# ==============================

def main():
    print("=== INÍCIO DA COLETA (ESTRUTURA PROFISSIONAL) ===\n")
    sessao = criar_sessao()

    for categoria_nome, url_api in CATEGORIAS.items():
        print(f"=== CATEGORIA: {categoria_nome} ===")
        
        try:
            # Buscar produtos
            lista_produtos = buscar_produtos_api(sessao, url_api)
            print(f"   Produtos retornados pela API: {len(lista_produtos)}")
            
            # Extrair campos
            produtos_tratados = extrair_campos_produtos(lista_produtos, categoria_nome)
            print(f"   Produtos processados: {len(produtos_tratados)}")
            
            # Gerar nome do arquivo
            arquivo_csv = f"precos_fort_{categoria_nome.lower().replace(' ', '_')}_historico.csv"
            
            # Salvar usando a nova lógica de caminhos
            salvar_csv_append(produtos_tratados, arquivo_csv)
            
        except Exception as e:
            print(f"   ERRO ao processar {categoria_nome}: {e}")
        
        print() 
        time.sleep(1) 

    print("=== COLETA FINALIZADA ===")


if __name__ == "__main__":
    main()