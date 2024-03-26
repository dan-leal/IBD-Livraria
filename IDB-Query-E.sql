-- neste exemplo o livro que já existe tem isbn 0-18-338464-4 e
-- a partir dessa variável que eu posso adquirir a editora a qual o livro pertence mas poderia ser livro_id também

select livro_id, livro_nome,L.isbn, editora_id from livro L, edicao E where L.isbn = '1-4524-3146-9' and E.isbn = L.isbn;

insert into edicao values (
'0-01-000001-1',
(select editora_id from livro L, edicao E where L.isbn = '1-4524-3146-9' and E.isbn = L.isbn),
'2024-01-01',
10,
100.00,
666);

select * from edicao E where isbn='0-01-000001-1';