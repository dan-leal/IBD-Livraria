#!/usr/bin/env python
# an example how to use Faker to create fake data and inject them
# in a mysql database

import time
import os
from datetime import date, datetime, timedelta
import decimal
import random
import mysql.connector
from mysql.connector import Error
from faker import Faker
Faker.seed(0)

fake = Faker()

create_table_autor = """
CREATE TABLE `autor` (
	`autor_id` int(11) NOT NULL AUTO_INCREMENT,
    `autor_nome` VARCHAR(100) NOT NULL,
    `paisNasc` VARCHAR(100),
    `dataNasc` date NOT NULL,
    `notaBiografica` VARCHAR(400),
    PRIMARY KEY (`autor_id`)
);
"""


try:
    conn = mysql.connector.connect(host='localhost', database='livrariaDB',
                                   user='root', password='root')

    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_autor)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
        row = {}
        n = 0

        while n <= 100:
            n += 1
            autores = [fake.name(),
                       fake.country(),
                       fake.date_of_birth(minimum_age=18),
                       fake.text(max_nb_chars=300)
                       ]

            cursor.execute(' \
                INSERT INTO `autor` (autor_nome, paisNasc, dataNasc, notaBiografica) \
                VALUES ("%s", "%s", "%s", "%s"); \
                ' % (autores[0], autores[1], autores[2], autores[3]))

            if n % 100 == 0:
                print("Iteração Autores %s" % n)
                time.sleep(0.5)
                conn.commit()
except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if (conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()

create_table_editora = """
CREATE TABLE `editora` (
	`editora_id` int(11) NOT NULL AUTO_INCREMENT,
    `editora_nome` VARCHAR(50) NOT NULL,
    `telefone` VARCHAR(100) NOT NULL,
    `endereco` VARCHAR(200),
    KEY `idx_editora_id` (`editora_id`)
);
"""

Faker.seed(0)
fake = Faker()

# Editoras
try:
    conn = mysql.connector.connect(host='localhost', database='livrariaDB',
                                   user='root', password='root')

    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_editora)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
        row = {}
        n = 0

        while n <= 50:
            n += 1
            editora = [
                'Editora '+fake.name(),
                fake.phone_number(),
                fake.address()
            ]

            cursor.execute(' \
                      INSERT INTO `editora` (editora_nome, telefone, endereco) \
                      VALUES ("%s", "%s", "%s"); \
                      ' % (editora[0], editora[1], editora[2]))
            if n % 10 == 0:
                print("Iteração Editoras %s" % n)
                time.sleep(0.5)
                conn.commit()

except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if (conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()

# Edicao

create_table_edicao = """
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
"""


try:
    conn = mysql.connector.connect(host='localhost', database='livrariaDB',
                                   user='root', password='root')

    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_edicao)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
        row = {}
        n = 0

        while n <= 1000:
            n += 1

            edicao = [fake.isbn10(),
                      random.randint(1, 51),
                      fake.date_time_between(start_date='-19y'),
                      random.randint(0, 60),
                      float(random.uniform(10, 400)),
                      random.randint(1, 10000)
                      ]

            cursor.execute(' \
                INSERT INTO `edicao` (isbn, editora_id, edicao_ano, qt_estoque, preco, numPag) \
                VALUES ("%s", "%s", "%s", "%s", "%s", "%s"); \
                ' % (edicao[0], edicao[1], edicao[2], edicao[3], edicao[4], edicao[5]))

            if n % 100 == 0:
                print("Iteração Edição %s" % n)
                time.sleep(0.5)
                conn.commit()
except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if (conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()

# Livro

create_table_livro = """
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
"""
sql_query_edicao = "SELECT isbn,edicao_ano FROM edicao"

try:
    conn = mysql.connector.connect(host='localhost', database='livrariaDB',
                                   user='root', password='root')

    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_livro)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
        row = {}
        n = 0

        try:
            cursor.execute(sql_query_edicao)
            edicoes = cursor.fetchall()
            print("Encontradas todas as Edições")
        except Exception as e:
            print("Error query edicoes", e)

        while n <= 400:
            n += 1

            selecionada = edicoes[random.randint(1, 1000)]

            livro = [fake.catch_phrase(),
                     fake.language_name(),
                     fake.date_time_between(start_date=selecionada[1]),
                     selecionada[0]
                     ]

            cursor.execute(' \
                INSERT INTO `livro` (livro_nome, lingua, anoEscrito, isbn) \
                VALUES ("%s", "%s", "%s", "%s"); \
                ' % (livro[0], livro[1], livro[2], livro[3]))

            if n % 100 == 0:
                print("Iteração Livro %s" % n)
                time.sleep(0.5)
                conn.commit()
except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if (conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()

# Pertence

create_table_pertence = """
CREATE TABLE `pertence` (
	`livro_id` int(11) NOT NULL,
	`autor_id` int(11) NOT NULL,
  PRIMARY KEY (`livro_id` ,`autor_id`),
	FOREIGN KEY (`livro_id`) REFERENCES `livro` (`livro_id`) ON UPDATE CASCADE,
	FOREIGN KEY (`autor_id`) REFERENCES `autor` (`autor_id`) ON UPDATE CASCADE
);
"""

try:
    conn = mysql.connector.connect(host='localhost', database='livrariaDB',
                                   user='root', password='root')

    if conn.is_connected():
        cursor = conn.cursor()

        try:
            cursor.execute(create_table_pertence)
            print("Table created")
        except Exception as e:
            print("Error creating table", e)
        row = {}
        n = 0

        while n <= 100:
            n += 1

            pertence = [random.randint(1, 401),
                        random.randint(1, 101),
                        ]

            cursor.execute(' \
                INSERT INTO `pertence` (livro_id, autor_id) \
                VALUES ("%s", "%s"); \
                ' % (pertence[0], pertence[1]))

            if n % 100 == 0:
                print("Iteração Relação Autor-Livro %s" % n)
                time.sleep(0.5)
                conn.commit()
except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if (conn and conn.is_connected()):
        conn.commit()
        cursor.close()
        conn.close()
