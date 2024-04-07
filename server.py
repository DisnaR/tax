import pyodbc  # Importa o módulo pyodbc para conexão com o banco de dados SQL Server
from http.server import BaseHTTPRequestHandler, HTTPServer  # Importa classes para criar um servidor HTTP
import os  # Importa o módulo os para lidar com caminhos de arquivos
import cgi  # Importa o módulo cgi para analisar dados de formulário HTML
from datetime import datetime  # Importa a classe datetime para trabalhar com datas e horas

# Função para inserir dados no banco de dados
def insert_into_database(data):
    # Estabelece conexão com o banco de dados SQL Server
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DISNAR\\SQLEXPRESS;'
                          'Database=master;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()  # Cria um cursor para executar consultas SQL

    try:
        # Extrair os dados do dicionário
        nome = data['nome'].value if 'nome' in data else ''
        email = data['email'].value if 'email' in data else ''
        departamento = data['departamento'].value if 'departamento' in data else ''
        pergunta = data['mensagem'].value if 'mensagem' in data else ''

        # Se houver um anexo, lê os dados binários e obtém o nome do arquivo
        if 'anexo' in data:
            anexo_data = data['anexo']
            anexo = anexo_data.file.read()  # Lê o conteúdo do anexo
            nome_anexo = anexo_data.filename  # Obtém o nome do arquivo
        else:
            anexo = None
            nome_anexo = None

        # Obtém a data e hora atual
        data_solicitacao = datetime.now()

        # Consulta SQL para inserir dados na tabela FormularioContato
        sql = "INSERT INTO dbo.FormularioContato (Nome, Email, Departamento, Pergunta, Anexo, NomeArquivo, Data_Solicitacao) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (nome, email, departamento, pergunta, anexo, nome_anexo, data_solicitacao)

        # Executando a consulta
        cursor.execute(sql, params)

        # Commit para salvar as alterações no banco de dados
        conn.commit()

        print("Dados inseridos com sucesso!")
    except pyodbc.Error as e:
        print("Erro ao inserir dados no banco de dados:", e)
    finally:
        # Fechando a conexão
        conn.close()

