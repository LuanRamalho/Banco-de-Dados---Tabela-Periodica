import tkinter as tk
import json

class TabelaPeriodica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tabela Periódica Interativa")
        self.geometry("1100x700")
        self.configure(bg="#1e1e1e") # Fundo escuro para visual moderno

        # Permite que o container principal expanda com a janela
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Frame da Tabela (Grade)
        self.grid_frame = tk.Frame(self, bg="#1e1e1e")
        self.grid_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Frame da Legenda (Rodapé)
        self.legenda_frame = tk.Frame(self, bg="#1e1e1e")
        self.legenda_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # Configura as 10 linhas e 18 colunas para redimensionamento perfeito
        for i in range(10):
            self.grid_frame.rowconfigure(i, weight=1)
        for i in range(18):
            self.grid_frame.columnconfigure(i, weight=1)

        self.carregar_dados()
        self.criar_legenda()

    def carregar_dados(self):
        try:
            with open('elementos.json', 'r', encoding='utf-8') as f:
                elementos = json.load(f)
            
            for el in elementos:
                self.criar_celula(el)
        except FileNotFoundError:
            print("Erro: O arquivo 'elementos.json' não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: Falha ao ler o formato do arquivo JSON.")

    def criar_celula(self, el):
        # O JSON usa índices baseados em 1, ajustamos para base 0 no grid do Tkinter
        linha = el["Linha"] - 1
        coluna = el["Coluna"] - 1
        cor_base = el["CorHex"]

        # Criando um frame em vez de um botão padrão para um controle visual mais limpo
        celula = tk.Frame(self.grid_frame, bg=cor_base, relief="flat", bd=0)
        celula.grid(row=linha, column=coluna, sticky="nsew", padx=2, pady=2)

        # Efeitos de Hover
        def on_enter(e): celula.config(bg="#FFFFFF")
        def on_leave(e): celula.config(bg=cor_base)

        # Textos do elemento
        lbl_num = tk.Label(celula, text=str(el["NumeroAtomico"]), font=("Segoe UI", 8, "bold"), bg=cor_base, fg="#333333")
        lbl_num.pack(anchor="nw", padx=3)

        lbl_simb = tk.Label(celula, text=el["Simbolo"], font=("Segoe UI", 14, "bold"), bg=cor_base, fg="black")
        lbl_simb.pack(expand=True)

        lbl_nome = tk.Label(celula, text=el["Nome"], font=("Segoe UI", 7), bg=cor_base, fg="#333333")
        lbl_nome.pack(side="bottom", fill="x", pady=2)

        # Vincula os eventos de clique e hover a todos os componentes da célula
        for widget in (celula, lbl_num, lbl_simb, lbl_nome):
            widget.bind("<Button-1>", lambda e, elemento=el: self.mostrar_detalhes(elemento))
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def mostrar_detalhes(self, el):
        # Janela Popup
        popup = tk.Toplevel(self)
        popup.title(f"Detalhes - {el['Nome']}")
        popup.geometry("300x250")
        popup.configure(bg="#2d2d30")
        popup.resizable(False, False)
        
        # Centraliza o popup em relação à tela principal
        popup.transient(self)
        popup.grab_set()

        # Cabeçalho do popup
        header = tk.Frame(popup, bg=el["CorHex"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=el["Simbolo"], font=("Segoe UI", 24, "bold"), bg=el["CorHex"], fg="black").pack(side="left", padx=15)
        tk.Label(header, text=el["Nome"], font=("Segoe UI", 14), bg=el["CorHex"], fg="black").pack(side="left", fill="y", pady=15)

        # Informações detalhadas
        info_frame = tk.Frame(popup, bg="#2d2d30")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        infos = [
            ("Número Atômico:", el["NumeroAtomico"]),
            ("Peso Atômico:", el["PesoAtomico"]),
            ("Coluna (Grupo):", el["Coluna"]),
            ("Linha (Período):", el["Linha"])
        ]

        for desc, valor in infos:
            row_frame = tk.Frame(info_frame, bg="#2d2d30")
            row_frame.pack(fill="x", pady=5)
            tk.Label(row_frame, text=desc, font=("Segoe UI", 10, "bold"), bg="#2d2d30", fg="#aaaaaa").pack(side="left")
            tk.Label(row_frame, text=str(valor), font=("Segoe UI", 10), bg="#2d2d30", fg="white").pack(side="right")

    def criar_legenda(self):
        # Mapeamento inferido pelas cores fornecidas no seu JSON
        categorias = [
            ("#C1FFC1", "Metais Alcalinos / Alcalinoterrosos"),
            ("#FFFF96", "Não-Metais e Semimetais"),
            ("#FFC080", "Metais de Transição"),
            ("#F5DEB3", "Gases Nobres"),
            ("#ADD8E6", "Lantanídeos e Actinídeos")
        ]

        # Centralizando a legenda
        container_legenda = tk.Frame(self.legenda_frame, bg="#1e1e1e")
        container_legenda.pack(anchor="center")

        for cor, texto in categorias:
            item_frame = tk.Frame(container_legenda, bg="#1e1e1e")
            item_frame.pack(side="left", padx=15)
            
            # Quadrado de cor
            cor_box = tk.Frame(item_frame, bg=cor, width=15, height=15, relief="flat")
            cor_box.pack(side="left", padx=5)
            cor_box.pack_propagate(False)
            
            # Texto da legenda
            tk.Label(item_frame, text=texto, font=("Segoe UI", 9), bg="#1e1e1e", fg="white").pack(side="left")

if __name__ == "__main__":
    app = TabelaPeriodica()
    app.mainloop()