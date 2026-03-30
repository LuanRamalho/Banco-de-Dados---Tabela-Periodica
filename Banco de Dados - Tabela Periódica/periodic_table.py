import tkinter as tk
import json

class TabelaPeriodica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tabela Periódica Interativa")
        self.geometry("1100x700")
        self.configure(bg="#100f0f") 

        # Permite que o container principal expanda com a janela
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Frame da Tabela (Grade)
        self.grid_frame = tk.Frame(self, bg="#fffcfc")
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
        def on_enter(e): celula.config(bg="#0E0086")
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
        # Criação da janela popup (Toplevel)
        popup = tk.Toplevel(self)
        popup.title(f"Detalhes: {el['Nome']}")
        popup.geometry("350x300")
        popup.configure(bg="#2d2d30") # Fundo grafite escuro
        popup.resizable(False, False)
        
        # Faz a janela ser modal (focar nela até fechar)
        popup.transient(self)
        popup.grab_set()

        # --- Cabeçalho Colorido ---
        header = tk.Frame(popup, bg=el["CorHex"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Símbolo em destaque no cabeçalho
        tk.Label(header, text=el["Simbolo"], font=("Segoe UI", 32, "bold"), 
                 bg=el["CorHex"], fg="black").pack(side="left", padx=20)
        
        # Nome do elemento ao lado do símbolo
        tk.Label(header, text=el["Nome"].upper(), font=("Segoe UI", 14, "bold"), 
                 bg=el["CorHex"], fg="black").pack(side="left", pady=20)

        # --- Corpo com Informações Técnicas ---
        info_container = tk.Frame(popup, bg="#2d2d30")
        info_container.pack(fill="both", expand=True, padx=25, pady=20)

        # Lista de dados conforme solicitado
        dados = [
            ("Número Atômico", el["NumeroAtomico"]),
            ("Símbolo Atômico", el["Simbolo"]),
            ("Nome Completo", el["Nome"]),
            ("Peso Atômico", f"{el['PesoAtomico']} u")
        ]

        for label, valor in dados:
            row = tk.Frame(info_container, bg="#2d2d30")
            row.pack(fill="x", pady=6)
            
            # Rótulo (ex: "Peso Atômico")
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 10, "bold"), 
                     bg="#2d2d30", fg="#888888").pack(side="left")
            
            # Valor (ex: "1.008 u")
            tk.Label(row, text=str(valor), font=("Segoe UI", 11), 
                     bg="#2d2d30", fg="white").pack(side="right")

        # Botão para fechar
        btn_fechar = tk.Button(popup, text="FECHAR", command=popup.destroy, 
                               bg="#444444", fg="white", font=("Segoe UI", 9, "bold"),
                               relief="flat", cursor="hand2", activebackground="#666666")
        btn_fechar.pack(side="bottom", fill="x", padx=25, pady=15)

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
