import customtkinter as ctk
from tkinter import messagebox

from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.servicos.calculador_custo import CalculadorCusto
from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel
from gestao_frotas.excecoes import DadoInvalidoException

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ProvedorPrecoFixo(ProvedorCombustivel):
    def __init__(self, preco):
        self.preco = preco

    def preco_por_litro(self, uf):
        return self.preco


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

        btn_calcular_custo = ctk.CTkButton(
            self,
            text="Calcular Custo da Viagem",
            command=self.mostrar_tela_custo,
            font=("Arial", 14),
            height=40
        )
        btn_calcular_custo.pack(pady=10)

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

    def mostrar_tela_custo(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self, text="Calcular Custo da Viagem", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)

        self.input_distancia = ctk.CTkEntry(self, placeholder_text="Distância (km)", width=280, height=35)
        self.input_distancia.pack(pady=8)

        self.input_consumo = ctk.CTkEntry(self, placeholder_text="Consumo do veículo (km/l)", width=280, height=35)
        self.input_consumo.pack(pady=8)

        self.input_custo_km = ctk.CTkEntry(self, placeholder_text="Custo por km (R$)", width=280, height=35)
        self.input_custo_km.pack(pady=8)

        self.input_preco_litro = ctk.CTkEntry(self, placeholder_text="Preço do litro (R$)", width=280, height=35)
        self.input_preco_litro.pack(pady=8)

        btn_calcular = ctk.CTkButton(
            self,
            text="Calcular Custo",
            command=self.calcular_custo,
            fg_color="green",
            hover_color="darkgreen",
            height=35
        )
        btn_calcular.pack(pady=12)

        btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="gray",
            hover_color="darkgray",
            height=30
        )
        btn_voltar.pack(pady=12)

    def calcular_custo(self):
        try:
            distancia = float(self.input_distancia.get().strip())
            consumo = float(self.input_consumo.get().strip())
            custo_km = float(self.input_custo_km.get().strip())
            preco_litro = float(self.input_preco_litro.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos com números válidos.")
            return

        rota = Rota("Origem", "Destino", distancia, 1.0)
        veiculo = Veiculo(1, "", "", 9999, consumo, custo_km, "")
        calculador = CalculadorCusto(ProvedorPrecoFixo(preco_litro))

        try:
            custo_combustivel = calculador.calcular_custo_combustivel(rota, veiculo, "MG")
            custo_distancia = calculador.custo_por_distancia(rota, veiculo)
        except DadoInvalidoException as erro:
            messagebox.showerror("Erro", str(erro))
            return

        total = custo_combustivel + custo_distancia
        messagebox.showinfo(
            "Custo da Viagem",
            f"Combustível: R$ {custo_combustivel:.2f}\n"
            f"Custo por distância: R$ {custo_distancia:.2f}\n"
            f"Total: R$ {total:.2f}"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
