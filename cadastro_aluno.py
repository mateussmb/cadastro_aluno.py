
import sqlite3
import tkinter as tk
from tkinter import ttk
from turtle import width


class PrincipalRAD:
    def __init__(self, win):
        #componentes
        self.lblNome=tk.Label(win, text='Nome do Aluno:')
        self.lblmateria=tk.Label(janela, text = "Matéria: ",
                        font = ("Times New Roman", 10))
        self.lblNota1=tk.Label(win, text='Nota 1')
        self.lblNota2=tk.Label(win, text='Nota 2')
        self.lblavd=tk.Label(win, text='AVD')
        self.txtNome=tk.Entry(bd=3)
        self.n = tk.StringVar()
        self.txtmateria= ttk.Combobox(janela, width = 27, textvariable = self.n)
        self.txtNota1=tk.Entry()
        self.txtNota2=tk.Entry() 
        self.txtavd=tk.Entry()       
        self.txtmateria['values'] = (' Português',
                    ' Matemática',
                    ' História',
                   ' Geografia',
                   ' Biologia',
                      ' Química ',
                      ' Filosofia',
                      ' Sociologia',
                  ' Física',
                  ' Artes',
                  ' Redação',
                   )
        
        self.btnCalcular=tk.Button(win, text='Cadastrar', command=self.cadastrar)
        
                
        #----- Componente TreeView --------------------------------------------
        self.dadosColunas = ("Aluno", "Nota1", "Nota2", "AVD" ,  "Média", "situação", "Matéria")            
        
        
        self.treeMedias = ttk.Treeview(win, 
                                       columns=self.dadosColunas,
                                       selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeMedias.yview)
        
        self.verscrlbar.pack(side ='right', fill ='x')
                
        
        
        self.treeMedias.configure(yscrollcommand=self.verscrlbar.set)
        
        self.treeMedias.heading("Aluno", text="Aluno")
        self.treeMedias.heading("Nota1", text="Nota 1")
        self.treeMedias.heading("Nota2", text="Nota 2")
        self.treeMedias.heading("AVD", text="AVD")
        self.treeMedias.heading("Média", text="Média")
        self.treeMedias.heading("situação", text="situação")
        self.treeMedias.heading("Matéria", text="Matéria")
        

        self.treeMedias.column("Aluno",minwidth=0,width=70)
        self.treeMedias.column("Nota1",minwidth=0,width=70)
        self.treeMedias.column("Nota2",minwidth=0,width=70)
        self.treeMedias.column("AVD",minwidth=0,width=70)
        self.treeMedias.column("Média",minwidth=0,width=70)
        self.treeMedias.column("situação",minwidth=0,width=70)
        self.treeMedias.column("Matéria",minwidth=0,width=70)

        self.treeMedias.pack(padx=10, pady=10)
                
        #---------------------------------------------------------------------        
        #posicionamento dos componentes na janela
        #---------------------------------------------------------------------        
        self.lblNome.place(x=100, y=50)
        self.txtNome.place(x=200, y=50)

        self.lblmateria.place(x=100, y=100)
        self.txtmateria.place(x=200, y=100, width=130)
        
        self.lblNota1.place(x=100, y=150)
        self.txtNota1.place(x=200, y=150)
        
        self.lblNota2.place(x=100, y=200)
        self.txtNota2.place(x=200, y=200)

        self.lblavd.place(x=100, y=250)
        self.txtavd.place(x=200, y=250)
               
        self.btnCalcular.place(x=100, y=300)
           
        self.treeMedias.place(x=100, y=400)
        self.verscrlbar.place(x=805, y=400, height=225)
        
        
        self.id = 0
        self.iid = 0

        
        



        
#-----------------------------------------------------------------------------
#Banco de dados em sqlite3
#-----------------------------------------------------------------------------          
    def salvarDados(self):
        try:
            nome = self.txtNome.get()
            nota1=self.txtNota1.get()
            nota2=self.txtNota2.get()
            materia = self.txtmateria.get()

            conn = sqlite3.connect('python/bd_cadastrar.db')
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS cadastramento(
                
                    nome TEXT, materia TEXT, nota1 TEXT, nota2 TEXT);
                    """)

            cursor.execute('  INSERT INTO cadastramento VALUES( ?, ?, ?, ?)', (nome,materia,nota1,nota2,)
                                
                                   )
            conn.commit()
            
            
            cursor.execute('SELECT * FROM cadastramento')
            linhas = cursor.fetchall()
            print('----- Detalhe dos Alunos -----')
            
            for linha in linhas:
                print(linha)

            print('O Banco de dados  foi um Sucesso.') 
        except sqlite3.Error as e:
            print(f'ERRO: ERRO {e} na criação do banco')

            
    def fVerificarSituacao(self,nota1, nota2, avd):
          media=(nota1+nota2+avd)/3
          if(media>=6.0):
             situacao = 'Aprovado'
          elif(media>=4.0):
              situacao = 'Recuperação'
          else:   
             situacao = 'Reprovado'
         
          return media, situacao
            
        
#-----------------------------------------------------------------------------
#Imprime os dados do aluno
#-----------------------------------------------------------------------------          
    def cadastrar(self):
      nome = self.txtNome.get()
      materia = self.txtmateria.get()
      if len(nome) == 0 or len(materia) == 0:
          print('Entre com valores válidos')  
      else:
          try:
            nome = self.txtNome.get()
            nota1=float(self.txtNota1.get())
            nota2=float(self.txtNota2.get())
            avd=float(self.txtavd.get())
            
            materia = self.txtmateria.get()
            media, situacao = self.fVerificarSituacao(nota1, nota2, avd)
            
                      
            
            self.treeMedias.insert('', 'end', 
                                  iid=self.iid,                                  
                                  values=(nome, 
                                          str(nota1),
                                          str(nota2),
                                          str(avd),
                                          str(media),
                                          situacao,
                                          materia))
            
            
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.salvarDados()
          except ValueError:
            print('Entre com valores válidos')        
          finally:
            
            self.txtNome.delete(0, 'end')
            self.txtmateria.delete(0, 'end')
            self.txtNota1.delete(0, 'end')
            self.txtNota2.delete(0, 'end')
             

#-----------------------------------------------------------------------------
#Programa Principal
#-----------------------------------------------------------------------------          

janela=tk.Tk()
principal=PrincipalRAD(janela)

janela.title('Cadastramento de aluno')
janela.geometry("820x600+10+10")
janela.mainloop()

