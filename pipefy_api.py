import requests

# Configurações
PIPEFY_API_URL = "https://api.pipefy.com/graphql"
ACCESS_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MzI4MTA3NDYsImp0aSI6IjVmMzVlMTFhLTY4MTUtNDBlYy1iMmMyLTNkMjU4ZTE2MzI0MiIsInN1YiI6MzA1MDI1MDcxLCJ1c2VyIjp7ImlkIjozMDUwMjUwNzEsImVtYWlsIjoiY2FkYXN0cm9Ad2FwLmluZC5iciJ9fQ.Qcm9-JJt5_gbcqFMhi4rwrgmFfuELKMqqXSGDDP2AthwjMRLAXuB2QYS3LeETg-82wZ25Xr9xJ0o6j_HZbwdDA"  # Substitua pelo seu token de acesso
DATABASE_ID = "2GHP4QTV"  # Substitua pelo ID da tabela que você deseja consultar

# Função para buscar todos os registros de uma database específica
def buscar_todos_registros(database_id):
    query_template = """
    query ($table_id: ID!, $after: String) {
      table_records(table_id: $table_id, first: 50, after: $after) {
        edges {
          node {
            id
            title
            record_fields {
              name
              value
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    all_records = []  # Lista para armazenar todos os registros
    has_next_page = True
    after_cursor = None
    
    while has_next_page:  # Continue enquanto houver próximas páginas
        variables = {
            "table_id": database_id,
            "after": after_cursor
        }
        
        # Enviar a requisição para a API
        response = requests.post(PIPEFY_API_URL, json={"query": query_template, "variables": variables}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Debugging: Mostra a resposta completa no terminal para análise
            print("Resposta completa da API:", data)
            
            if "errors" in data:
                print("Erros ao buscar registros:", data["errors"])
                break
            else:
                # Extrair registros retornados nesta página
                records = data["data"]["table_records"]["edges"]
                for record in records:
                    registro = {"ID": record['node']['id'], "Título": record['node']['title']}
                    for field in record['node']['record_fields']:
                        registro[field['name']] = field['value']
                    all_records.append(registro)  # Adiciona o registro à lista
                
                # Atualizar informações de paginação
                has_next_page = data["data"]["table_records"]["pageInfo"]["hasNextPage"]
                after_cursor = data["data"]["table_records"]["pageInfo"]["endCursor"]
        else:
            print(f"Erro ao conectar à API: {response.status_code}, {response.text}")
            break
    
    return all_records

# Executa a busca na tabela específica
if __name__ == "__main__":
    print(f"Buscando todos os registros da tabela com ID: {DATABASE_ID}")
    registros = buscar_todos_registros(DATABASE_ID)
    if registros:
        print(f"\nTotal de registros encontrados: {len(registros)}")
        for registro in registros:
            print(registro)
    else:
        print("Nenhum registro encontrado ou houve um erro na consulta.")
