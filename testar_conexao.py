import pyodbc

# Dados de conexão
server = 'DISNAR\\SQLEXPRESS'
database = 'master'
username = 'DisnaR\\disna'

try:
    # Conexão com o banco de dados
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        'Trusted_Connection=yes;'
    )

    # Obtendo a versão do SQL Server
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    row = cursor.fetchone()
    print("Conexão bem-sucedida!")
    print("Versão do SQL Server:", row[0])
    conn.close()
except pyodbc.Error as e:
    print("Erro ao conectar ao banco de dados:", e)
