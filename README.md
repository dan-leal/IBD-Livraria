# IBD-Livraria

#Configurando no docker
 Pendente
## Criando o container do Banco
1. Rodar a imagem no docker (mysql image)
2. Adicionar enviroment key `MYSQL_ROOT_PASSWORD` para definir a senha root.
Agora criar a pasta que será salvo os arquivos do mysql.

```cmd
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -v D:\Arquivos\Desktop\mysql-arquivos:/var/lib/mysql -d -p 3306:3306 mysql:8.0
```

**Obs.**: é preciso utilizar o caminho dos dados que o banco salva após definir onde irei salvar os dados, sinalizado pelo "**:**" .
## Encontrando o IP do container

Agora ele está rodando na porta 3306, e precisamos do IP do nosso container.

Para adquirir ele utilize:
```shell
docker container inspect mysql-container
```

E procure o valor armazenado em IPAddress, no meu caso é 172.17.0.2.

## Para rodar o terminal de um container já executando

Para realizar isso utilizamos o comando abaixo:
```cmd
docker exec -it mysql-container bash
```

## Configurando o DBeaver

Inclua na string de conexão a opção "allowPublicKeyRetrieval=true":
````bash
jdbc:mysql://localhost:3306/db?allowPublicKeyRetrieval=true&useSSL=false
````

Para permitir que o DBeaver permita utilizar uma chave pública, é preciso definir as seguintes configurações.

1. Clique com o botão direito na sua conexão, escolha "Editar Conexão".
2. Na tela "Configurações de conexão" (tela principal), clique em "Editar configurações do driver".
3. Clique em "Propriedades da conexão".
4. Clique com o botão direito na área "propriedades do usuário" e escolha "Adicionar nova propriedade".
5. Adicione duas propriedades: "useSSL" e "allowPublicKeyRetrieval".

Defina seus valores como "false" e "true" clicando duas vezes na coluna "value".



# Iniciando o trabalho
Objetivo é implementar um banco com Livraria - (primeiro exercício) deve ter no mínimo 100 autores, 400 livros, 50 editoras e 1000 edições.
## Requisitos
1) Linguagem de programação compatível com o SGBDs escolhido (com driver disponível para a linguagem escolhida pela equipe)
2) Utilizar o template de artigo fornecido (limite de 12 páginas, sem alterar as fontes e espaçamento do template) para elaboração do relatório.
## Restrições

1) Não utilizar frameworks de persistência objeto-relacional.
2) Somente o MySQL ou PostGreSQL podem ser escolhidos para as implementações.
2) As equipes devem escolher implementar para o seu trabalho, somente 1 dos seguintes problemas descritos na segunda lista de exercícios.
	1. Loja de Peças (sexto exercício) - deve ter no mínimo 20 clientes, 100 pedidos e 200 mercadorias e 20 fornecedores de cada tipo.
	2. Livraria - (primeiro exercício) deve ter no mínimo 100 autores, 400 livros, 50 editoras e 1000 edições.
#### Descrição do problema:

LIVRARIA
Uma livraria mantém o cadastro de livros disponíveis para a venda. Para cada livro são armazenados código, nome, língua e ano em que foi escrito. Para os autores é mantido igualmente um cadastro que inclui nome, data de nascimento, pais de nascimento e uma breve nota biográfica.
Cada livro pode ter vários autores e para um mesmo autor podem existir vários livros cadastrados. Um autor pode estar incluído no cadastro ainda quando não exista um livro seu para venda.
As editoras são incluídas no cadastro a partir do seu nome, endereço, telefone. Uma editora pode estar cadastrada mesmo quando não existam livros editados por ela em venda.
Para um mesmo livro podem existir várias edições realizadas por editoras diferentes ou em anos diferentes. Cada edição tem um código (ISBN), preço, ano, número de páginas e quantidade em estoque.
Considere que um livro pode ser cadastrado se existe pelo menos uma edição do mesmo para venda.
## Metodologia

1. Implementar o esquema no SGBD.
2. Realizar o preenchimento do banco com os dados (a equipe deve desenvolver um programa/scripts para popular os dados, usando o driver do banco para acesso).
3. Executar as consultas determinadas (descritas a seguir).
4. A partir dos dados coletados, escrever o relatório.

## 1. Implementando o esquema no SGBD
### Modelo ER

![[Schema_Livraria-Página-2.drawio 5.png]]
### Esquema Relacional

