import json
import math
import urllib.request

import customtkinter as ctk
import tkintermapview
from tkinter import messagebox

from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.servicos.calculador_custo import CalculadorCusto
from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel
from gestao_frotas.excecoes import DadoInvalidoException

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# valores padrao usados na tela de custo (nao afetam o calculo do custo em si)
TEMPO_ROTA_PADRAO_HORAS = 1.0
CAPACIDADE_PADRAO_KG = 9999
UF_PADRAO = "MG"


class ProvedorPrecoFixo(ProvedorCombustivel):
    def __init__(self, preco):
        self.preco = preco

    def preco_por_litro(self, uf):
        return self.preco


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Entregas")
        self.geometry("600x550")
        self.resizable(True, True)

        self.historico_entregas = []
        self.motoristas: list[Motorista] = []
        self.mostrar_tela_login()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self, text="Login", font=("Arial", 20, "bold"))
        titulo.pack(pady=30)

        self.input_user = ctk.CTkEntry(self, placeholder_text="User", width=280, height=35)
        self.input_user.pack(pady=8)

        self.input_senha = ctk.CTkEntry(self, placeholder_text="Senha", width=280, height=35)
        self.input_senha.pack(pady=8)

        btn_confirmar = ctk.CTkButton (
            self,
            text="Confirmar",
            command=self.confirmar_login,
            font=("Arial", 14),
        )
        btn_confirmar.pack(pady=10)

    def confirmar_login(self):
        if not self.input_user.get() or not self.input_senha.get():
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

        if self.input_user.get().strip() == "admin" and self.input_senha.get().strip() == "admin":
            self.mostrar_tela_inicial()

        motorista = Motorista(1, "abc", "x", "1234")
        self.motoristas.append(motorista)

        for mot in self.motoristas:
            if mot.nome == self.input_user.get() and mot.senha == self.input_senha.get():
                self.mostrar_tela_entregas()

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

        btn_mapa = ctk.CTkButton(
            self,
            text="Ver Mapa da Rota",
            command=self.mostrar_tela_mapa,
            font=("Arial", 14),
            height=40
        )
        btn_mapa.pack(pady=10)

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

        rota = Rota("Origem", "Destino", distancia, TEMPO_ROTA_PADRAO_HORAS)
        veiculo = Veiculo(1, "", "", CAPACIDADE_PADRAO_KG, consumo, custo_km, "")
        calculador = CalculadorCusto(ProvedorPrecoFixo(preco_litro))

        try:
            custo_combustivel = calculador.calcular_custo_combustivel(rota, veiculo, UF_PADRAO)
            custo_distancia = calculador.custo_por_distancia(rota, veiculo)
        except DadoInvalidoException as erro:
            messagebox.showerror("Erro", str(erro))
            return

        total = calculador.calcular_custo_total(rota, veiculo, UF_PADRAO)
        messagebox.showinfo(
            "Custo da Viagem",
            f"Combustível: R$ {custo_combustivel:.2f}\n"
            f"Custo por distância: R$ {custo_distancia:.2f}\n"
            f"Total: R$ {total:.2f}"
        )

    def mostrar_tela_mapa(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self, text="Mapa da Rota", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        self.input_mapa_origem = ctk.CTkEntry(
            self, placeholder_text="Endereço de origem", width=300, height=35
        )
        self.input_mapa_origem.pack(pady=5)

        self.input_mapa_destino = ctk.CTkEntry(
            self, placeholder_text="Endereço de destino", width=300, height=35
        )
        self.input_mapa_destino.pack(pady=5)

        btn_rota = ctk.CTkButton(
            self,
            text="Ver Rota",
            command=self.ver_rota_no_mapa,
            fg_color="green",
            hover_color="darkgreen",
            height=35
        )
        btn_rota.pack(pady=8)

        self.mapa = tkintermapview.TkinterMapView(self, width=540, height=320, corner_radius=8)
        self.mapa.set_position(-22.25, -45.70)
        self.mapa.set_zoom(6)
        self.mapa.pack(pady=10)

        btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="gray",
            hover_color="darkgray",
            height=30
        )
        btn_voltar.pack(pady=5)

    def ver_rota_no_mapa(self):
        origem = self.input_mapa_origem.get().strip()
        destino = self.input_mapa_destino.get().strip()

        if not origem or not destino:
            messagebox.showerror("Erro", "Preencha a origem e o destino.")
            return

        self.mapa.delete_all_marker()
        self.mapa.delete_all_path()

        marcador_origem = self.mapa.set_address(origem, marker=True, text=origem)
        marcador_destino = self.mapa.set_address(destino, marker=True, text=destino)

        if not marcador_origem or not marcador_destino:
            messagebox.showerror("Erro", "Não consegui localizar um dos endereços.")
            return

        coord_origem = marcador_origem.position
        coord_destino = marcador_destino.position

        trajeto = self.buscar_trajeto(coord_origem, coord_destino)

        if trajeto is not None:
            pontos, distancia = trajeto
            self.mapa.set_path(pontos)
            self.mapa.set_position(coord_origem[0], coord_origem[1])
            self.mapa.set_zoom(9)
            messagebox.showinfo("Rota", f"Distância pela estrada: {distancia:.1f} km")
        else:
            self.mapa.set_path([coord_origem, coord_destino])
            self.mapa.set_position(coord_origem[0], coord_origem[1])
            self.mapa.set_zoom(9)
            distancia = self.distancia_em_linha_reta(coord_origem, coord_destino)
            messagebox.showinfo(
                "Rota",
                f"Não achei o trajeto pela estrada, mostrando linha reta: {distancia:.1f} km"
            )

    def buscar_trajeto(self, coord_origem, coord_destino):
        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            f"{coord_origem[1]},{coord_origem[0]};"
            f"{coord_destino[1]},{coord_destino[0]}"
            "?overview=full&geometries=geojson"
        )

        try:
            with urllib.request.urlopen(url, timeout=15) as resposta:
                dados = json.loads(resposta.read().decode())
        except Exception:
            return None

        if dados.get("code") != "Ok" or not dados.get("routes"):
            return None

        rota = dados["routes"][0]
        pontos = [(lat, lon) for lon, lat in rota["geometry"]["coordinates"]]
        distancia_km = rota["distance"] / 1000
        return pontos, distancia_km

    def distancia_em_linha_reta(self, coord1, coord2):
        raio_terra_km = 6371
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 2 * raio_terra_km * math.asin(math.sqrt(a))

    def mostrar_tela_entregas(self):
        self.limpar_janela()
        return


if __name__ == "__main__":
    app = App()
    app.mainloop()
