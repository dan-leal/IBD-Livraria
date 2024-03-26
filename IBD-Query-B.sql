#(SELECT) Dada uma palavra “XXX” dada como entrada, 
#	listar as informações das edições (número da edição, editora, título do livro e seu primeiro autor)
# 	que tenha a palavra dada no título do livro da edição.

-- primeiro cria uma tabela onde utiliza o critério livro_id para separar grupos ordenados pelo autor_id
select ROW_NUMBER() OVER (PARTITION BY livro_id order by autor_id) as rn, livro_id, autor_id
from pertence
order by livro_id, autor_id;

-- pego o restande das informações necessárias para atender a solicitação do SELECT
select L.isbn, E.editora_id, ED.editora_nome, L.livro_nome, A.autor_nome from 
livro L, edicao E, editora ED, autor A Inner Join
(
	select ROW_NUMBER() OVER (PARTITION BY livro_id order by autor_id) as primeiroAutor, livro_id, autor_id
	from pertence
	-- order by livro_id, autor_id;
) as tab
where primeiroAutor = 1
and tab.autor_id = A.autor_id
and tab.livro_id = L.livro_id
and L.isbn = E.isbn
and E.editora_id = ED.editora_id
and L.livro_nome LIKE '%Hori%'
order by tab.livro_id,tab.autor_id