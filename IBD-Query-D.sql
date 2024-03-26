-- (UPDATE) Atualizar a quantidade de estoque de todas as edições de livros 
-- 	de uma editora dada como entrada - aumentando em 20%.
-- no exemplo a entrada é 6

SELECT isbn,qt_Estoque from edicao E where editora_id = '6';
-- verificar o atual e o esperado
SELECT E.isbn,E.qt_Estoque as qtEstoqueAntigo, Round(E.qt_Estoque*0.2 + E.qt_Estoque,0) as novoQt from edicao E where editora_id = '6';

update edicao E
set qt_Estoque = Round(E.qt_Estoque*0.2 + E.qt_Estoque,0)
where editora_id = '6';

-- confirma o esperado
SELECT isbn,qt_Estoque from edicao E where editora_id = '6';