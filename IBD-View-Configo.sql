## Todas as informações relacionadas aos livros com maior quantidade de edições em estoque atualmente 
## - mostrando nome da editora, id da edição, título de livro e quantidade em estoque
select ED.editora_nome, E.isbn, L.livro_nome, E.qt_Estoque 
from editora ED, edicao E, Livro L
where L.isbn = E.isbn
order by qt_Estoque desc;

