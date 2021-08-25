from faker import Faker
import psycopg2 as pg

# Conection com o pg
DATABASE = 'Estacio'
HOST = 'localhost'
PORT = '5432'
USER = 'postgres'
PASS = 'postgres'

try:
    conn = pg.connect(database = DATABASE, user = USER, password = PASS, host = HOST, port = PORT)
    print('Conectado com o banco!!')
except:
    print('Error ao tentar fazer conexao com o banco!')

cursor = conn.cursor()
fake = Faker('pt_BR')

n = 10
for i in range(n):
    codigo = i + 10
    nome = 'produto_'+str(i + 1)
    preco = fake.pyfloat(left_digits= 3, right_digits=2, positive = True, min_value=5, max_value= 1000)
    print(preco)
    print(nome)

    insertInto = '''INSERT INTO public."PRODUTO" ("codigo", "nome", "preco")
                    VALUES (%s, %s, %s)'''
    registro = (codigo, nome, preco)
    cursor.execute(insertInto, registro)

conn.commit()
print('Insert Concluido')
conn.close()