Autor (<u>autor_id</u>, autor_nome, paisNasc, dataNasc, notaBiografica)
Pertence( #livro_id, #autor_id )
	Pertence [autor_id] = Autor[autor_id]
	Pertence [livro_id] = Livro[livro_id]
Livro(<u>livro_id</u>, lingua, anoEscrito, livro_nome, #isbn)
Edicao(<u>isbn</u>, preco, qt_estoque, edicao_ano, numPag, #editora_id)
	Livro [isbn] = Edicao [isbn]
Editora(<u>editora_id</u>, editora_nome, telefone, endereco)
	Edicao [editora_id] = Editora [editora_id]

Após criar o Modelo Entidade Relacionamento e transformá-lo para esquema relacional. Podemos criar o Schema no SGBD.
### Schema no SGBD

```mysql 8.0
DROP DATABASE IF EXISTS `LivrariaDB`;
CREATE DATABASE `LivrariaDB`;
USE `LivrariaDB`;

CREATE TABLE `editora` (
	`editora_id` int(11) NOT NULL AUTO_INCREMENT,
	`editora_nome` VARCHAR(50) NOT NULL,
	`telefone` VARCHAR(100) NOT NULL,
	`endereco` VARCHAR(200),
	KEY `idx_editora_id` (`editora_id`)
);

CREATE TABLE `edicao` (
	`isbn` VARCHAR(15) NOT NULL,
	`editora_id` int(11) NOT NULL AUTO_INCREMENT,
	`edicao_ano` DATE Not Null,
	`qt_estoque` int NOT NULL DEFAULT '0',
	`preco` DECIMAL(6,2) NOT NULL,
	`numPag` int,
	PRIMARY KEY (`isbn`),
	KEY `fk_editora_id` (`editora_id`),
	CONSTRAINT `fk_editora_id` FOREIGN KEY (`editora_id`) REFERENCES `editora` (`editora_id`) ON UPDATE CASCADE

);

CREATE TABLE `autor` (
	`autor_id` int(11) NOT NULL AUTO_INCREMENT,
	`autor_nome` VARCHAR(100) NOT NULL,
	`paisNasc` VARCHAR(100),
	`dataNasc` date NOT NULL,
	`notaBiografica` VARCHAR(400),
	PRIMARY KEY (`autor_id`)
);

CREATE TABLE `livro` (
	`livro_id` int(11) NOT NULL AUTO_INCREMENT,
	`livro_nome` VARCHAR(80) NOT NULL,
	`lingua` VARCHAR(20),
	`anoEscrito` date NOT NULL,
	`isbn` VARCHAR(15) NOT NULL,
	PRIMARY KEY (`livro_id`),
	KEY `fk_isbn` (`isbn`),
	CONSTRAINT `fk_isbn` FOREIGN KEY (`isbn`) REFERENCES `edicao` (`isbn`) ON UPDATE CASCADE
);

CREATE TABLE `pertence` (
	`livro_id` int(11) NOT NULL,
	`autor_id` int(11) NOT NULL,
	PRIMARY KEY (`livro_id` ,`autor_id`),
	FOREIGN KEY (`livro_id`) REFERENCES `livro` (`livro_id`) ON UPDATE CASCADE,
	FOREIGN KEY (`autor_id`) REFERENCES `autor` (`autor_id`) ON UPDATE CASCADE
);
```



## 2. Preenchimento do banco com os dados

Descrever no vídeo

## 3. Consultas SQL
(SELECT) Listar os nomes de todos os autores que têm edições de seus livros  publicados com uma determinada editora (id da editora dado como entrada).

```mysql
Select A.autor_nome, L.livro_id, E.editora_id 
from autor A, pertence P, livro L, edicao E
where A.autor_id = P.autor_id and L.livro_id = P.livro_id 
and E.isbn=L.isbn 
and E.editora_id = '1'
```

1. (SELECT) Dada uma palavra “XXX” dada como entrada, listar as informações das edições (número da edição, editora, título do livro e seu primeiro autor) que tenha a palavra dada no título do livro da edição.

```mysql
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
and L.livro_nome LIKE '%XXX%'
order by tab.livro_id,tab.autor_id
```

3. (SELECT) Dada uma string “XXX” dada como entrada, listar as informações das edições (id das edições, editoras, títulos dos livros) onde a string fornecida esteja presente no nome de pelo menos um dos autores dos livros.
    
4. (UPDATE) Atualizar a quantidade de estoque de todas as edições de livros de uma editora dada como entrada - aumentando em 20%.
    
5. (INSERT) Inserir uma nova edição de um livro que já existe, considerando que essa edição continua associada à editora anterior.

# Referências

- https://www.youtube.com/watch?v=hl55qULfHyU - 17/03 17:32
- https://www.youtube.com/watch?v=1Zpr1vX0wqk - 17/03 17:32
- https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html
- https://www.codeproject.com/Questions/5328479/Missing-index-constraint-for-an-SQL-table
- https://learnsql.com/blog/referential-constraints-foreign-keys-mysql/
- https://www.gleek.io/blog/er-model-cardinality
- https://www.overleaf.com/latex/templates/sbc-conferences-template/blbxwjwzdngr
- https://medium.com/@fifthfrankie/creating-a-basic-database-using-mysql-python-and-some-fake-data-3ef789859639
- https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
- https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python
- https://www.w3schools.com/python/ref_random_uniform.asp
- https://www.tutorialspoint.com/mysql-error-1452-cannot-add-or-a-child-row-a-foreign-key-constraint-fails
- https://stackoverflow.com/questions/12661999/get-raw-decimal-value-from-mysqldb-query
- https://dev.mysql.com/doc/refman/8.0/en/precision-math-expressions.html
- https://pynative.com/python-get-random-float-numbers/
- https://www.w3schools.com/python/module_random.asp
- https://gist.github.com/bmillemathias/f4ae3d8739b4b30c6d18164c4a70b7c2
- https://pynative.com/python-mysql-select-query-to-fetch-data/
- https://stackoverflow.com/questions/42640300/using-two-foreign-auto-increment-keys-as-composite-primary-key-in-another-table
- https://dba.stackexchange.com/questions/282922/mysql-set-column-on-first-appearance-of-value
- https://www.geeksforgeeks.org/mysql-partition-by-clause/
- https://dbfiddle.uk/l2PlRUF9
- https://navicat.com/en/company/aboutus/blog/1647-applying-select-distinct-to-one-column-only
