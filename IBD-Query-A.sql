#(SELECT) Listar os nomes de todos os autores que têm edições 
#	de seus livros  publicados com uma determinada editora (id da editora dado como entrada).
Select A.autor_nome, L.livro_id, E.editora_id 
from autor A, pertence P, livro L, edicao E
where A.autor_id = P.autor_id and L.livro_id = P.livro_id 
and E.isbn=L.isbn 
and E.editora_id = 'XXX'