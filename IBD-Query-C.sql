-- (SELECT) Dada uma string “XXX” dada como entrada, 
-- listar as informações das edições (id das edições, editoras, títulos dos livros) 
-- onde a string fornecida esteja presente no nome de pelo menos um dos autores dos livros.

select E.isbn, ED.editora_id, ED.editora_nome, L.livro_id ,L.livro_nome
from edicao E, editora ED, livro L
where livro_id IN (select l.livro_id
from autor A, pertence P, livro l
where A.autor_nome like '%Michael%' and 
A.autor_id = P.autor_id and L.livro_id = P.livro_id 
)
