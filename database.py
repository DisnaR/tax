import pyodbc

# Função para conectar-se ao banco de dados e inserir os dados do formulário
def insert_into_database(data):
    # Dados de conexão
    server = 'DISNAR\\SQLEXPRESS'
    database = 'master'
    username = 'DisnaR\\disna'

    # Conexão com o banco de dados
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        'Trusted_Connection=yes;'
    )

    # Inserindo os dados no banco de dados
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FormularioContato (Nome, Email, Departamento, Pergunta, Anexo) VALUES (?, ?, ?, ?, ?)",
                   data['nome'][0], data['email'][0], data['departamento'][0], data['pergunta'][0], data['anexo'][0])

    # Confirmar a transação
    conn.commit()

    # Fechar a conexão
    conn.close()

    print("Dados inseridos com sucesso no banco de dados.")

# Executar a função de inserção de dados se este script for executado diretamente
if __name__ == '__main__':
    # Aqui você pode testar a função insert_into_database()
    # inserindo manualmente alguns dados de exemplo
    data = {
        'nome': ['Exemplo'],
        'email': ['exemplo@example.com'],
        'departamento': ['Vendas'],
        'pergunta': ['Esta é uma pergunta de exemplo.'],
        'anexo': ['caminho/para/o/anexo']
    }
    insert_into_database(data)
