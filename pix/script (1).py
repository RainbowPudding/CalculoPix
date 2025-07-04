import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
from datetime import datetime
import json
import os

servicos = {
    "Autenticação": 5.02,
    "Firma com valor": 13.24,
    "Firma sem valor": 8.66,
    "Firma Autêntica": 22.17
}

arquivoDados = "dados.json"
lista = []

def salvar_automático():
    try:
        with open(arquivoDados, "w", encoding="utf-8") as f:
            json.dump(lista, f)
    except Exception as e:
        print("Erro ao salvar automaticamente:", e)

def carregar_lista():
    if os.path.exists(arquivoDados):
        try:
            with open(arquivoDados, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for item in dados:
                    lista.append(tuple(item))
        except Exception as e:
            print("Erro ao carregar dados:", e)

def addServicos(servico):
    try:
        qtd = simpledialog.askinteger("PIX", f"Quantidade feita de {servico}:")
        if qtd and qtd > 0:
            preco = servicos[servico]
            total = qtd * preco
            hora = datetime.now().strftime("%H:%M")
            lista.append((servico, qtd, preco, total, hora))
            atualizaLista()
        else:
            messagebox.showerror("Erro!", "Insira uma quantidade válida.")
    except Exception as e:
        messagebox.showerror("Erro!", str(e))

def atualizaLista():
    saida.config(state="normal")
    saida.delete(1.0, "end")
    final = 0
    for i in lista:
        saida.insert("end", f" {i[4]} \n {i[0]} - Quantidade: {i[1]} \n Total: R$ {i[3]:.2f}\n\n")
        final += i[3]
    saida.insert("end", f"\nTOTAL: R$ {final:.2f}")
    saida.config(state="disabled")
    salvar_automático()

def removerServico():
    if not lista:
        messagebox.showinfo("Aviso", "A lista está vazia.")
        return
    nomes = [f"{i[0]} (Qtd: {i[1]}, Total: R$ {i[3]:.2f})" for i in lista]
    escolha = simpledialog.askinteger(
        "Remover Serviço",
        "Escolha o número do serviço para remover:\n\n" +
        "\n".join([f"{idx + 1}. {nome}" for idx, nome in enumerate(nomes)]),
        minvalue=1, maxvalue=len(lista)
    )
    if escolha:
        del lista[escolha - 1]
        atualizaLista()

def limparLista():
    if messagebox.askyesno("Confirmação", "Deseja realmente limpar todos os serviços?"):
        lista.clear()
        atualizaLista()

def salvarLista():
    if not lista:
        messagebox.showinfo("Aviso", "A lista está vazia.")
        return
    try:
        data = datetime.now().strftime("%d-%m-%Y")
        filename = f"servicos_{data}.txt"
        counter = 1
        while os.path.exists(filename):
            filename = f"servicos_{data}_{counter}.txt"
            counter += 1
        with open(filename, "w", encoding="utf-8") as f:
            total_geral = 0
            for i in lista:
                f.write(f"{i[4]} - {i[0]} - Qtd: {i[1]} - Preço: R$ {i[2]:.2f} - Total: R$ {i[3]:.2f}\n")
                total_geral += i[3]
            f.write(f"\nTOTAL GERAL: R$ {total_geral:.2f}\n")
        messagebox.showinfo("Sucesso", f"Lista salva com sucesso em '{filename}'.")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", str(e))

def addValorPersonalizado():
    try:
        valor = simpledialog.askfloat("Adicionar Valor Personalizado", "Digite o valor (R$):")
        if valor is not None and valor > 0:
            hora = datetime.now().strftime("%H:%M")
            lista.append(("Valor Personalizado", 1, valor, valor, hora))
            atualizaLista()
        else:
            messagebox.showerror("Erro!", "Insira um valor válido.")
    except Exception as e:
        messagebox.showerror("Erro!", str(e))

app = ttk.Window(themename="darkly")
app.title("PIX")
app.geometry("800x800")
app.protocol("WM_DELETE_WINDOW", lambda: (salvar_automático(), app.destroy()))

# Custom button styles
style = ttk.Style()
style.configure("autenticacao.TButton", background="#6a994e", foreground="black", font=("Segoe UI", 10, "bold"))
style.configure("semvalor.TButton", background="#87BCDE", foreground="black", font=("Segoe UI", 10, "bold"))
style.configure("comvalor.TButton", background="#d62828", foreground="black", font=("Segoe UI", 10, "bold"))
style.configure("autentica.TButton", background="#c8b6ff", foreground="black", font=("Segoe UI", 10, "bold"))

frame_servicos = ttk.LabelFrame(app, text="Autenticações e Firmas", padding=10)
frame_servicos.pack(padx=10, pady=10, fill="x")

container = ttk.Frame(frame_servicos)
container.pack(pady=5)
container.columnconfigure(0, weight=1)

# Add buttons with custom styles
ttk.Button(container, text="Autenticação", command=lambda: addServicos("Autenticação"),
           style="autenticacao.TButton", width=30).pack(pady=4)
ttk.Button(container, text="Firma com valor", command=lambda: addServicos("Firma com valor"),
           style="comvalor.TButton", width=30).pack(pady=4)
ttk.Button(container, text="Firma sem valor", command=lambda: addServicos("Firma sem valor"),
           style="semvalor.TButton", width=30).pack(pady=4)
ttk.Button(container, text="Firma Autêntica", command=lambda: addServicos("Firma Autêntica"),
           style="autentica.TButton", width=30).pack(pady=4)

ttk.Button(container, text="Adicionar Valor Personalizado", command=addValorPersonalizado,
           bootstyle="info-outline", width=30).pack(pady=8)

frame_saida = ttk.Frame(app)
frame_saida.pack(fill="both", expand=True, padx=10, pady=5)

saida = ttk.Text(frame_saida, height=10, font=("Segoe UI", 10))
saida.pack(side="left", fill="both", expand=True)

scroll = ttk.Scrollbar(frame_saida, command=saida.yview)
scroll.pack(side="right", fill="y")
saida.config(yscrollcommand=scroll.set, state="disabled")

frame_acoes = ttk.Frame(app)
frame_acoes.pack(padx=10, pady=10, fill="x")

for widget, func in [
    ("Remover Serviço", removerServico),
    ("Limpar Lista", limparLista),
    ("Salvar Lista", salvarLista)
]:
    ttk.Button(frame_acoes, text=widget, command=func, bootstyle="info-outline", width=30).pack(side="left", padx=10)

carregar_lista()
atualizaLista()
app.mainloop()
