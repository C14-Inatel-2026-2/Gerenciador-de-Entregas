from flask import Flask
import customtkinter as ctk
from tkinter import messagebox
from gestao_frotas.modelos import *

from gestao_frotas.modelos.entrega import Entrega

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "Gerenciador de Entregas rodando com sucesso!"}

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Entregas")
        self.geometry("600x600")
        self.resizable(True, True)

        self.historico_entregas = []
        self.mostrar_tela_inicial()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self, text="Controle de Entregas", font=("Arial", 20, "bold"))
        titulo.pack(pady=40)

        btn_cadastrar_entrega = ctk.CTkButton(
            self,
            text="Cadastrar Entrega",
            command=self.mostrar_tela_cadastro,
            font=("Arial", 14),
            height=40
        )
        btn_cadastrar_entrega.pack(pady=10)

    def mostrar_tela_cadastro(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self, text="Nova Entrega", font=("Arial", 16, "bold"))

        self.input_codigo = ctk.CTkEntry(self, placeholder_text="Código da Entrega", width=280, height=35)
        self.input_codigo.pack(pady=8)

        self.input_origem = ctk.CTkEntry(self, placeholder_text="Endereço de Origem", width=280, height=35)
        self.input_origem.pack(pady=8)

        self.input_destino = ctk.CTkEntry(self, placeholder_text="Endereço de Destino", width=280, height=35)
        self.input_destino.pack(pady=8)

        self.input_peso = ctk.CTkEntry(self, placeholder_text="Peso da Entrega (Kg)", width=280, height=35)
        self.input_peso.pack(pady=8)

        btn_salvar = ctk.CTkButton(
            self,
            text="Salvar e Cadastrar Entrega",
            command=self.salvar_dados,
            fg_color="green",
            hover_color="darkgreen",
            height=35
        )
        btn_salvar.pack(pady=12)

        btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="gray",
            hover_color="darkgray",
            height=30
        )
        btn_voltar.pack(pady=12)

    def salvar_dados(self):
        destino = self.input_destino.get().strip()
        origem = self.input_origem.get().strip()
        id = self.input_codigo.get().strip()
        peso = int(self.input_peso.get().strip())

        if not destino or not origem or not id or not peso:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

        nova_entrega = Entrega(id, origem, destino, peso)
        self.historico_entregas.append(nova_entrega)

        messagebox.showinfo("Sucesso", "Entrega Cadastrada com sucesso!")
        print(nova_entrega)
        self.mostrar_tela_inicial()

if __name__ == "__main__":
    app = App()
    app.mainloop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)