# Trabalho - PI1 LAD.PY

Repositorio para o Projeto Integrador 1 de Engenharia de Software.

## Descricao do Projeto

O LAD.PY e um sistema de votacao digital ficticio, feito para fins academicos. O sistema roda pelo terminal e usa Python com MySQL para cadastrar eleitores, candidatos, registrar votos, gerar protocolos, exibir resultados e manter logs de auditoria.

O projeto tambem usa a Cifra de Hill para criptografar CPF, chave de acesso e protocolo de votacao antes de salvar esses dados.

## Equipe de Desenvolvimento

- Joao Pedro Silveira de Souza (26009261)
- Luiz Gustavo Urias Vieira (26005065)
- Matheus Alves Kusuki de Almeida (26007007)
- Matheus Milanez da Silva ()
- Murilo Henrique de Oliveira Joaquim ()

## Tecnologias Utilizadas

- Python 3.x
- MySQL
- mysql-connector-python
- VSCode
- Git e GitHub

## Como Executar

1. Instale o Python 3.x.
2. Instale o MySQL.
3. Instale a biblioteca de conexao:

```bash
pip install mysql-connector-python
```

4. No MySQL, execute o arquivo `db/db-ladpy.sql` para criar o banco.
5. Confira usuario e senha em `db/conexao.py`.
6. Execute o sistema:

```bash
python main.py
```

## Observacoes

- Cadastre pelo menos um eleitor como mesario antes de abrir a votacao.
- A chave de acesso aparece apenas no momento do cadastro do eleitor.
- Os logs sao salvos no arquivo `logs_ocorrencias.txt`.
