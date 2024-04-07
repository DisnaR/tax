SELECT 
    [ID],
    [Nome],
    [Email],
    [Departamento],
    [Pergunta],
    [Anexo],
    [NomeArquivo],
    CONVERT(varchar, Data_Solicitacao, 103) AS Data_Solicitacao_Brasileira,
    CONVERT(varchar, Data_Conclusao, 103) AS Data_Conclusao_Brasileira
FROM [master].[dbo].[FormularioContato];
