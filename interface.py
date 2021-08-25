import tkinter as TK
from tkinter import ttk
import crud as crud

class interface:
    def __init__(self, janela):
        print("--------------------- CONSTRUCTOR ---------------------")
        self.objeto_bd = crud.AppBD()

        #----------- COMPONENTES ----------- #
        self.label_codigo = TK.Label(janela,    text= "codigo do Produto")
        self.label_nome = TK.Label(janela,      text= "nome do Produto")
        self.label_preco = TK.Label(janela,     text= "preco do Produto")

        self.texto_codigo = TK.Entry(bd=3)
        self.texto_nome = TK.Entry()
        self.texto_preco = TK.Entry()

        # AS FUNCOES MEU JOVEM DOS COMANDOS DOS BTNS ESTAO LA EM BAIXO NA LINHA 114
        self.btn_cadastrar = TK.Button(janela,  text="CADASTRAR",   command= self.fn_cadastrar_produto)
        self.btn_atualizar = TK.Button(janela,  text="ATUALZIAR",   command= self.fn_atualizar_produto)
        self.btn_excluir = TK.Button(janela,    text="EXCLUIR",     command= self.fn_exluir_produto)
        self.btn_limpar = TK.Button(janela,     text="LIMPAR",      command= self.fn_limpar_tela)

        # O construtor ainda possui mais duas partes. Uma delas é responsável por instanciar e configurar o componente “TreeView”

        self.dados_column = ("Código", "Nome", "Preço")
        self.tree_produtos = ttk.Treeview(janela, columns= self.dados_column, selectmode= "browse")
        self.scrollbar = ttk.Scrollbar(janela, orient="vertical", command= self.tree_produtos.yview)
        self.scrollbar.pack(side="right", fill= 'x' )

        self.tree_produtos.configure(yscrollcommand = self.scrollbar.set)

        self.tree_produtos.heading("Código", text="Códido")
        self.tree_produtos.heading("Nome", text="Nome")
        self.tree_produtos.heading("Preço", text="Preço")

        self.tree_produtos.column("Código", minwidth= 0, width= 100)
        self.tree_produtos.column("Nome", minwidth= 0, width= 100)
        self.tree_produtos.column("Preço", minwidth= 0, width= 100)

        self.tree_produtos.pack(padx=10, pady=10)
        self.tree_produtos.bind("<<TreeviewSelect>>", self.apresentar_registros_selecionados)

        # O posicionamento dos elementos na janela

        # ------------- CODIGO ------------- #
        self.label_codigo.place(    x= 100, y= 50)
        self.texto_codigo.place(    x= 250, y= 50)
        # -------------- NOME -------------- #
        self.label_nome.place(      x= 100, y= 100)
        self.texto_nome.place(      x= 250, y= 100)
        # -------------- PRECO ------------- #
        self.label_preco.place(     x= 100, y= 150)
        self.texto_preco.place(     x= 250, y= 150)
        # ------------- BUTTON ------------- #
        self.btn_cadastrar.place(   x= 100, y= 200)
        self.btn_atualizar.place(   x= 200, y= 200)
        self.btn_excluir.place(     x= 300, y= 200)
        self.btn_limpar.place(      x= 400, y= 200)
        # ------------ TREEVIEW ------------ #
        self.tree_produtos.place(   x= 100, y= 300)
        self.scrollbar.place(       x= 805, y= 300, height= 225)

        self.carregar_dados_iniciais()

    # Esta function exibe os dados selecionados na grade (componente “TreeView”) nas caixas de texto, de modo que o usuário possa fazer alterações, ou exclusões sobre eles
    def apresentar_registros_selecionados(self, evento):
        self.fn_limpar_tela()
        for selection in self.tree_produtos.selection():
            item = self.tree_produtos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.texto_codigo.insert( 0, codigo)
            self.texto_nome.insert(   0, nome)
            self.texto_preco.insert(  0, preco)
    
    # Esta function carrega os dados que já estão armazenados na tabela para serem exibidos na grade de dados (componente “TreeView”)
    def carregar_dados_iniciais(self):
        try:
            self.id  = 0
            self.iid = 0
            registros = self.objeto_bd.selecionarProduto()
            print("-------------------------- DADOS DISPONIVEIS NO BD ------------------------------")
            for item in registros:
                codigo = item[0]
                nome   = item[1]
                preco  = item[2]

                # INSERIR NA TABELA TREEVIEW
                self.tree_produtos.insert('', 'end', iid= self.iid, values= ( codigo, nome, preco ))
                self.iid = self.iid + 1
                self.id  = self.id  + 1
            
            print("------------> DADOS DA BASE <------------- ")

        except:
            print('------------> AINDA NAO EXISTE DADOS PARA SEREM CARREGADOS <-----------')

    # Esta function lê os dados que estão nas caixas de texto e os retorna para quem faz a chamada.
    def fler_campos(self):
        try:
            print("*************** DADOS DISPONIVEIS ******************")
            codigo = int(self.texto_codigo.get()) # pegar o texto que esta no campo e converter para inteiro safe!
            nome   = self.texto_nome.get()
            preco  = float(self.texto_preco.get())# pegar o texto que esta no campo e converter para float "famoso ctrl + v da linha 102 kk" safe!

            print("-----------------> LEITURA DOS DADOS COM SUCESSO <-------------------")
            print('codigo --> '+ codigo,'\nnome ---> '+  nome,'\npreco --> '+  preco)
        except:
            print('NAO FOI POSSIBLE LER OS DADOS!')
        return codigo, nome, preco

    # Esta function tem como objetivo fazer a inserção dos dados na tabela “PRODUTOS”
    def fn_cadastrar_produto(self):
        try:
            print("*************** DADOS DISPONIVEIS ******************")
            # DESESTRUTURANDO kkkk O FLEX CAMPOS FUNCAO DE CIMA
            codigo, nome, preco = self.fler_campos()
            
            # LEMBRANDO QUE ESSE È O CRUD DO ARQUIVO CRUD.PY
            self.objeto_bd.inserirDados(codigo, nome, preco) # INSERT INTO public."PRODUTO" os campinhos basicos VALUES (codigo, nome, preco)
            
            # INSERINDO TBM NO NOSSO QUERIDA TABELINHA TREEVIEW
            self.tree_produtos.insert('', 'end', iid= self.iid, values= ( codigo, nome, preco ))
            self.iid = self.iid + 1
            self.id  = self.id  + 1

            self.fn_limpar_tela()
            print("------> PRODUTO CADASTRADO COM SUCESSO!!")
        except:
            print("NAO FOI POSSIVEL FAZER O CADASTRO")
    
    # ESSA FUNCTION SE JA TA LIGADO QUE VAI FAZER !!!!! brinks É atualizar os dados que o usuário selecionou na grade de dados
    def fn_atualizar_produto(self):
        try:
            print("*************** DADOS DISPONIVEIS ******************")
            codigo, nome, preco = self.fler_campos()

            #FILE CRUD.JS
            self.objeto_bd.atualizarDados(codigo, nome, preco)

            #CARREGAR DADOS NA TELA
            self.tree_produtos.delete(*self.tree_produtos.get_children())
            self.carregar_dados_iniciais()
            self.fn_limpar_tela()

            print("------> PRODUTO ATUALIZADO COM SUCESSO!!")
        except:
            print("NAO FOI POSSIVEL FAZER ATUALIZAÇÂO")

    #Essa function Excluir os dados que o usuário selecionou na grade de dados, aque menos gosto :)
    def fn_exluir_produto(self):
        try:
            print("*************** DADOS DISPONIVEIS ******************")
            codigo = self.fler_campos()
            #FILE CRUD.JS       
            self.objeto_bd.deletarDados(codigo)

            #CARREGAR DADOS NA TELA
            self.tree_produtos.delete(*self.tree_produtos.get_children())
            self.carregar_dados_iniciais()
            self.fn_limpar_tela()
            print("------> PRODUTO DELETADO COM SUCESSO!!")
        except:
            print(f"NAO FOI POSSIVEL DELETAR O PRODUTO COM O Nº{codigo}")


    #Esta function limpa o conteúdo das caixas de texto
    def fn_limpar_tela(self):
        try:
            print("*************** DADOS DOS CAMPOS ************")
            self.texto_codigo.delete(0, TK.END)
            self.texto_nome.delete(0, TK.END)
            self.texto_preco.delete(0, TK.END)
            print("*************** CAMPOS LIMPOS ***************")
        except:
            print("NAO FOI POSSIVEL LIMPAR OS CAMPOS")