import psycopg2

class AppBD:
    def __init__(self):
        print('metodo constructor')
    
    def abrirConexao(self):
        # ----------- ERRORS DE CONECTIONS -------- #
        self.ERROR_CONNECT_BD = 'Error ao se conectar com ao banco de dados ------> '
        self.ERROR_SELECT = 'Error ao selecionar registro ------> '
        self.ERROR_INSERT = 'Error ao inserir registro ------> '
        self.ERROR_UPDATE = 'Error ao atualizar Registro! --------> '
        self.ERROR_DELETE = 'Error ao deletar Registro! --------> '

        # ----------- VAR EM COMM ---------- #
        self.CONNECTION_CLOSE = 'A conexão com o pg foi fechada!'

        # ----------- CONFIG CONECTION ------------ #
        DATABASE = 'Estacio'
        HOST = 'localhost'
        PORT = '5432'
        USER = 'postgres'
        PASS = 'postgres'

        try:
            self.connection = psycopg2.connect(
                user= USER, password= PASS, host= HOST, port= PORT, database= DATABASE
            )
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print(self.ERROR_CONNECT_BD, error)

    #-------------------------------------------------------------------------------------
    #---------------------------- SELECIONAR TODOS OS PRODUTOS ---------------------------
    #-------------------------------------------------------------------------------------

    def selecionarProduto(self):
        try:
            self.abrirConexao
            cursor = self.connection.cursor()

            print("#------------- SELECT * FROM public.'PRODUTO' -------------#")
            queryAllProducts = '''SELECT * FROM public."PRODUTO"'''

            cursor.execute(queryAllProducts)
            registro = cursor.fetchall()
            print(registro)
        except (Exception, psycopg2.Error) as error:
            print(self.ERROR_SELECT, error)
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print(self.CONNECTION_CLOSE)
        return registro
    
    #-------------------------------------------------------------------------------------
    #---------------------------- INSERT DADOS NOS PRODUTOS ------------------------------
    #-------------------------------------------------------------------------------------

    def inserirDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            print("#------------- INSERT INTO public.'PRODUTO' -------------#")
            insert_produto = '''INSERT INTO public."PRODUTO" ("codigo", "nome", "preco")
                                VALUES (%s, %s, %s)"'''
            cursor.execute(insert_produto, (codigo, nome, preco))
            self.connection.commit()
            count = cursor.rowcount()

            print(count, " -------> Registros inseridos com sucesso! <---------")
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print(self.ERROR_INSERT, error)
        finally:
            cursor.close()
            self.connection.close()
            print(self.CONNECTION_CLOSE)
    
    #-------------------------------------------------------------------------------------
    #---------------------------- UPDATE DE DADOS EM UM PRODUTO --------------------------
    #-------------------------------------------------------------------------------------

    def atualizarDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            # ------------------- Registro antes da atualização -------- #
            selectWhereCodigo = '''SELECT * FROM public."PRODUTO" WHERE codigo = %s'''
            cursor.execute(selectWhereCodigo, (codigo))

            record = cursor.fetchone()
            print(record)

            # ------------------ Atualizar registro -------------------- #
            updateProduto = '''UPDATE public."PRODUTO" SET "nome"= %s, "preco"= %s WHERE codigo = %s'''
            cursor.execute(updateProduto, (nome, preco, codigo))

            self.connection.commit()
            count = cursor.rowcount()
            print(count ," <----------------- Registro Atualizado com sucesso!")

            # ------------------- Registro depois da atualização -------- #
            cursor.execute(selectWhereCodigo, (codigo))
            record2 = cursor.fetchone()
            print(record2)

        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print(self.ERROR_UPDATE, error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print(self.CONNECTION_CLOSE)

    #-------------------------------------------------------------------------------------
    #---------------------------- UPDATE DE DADOS EM UM PRODUTO --------------------------
    #-------------------------------------------------------------------------------------

    def deletarDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            deleteWhereCodigo = '''DELETE FROM public."PRODUTO" WHERE codigo = %s'''
            cursor.execute(deleteWhereCodigo, (codigo))

            self.connection.commit()
            count = cursor.rowcount()

            print(count , '<----------------- Registro Deletado com sucesso!')
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print(self.ERROR_DELETE, error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print(self.CONNECTION_CLOSE)
