import json
import math
import urllib.request

import customtkinter as ctk
import tkintermapview
from tkinter import messagebox

from gestao_frotas.modelos import motorista
from gestao_frotas.modelos.entrega import Prioridade, Entrega
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
        self.resizable(False, False)
        self.configure(fg_color="#030A21")

        self.historico_entregas = []
        self.motoristas: list[Motorista] = []
        self.mostrar_tela_inicial()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        self.limpar_janela()

        frame_central = ctk.CTkFrame(self, fg_color="#051121", border_width=1,
                                     border_color="gray", corner_radius=16)
        frame_central.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.45, anchor="center")

        titulo = ctk.CTkLabel(
            frame_central,
            text="Login",
            font=("Helvetica", 24, "bold")
        )
        titulo.pack(pady=(20))

        self.input_user = ctk.CTkEntry(frame_central, placeholder_text="User", width=280, height=35)
        self.input_user.pack(pady=8)

        self.input_senha = ctk.CTkEntry(frame_central, placeholder_text="Senha", width=280, height=35, show="*")
        self.input_senha.pack(pady=8)

        self.label_erro = ctk.CTkLabel(
            frame_central,
            text="",
            text_color="#ff4d4d",  # Vermelho elegante para alertas
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_erro.pack(pady=(0, 3))

        btn_confirmar = ctk.CTkButton (
            frame_central,
            text="Confirmar",
            command=self.confirmar_login,
            font=("Arial", 14)
        )
        btn_confirmar.pack(pady=10)

    def confirmar_login(self):
        if not self.input_user.get() or not self.input_senha.get():
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

        motorista = Motorista(1, "abc", "1234")
        self.motoristas.append(motorista)

        if self.input_user.get().strip() == "admin" and self.input_senha.get().strip() == "admin":
            self.mostrar_tela_inicial()
            return

        login_sucesso = False
        for mot in self.motoristas:
            if mot.nome == self.input_user.get() and mot.cnh == self.input_senha.get():
                login_sucesso = True
        if login_sucesso:
            self.label_erro.configure(text="")
            self.mostrar_tela_entregas()
        else:
            self.label_erro.configure(text="Usuário ou senha incorretos. Tente novamente.")

    def mostrar_tela_inicial(self):
        self.limpar_janela()

        title = ctk.CTkFrame(self, fg_color="#030A21")
        title.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor="center")

        topo_title = ctk.CTkFrame(title, fg_color="transparent")
        topo_title.pack(fill="x", padx=20, pady=(15, 5))

        titulo = ctk.CTkLabel(
            topo_title,
            text="Gerenciador de Entregas 📦",
            font=("Arial", 30, "bold"),
            anchor="w", justify="left"
        )
        titulo.pack(side="left")

        btn_logout = ctk.CTkButton(
            topo_title,
            text="Sair ⏻",
            command=self.mostrar_tela_login,
            fg_color="darkgray",
            font=("Arial", 10, "bold"),
            text_color="black",
            width=40,
            height=10
        )
        btn_logout.pack(side="right")

        linha_divisoria = ctk.CTkFrame(
            title,
            height=5,
            fg_color=("gray50", "gray90")
        )
        linha_divisoria.pack(fill="x", pady=(5,5))

        frame = ctk.CTkFrame(self, fg_color="#051121")
        frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.75, anchor="center")

        titulo = ctk.CTkLabel(
            frame,
            text="Cadastros",
            font=("Arial", 24, "bold"),
            anchor="w", justify="left"
        )
        titulo.pack(fill="x", padx=20, pady=(20, 10))

        btn_cadastrar_entrega = ctk.CTkButton(
            frame,
            text="+ Cadastrar Entrega",
            command=self.mostrar_tela_cadastro,
            font=("Arial", 14),
            height=40,
            width=200
        )
        btn_cadastrar_entrega.pack(anchor="w", padx=20, pady=8)

        ctk.CTkButton(
            frame,
            text="+ Cadastrar Motorista",
            command=self.mostrar_tela_cadastro_motorista,
            font=("Arial", 14),
            height=40,
            width=200).pack(anchor="w", padx=20, pady=8)

        linha_cadastro = ctk.CTkFrame(frame, height=3, fg_color="gray")
        linha_cadastro.pack(fill="x", pady=5)

        titulo = ctk.CTkLabel(
            frame,
            text="Serviços",
            font=("Arial", 24, "bold"),
            anchor="w", justify="left"
        )
        titulo.pack(fill="x", padx=20, pady=(20, 10))

        topo_servicos = ctk.CTkFrame(frame, fg_color="transparent")
        topo_servicos.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkButton(
            topo_servicos,
            text="Listar Motoristas",
            command=self.mostrar_tela_motoristas,
            font=("Arial", 14),
            height=40,
            width=200
        ).pack(side="left")

        btn_calcular_custo = ctk.CTkButton(
            topo_servicos,
            text="Calcular Custo da Viagem",
            command=self.mostrar_tela_custo,
            font=("Arial", 14),
            height=40,
            width = 200
        )
        btn_calcular_custo.pack(side="right", padx=90)

        bottom_servicos = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_servicos.pack(fill="x", padx=20, pady=(15, 5))

        btn_mapa = ctk.CTkButton(
            bottom_servicos,
            text="Ver Mapa da Rota",
            command=self.mostrar_tela_mapa,
            font=("Arial", 14),
            height=40,
            width = 200
        )
        btn_mapa.pack(side="left")

        btn_mapa = ctk.CTkButton(
            bottom_servicos,
            text="Iniciar Entrega",
            command=self.mostrar_tela_viagens,
            font=("Arial", 14),
            height=40,
            width=200
        )
        btn_mapa.pack(side="right", padx=90)

        footer_frame = ctk.CTkFrame(
            self,
            fg_color="#030A21",
            height=40,
            corner_radius=0
        )
        footer_frame.place(relx=0.5, rely=1.0, relwidth=1.0, anchor="s")

        lbl_footer = ctk.CTkLabel(
            footer_frame,
            text="© 2026 Gerenciador de Entregas - Todos os direitos reservados",
            font=("Arial", 11),
            text_color=("gray60", "gray50")
        )
        lbl_footer.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_tela_cadastro(self):
        self.limpar_janela()

        frame = ctk.CTkFrame(self, corner_radius=16, fg_color=("black", "#051121"), border_color="grey", border_width=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        titulo = ctk.CTkLabel(frame, text="Informações da Entrega 📦", font=ctk.CTkFont(size=25, weight="bold"))
        titulo.pack(pady=25)

        self.input_codigo = ctk.CTkEntry(
            frame, placeholder_text="Código da Entrega",
            width=320, height=40, corner_radius=8)
        self.input_codigo.pack(pady=10)

        self.input_origem = ctk.CTkEntry(
            frame, placeholder_text="Endereço de Origem",
            width=320, height=40, corner_radius=8)
        self.input_origem.pack(pady=10)

        self.input_destino = ctk.CTkEntry(
            frame, placeholder_text="Endereço de Destino",
            width=320, height=40, corner_radius=8)
        self.input_destino.pack(pady=10)

        frame_2 = ctk.CTkFrame(frame, fg_color="transparent")
        frame_2.pack(pady=(20, 0))

        self.input_prioridade = ctk.CTkOptionMenu(
            frame_2,
            values = ["Baixa", "Normal", "Alta"],
            width=20, height=40, corner_radius=8,
        )

        self.input_prioridade.pack(side="left", padx=10)

        self.input_peso = ctk.CTkEntry(
            frame_2, placeholder_text="Peso da Entrega (Kg)",
            width=135, height=40)
        self.input_peso.pack(side="right", padx=10)

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(pady=(35, 0))

        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar e Cadastrar",
            command=self.salvar_dados,
            fg_color="green", hover_color="darkgreen",
            font=ctk.CTkFont(weight="bold"),
            height=40, corner_radius=8, width=150
        )
        btn_salvar.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            height=40, width=100, corner_radius=8,
        )
        btn_voltar.pack(side="right", padx=10)

    def salvar_dados(self):
        destino = self.input_destino.get().strip()
        origem = self.input_origem.get().strip()
        id = self.input_codigo.get().strip()
        peso = self.input_peso.get().strip()
        if self.input_prioridade.get().strip() == "Normal":
            prioridade = Prioridade.NORMAL
        elif self.input_prioridade.get().strip() == "Alta":
            prioridade = Prioridade.ALTA
        elif self.input_prioridade.get().strip() == "Baixa":
            prioridade = Prioridade.BAIXA

        if not destino or not origem or not id or not peso or not prioridade:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return

        nova_entrega = Entrega(int(id), origem, destino, int(peso), prioridade)
        self.historico_entregas.append(nova_entrega)

        messagebox.showinfo("Sucesso", "Entrega Cadastrada com sucesso!")
        print(nova_entrega)
        self.mostrar_tela_inicial()

    def mostrar_tela_cadastro_motorista(self):
        self.limpar_janela()

        frame = ctk.CTkFrame(self, corner_radius=16, fg_color=("black", "#051121"), border_color="grey", border_width=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.65)

        ctk.CTkLabel(frame, text="Cadastrar Motorista",font=ctk.CTkFont(size=25, weight="bold")).pack(pady=25)

        self.input_nome = ctk.CTkEntry(frame, placeholder_text="Nome", width=320, height=40, corner_radius=8)
        self.input_nome.pack(pady=10)
        self.input_cnh = ctk.CTkEntry(frame, placeholder_text="CNH", width=320, height=40, corner_radius=8)
        self.input_cnh.pack(pady=10)

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(pady=(35, 0))

        ctk.CTkButton(
            frame_botoes,
            text="Salvar",
          command=self.salvar_motorista,
          fg_color="green", hover_color="darkgreen",
          font=ctk.CTkFont(weight="bold"),
          height=40, corner_radius=8, width=100
          ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color = "transparent",
            border_width = 1,
            text_color = ("gray10", "gray90"),
            height = 40, width = 100, corner_radius = 8
        ).pack(side="right", padx=10)

    def salvar_motorista(self):
        nome = self.input_nome.get().strip()
        cnh = self.input_cnh.get().strip()
        if not nome or not cnh:
            messagebox.showerror("Erro", "Preencha nome e CNH.")
            return
        motorista = Motorista(len(self.motoristas) + 1, nome, cnh)
        self.motoristas.append(motorista)
        messagebox.showinfo("Sucesso", "Motorista cadastrado!")
        self.mostrar_tela_inicial()

    def mostrar_tela_motoristas(self):
        self.limpar_janela()

        frame = ctk.CTkFrame(self, fg_color="#030A21")
        frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")

        ctk.CTkLabel(
            frame,
            text="Motoristas Cadastrados 📋",
            font=("Arial", 26, "bold"),
            text_color="white"
        ).pack(pady=(25, 10))

        scroll_frame = ctk.CTkScrollableFrame(
            frame,
            width=400,
            height=300,
            fg_color="#0b132b",
            corner_radius=10
        )
        scroll_frame.pack(pady=10, fill="both", expand=True, padx=40)

        if not self.motoristas:
            ctk.CTkLabel(
                scroll_frame,
                text="Nenhum motorista cadastrado.",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
        else:
            for motorista in self.motoristas:
                item_card = ctk.CTkFrame(scroll_frame, fg_color="#1c2541", height=50, corner_radius=8)
                item_card.pack(fill="x", pady=6, padx=10)
                lbl_nome = ctk.CTkLabel(
                    item_card,
                    text=f"👤 {motorista.nome}",
                    font=("Arial", 14, "bold"),
                    text_color="white"
                )
                lbl_nome.pack(side="left", padx=15, pady=10)

                lbl_status = ctk.CTkLabel(
                    item_card,
                    text=f"Status: {motorista.status}",
                    font=("Arial", 12),
                    text_color="#4ade80"
                )
                lbl_status.pack(side="right", padx=15, pady=10)

        btn_voltar = ctk.CTkButton(
            frame,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            font=("Arial", 14),
            height=40,
            width=200
        )
        btn_voltar.pack(pady=(10, 25))

    def mostrar_tela_custo(self):
        self.limpar_janela()

        frame = ctk.CTkFrame(self, corner_radius=16, fg_color=("black", "#051121"), border_color="grey", border_width=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        titulo = ctk.CTkLabel(frame, text="Calcular Custo da Viagem", font=("Arial", 25, "bold"))
        titulo.pack(pady=25)

        self.input_distancia = ctk.CTkEntry(frame, placeholder_text="Distância (km)",
                                            corner_radius=8, width=320, height=40)
        self.input_distancia.pack(pady=10)

        self.input_consumo = ctk.CTkEntry(frame, placeholder_text="Consumo do veículo (km/l)",
                                            corner_radius=8, width=320, height=40)
        self.input_consumo.pack(pady=10)

        self.input_custo_km = ctk.CTkEntry(frame, placeholder_text="Custo por km (R$)",
                                           corner_radius=8, width=320, height=40)
        self.input_custo_km.pack(pady=10)

        self.input_preco_litro = ctk.CTkEntry(frame, placeholder_text="Preço do litro (R$)",
                                              corner_radius=8, width=320, height=40)
        self.input_preco_litro.pack(pady=10)

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(pady=(35, 0))

        btn_calcular = ctk.CTkButton(
            frame_botoes,
            text="Calcular Custo",
            command=self.calcular_custo,
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(weight="bold"),
            height=35,
            corner_radius=8,
            width=150
        )
        btn_calcular.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="transparent",
            height=30,
            border_width=1,
            text_color=("gray10", "gray90"),
            corner_radius=8,
            width=100
        )
        btn_voltar.pack(side="right", padx=10)

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

        titulo = ctk.CTkLabel(self, text="Mapa da Rota", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        linha_divisoria = ctk.CTkFrame(
            self,
            height=3,
            fg_color=("gray50", "gray90")
        )
        linha_divisoria.pack(fill="x", pady=(5, 5))

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
            height=35,
            width=60,
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
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            height=40, width=60, corner_radius=8
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

    def mostrar_tela_viagens(self):
        self.limpar_janela()

        frame = ctk.CTkScrollableFrame(self, corner_radius=16, fg_color=("black", "#051121"), border_color="grey", border_width=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ctk.CTkLabel(frame, text="Iniciar Entregas", font=ctk.CTkFont(size=25, weight="bold")).pack(pady=25)

        titulo = ctk.CTkLabel(frame, text="Motorista", font=ctk.CTkFont(size=14, weight="bold"))
        titulo.pack(pady=8)
        nomes_motoristas = [motorista.nome for motorista in self.motoristas]
        if not nomes_motoristas:
            nomes_motoristas = ["Nenhum motorista cadastrado"]
        self.input_motorista = ctk.CTkOptionMenu(
            frame,
            values=nomes_motoristas,
            width=320,
            height=40,
            corner_radius=8
            )
        self.input_motorista.pack(pady=10)

        if self.motoristas:
            self.input_motorista.set("Selecione o motorista")
        else:
            self.input_motorista.set("Nenhum motorista cadastrado")


        titulo = ctk.CTkLabel(frame, text="Entregas", font=ctk.CTkFont(size=14, weight="bold"))
        titulo.pack(pady=8)
        nomes_entregas = [(str(entrega.id) + ": " + str(entrega.destino)) for entrega in self.historico_entregas]
        if not nomes_entregas:
            nomes_entregas = ["Nenhuma entrega cadastrada"]

        for _ in range(5):
            self.input_entrega = ctk.CTkOptionMenu(
                frame,
                values=nomes_entregas,
                width=320,
                height=40,
                corner_radius=8
            )
            self.input_entrega.pack(pady=10)

            if self.historico_entregas:
                self.input_entrega.set("Selecione a entrega")
            else:
                self.input_entrega.set("Nenhuma entrega cadastrada")

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(pady=(35, 0))

        ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self.salvar_motorista,
            fg_color="green", hover_color="darkgreen",
            font=ctk.CTkFont(weight="bold"),
            height=40, corner_radius=8, width=100
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self.mostrar_tela_inicial,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            height=40, width=100, corner_radius=8
        ).pack(side="right", padx=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
