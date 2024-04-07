import pyodbc

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

# Obtendo a versão do SQL Server
cursor = conn.cursor()
cursor.execute('SELECT @@VERSION')
row = cursor.fetchone()
print(row)