# Classe do manipulador do servidor
class RequestHandler(BaseHTTPRequestHandler):

    # Diretório base para arquivos estáticos
    STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

    # Manipulador para solicitações GET
    def do_GET(self):
        # Verificar se a solicitação é para um arquivo estático
        if self.path.startswith('/static/'):
            # Caminho relativo do arquivo estático solicitado
            path = self.path[8:]  # Remover '/static/' do caminho
            # Construir o caminho absoluto do arquivo estático
            file_path = os.path.join(self.STATIC_DIR, path)
            # Verificar se o arquivo existe
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Se sim, abrir e ler o arquivo
                with open(file_path, 'rb') as file:
                    # Definir o cabeçalho de resposta
                    self.send_response(200)
                    # Definir o tipo MIME com base na extensão do arquivo
                    _, ext = os.path.splitext(file_path)
                    self.send_header('Content-type', self.get_mime_type(ext))
                    self.end_headers()
                    # Enviar o conteúdo do arquivo
                    self.wfile.write(file.read())
            else:
                # Se o arquivo não for encontrado, enviar uma resposta 404
                self.send_error(404, 'File not found')
        else:
            # Se não for um arquivo estático, retornar o formulário HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')  # Definindo a codificação de caracteres
            self.end_headers()
            # Corpo da resposta
            html = """
            <html>
            <head>
                <title>Formulário de Contato</title>
                <style>
                    /* Definições de fonte */
                    body {
                        font-family: 'Unilever Shilling', sans-serif;
                    }

                    /* Estilização para a div contendo o logo */
                    #logo {
                        width: 100%; /* Define a largura da div como 100% da largura da página */
                        margin: 0 auto; /* Centraliza a div horizontalmente */
                    }

                    /* Estilo para a imagem do logo */
                    #logo img {
                        max-width: 100%; /* Define a largura máxima da imagem como 100% */
                        height: auto; /* Mantém a proporção da imagem */
                        display: block; /* Torna a imagem um bloco para permitir a aplicação de margens */
                        margin: 0 auto; /* Centraliza a imagem horizontalmente */
                    }

                    /* Estilização para o formulário */
                    #formulario {
                        width: 100%; /* Define a largura da div como 100% da largura da página */
                        margin: 0 auto; /* Centraliza a div horizontalmente */
                        max-width: 600px; /* Define uma largura máxima para o formulário */
                        padding: 0 20px; /* Adiciona um preenchimento interno */
                        box-sizing: border-box; /* Inclui padding e borda na largura total */
                    }

                    /* Estilo para o título do formulário */
                    h2 {
                        text-align: center; /* Centraliza o texto horizontalmente */
                    }

                    /* Estilização para as colunas */
                    .colunas {
                        display: flex;
                        flex-wrap: wrap;
                    }

                    /* Estilização para as colunas */
                    .coluna {
                        flex: 1;
                        margin-right: 20px; /* Adiciona espaçamento entre as colunas */
                    }

                    /* Estilização específica para a coluna de mensagem */
                    .mensagem {
                        flex: 2; /* Define uma largura maior para a coluna de mensagem */
                    }

                    /* Estilização para os labels */
                    label {
                        display: block; /* Faz com que os labels ocupem uma linha inteira */
                        margin-bottom: 5px; /* Adiciona espaçamento entre os labels */
                    }

                    /* Estilização para os inputs, selects e textarea */
                    input[type="text"],
                    input[type="email"],
                    select,
                    textarea {
                        width: 100%; /* Garante que os inputs, selects e textarea ocupem toda a largura da coluna */
                        padding: 5px;
                        margin-bottom: 10px; /* Adiciona espaçamento entre os inputs, selects e textarea */
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        box-sizing: border-box; /* Garante que o padding não aumente a largura dos inputs */
                    }

                    /* Estilização para o botão */
                    button {
                        width: 100%; /* Faz o botão ocupar toda a largura disponível */
                        background-color: #020951;
                        color: #ffffff;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }

                    /* Efeito de hover para o botão */
                    button:hover {
                        background-color: #2f3fe7;
                        color: #fff;
                        border: 1px solid #020951;
                    }

                    /* Mídia para telas menores que 768px (tablet) */
                    @media (max-width: 768px) {
                        #formulario {
                            padding: 0 10px; /* Reduz o preenchimento interno */
                        }
                        .coluna {
                            flex: 100%; /* Define as colunas para ocupar 100% da largura disponível */
                            margin-right: 0; /* Remove a margem direita */
                        }
                        .mensagem {
                            flex: 100%; /* Define a coluna de mensagem para ocupar 100% da largura disponível */
                        }
                    }
                </style>
            </head>
            <body>
            <div id="logo">
                <img src="/static/Logo_Unilever.jpeg" alt="Logo Unilever">
            </div>

            <div id="formulario">    
                <h2>Formulário de Contato</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <div class="colunas">
                        <div class="coluna">
                            <label for="nome">Nome:</label>
                            <input type="text" id="nome" name="nome" required>
                        </div>
                        <div class="coluna">
                            <label for="email">E-mail:</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="coluna">
                            <label for="departamento">Departamento:</label>
                            <select id="departamento" name="departamento" required>
                                <option value="Vendas">Vendas</option>
                                <option value="Suporte">Suporte</option>
                                <option value="Financeiro">Financeiro</option>
                                <option value="Recursos Humanos">Recursos Humanos</option>
                            </select>
                        </div>
                    </div>
                    <div class="colunas">
                        <div class="coluna mensagem">
                            <label for="mensagem">Mensagem:</label>
                            <textarea id="mensagem" name="mensagem" rows="6" required></textarea> <!-- Ajuste do número de linhas -->
                        </div>
                        <div class="coluna">
                            <label for="anexo">Anexo:</label>
                            <input type="file" id="anexo" name="anexo">
                        </div>
                    </div>
                    <div class="coluna">
                        <button type="submit">Enviar</button>
                    </div>
                </form>
            </div>
            </body>
            </html>
            """
            # Enviando a resposta
            self.wfile.write(html.encode('utf-8'))

    # Manipulador para solicitações POST
    def do_POST(self):
        # Analisar os dados da solicitação
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})

        # Conectando-se ao banco de dados e inserindo os dados
        insert_into_database(form)

        # Enviando uma resposta de sucesso ao cliente
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')  # Definindo a codificação de caracteres
        self.end_headers()
        self.wfile.write(bytes('Formulário enviado com sucesso!', 'utf-8'))

    # Função para obter o tipo MIME com base na extensão do arquivo
    def get_mime_type(self, ext):
        mime_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
        }
        return mime_types.get(ext.lower(), 'application/octet-stream')

# Função principal para iniciar o servidor
def main():
    try:
        # Criando uma instância do servidor
        server = HTTPServer(('localhost', 8000), RequestHandler)
        print('Servindo HTTP na porta 8000...')
        # Mantendo o servidor em execução
        server.serve_forever()
    except KeyboardInterrupt:
        # Fechar o servidor quando CTRL+C for pressionado
        print('^C recebido, fechando o servidor...')
        server.socket.close()

if __name__ == '__main__':
    main()
