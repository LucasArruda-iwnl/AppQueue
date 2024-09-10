import sqlite3
import tkinter as tk
from tkinter import messagebox, StringVar

# Conexão com o banco de dados
conn = sqlite3.connect('ping_pong.db')
cursor = conn.cursor()

# Criação da tabela de partidas
cursor.execute('''
CREATE TABLE IF NOT EXISTS partidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vencedor TEXT NOT NULL,
    perdedor TEXT NOT NULL,
    placar_vencedor INTEGER,
    placar_perdedor INTEGER,
    data_partida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

fila_jogadores = []
vencedor_atual = None

def adicionar_jogador(nome):
    if nome:
        fila_jogadores.append(nome)
        atualizar_fila()
        entry_jogador.delete(0, tk.END)

def proximo_jogo():
    global vencedor_atual
    if len(fila_jogadores) < 1:
        messagebox.showinfo("Info", "Não há jogadores suficientes para iniciar um jogo.")
        return

    if vencedor_atual is None:  
        jogador1 = fila_jogadores.pop(0)
        jogador2 = fila_jogadores.pop(0)
    else: 
        jogador1 = vencedor_atual
        jogador2 = fila_jogadores.pop(0)

    lbl_jogo_atual.config(text=f"{jogador1} vs {jogador2}")

    vencedor_var.set('')
    perdedor_var.set('')
    menu_vencedor['menu'].delete(0, 'end')
    menu_perdedor['menu'].delete(0, 'end')

    menu_vencedor['menu'].add_command(label=jogador1, command=tk._setit(vencedor_var, jogador1))
    menu_vencedor['menu'].add_command(label=jogador2, command=tk._setit(vencedor_var, jogador2))

    menu_perdedor['menu'].add_command(label=jogador1, command=tk._setit(perdedor_var, jogador1))
    menu_perdedor['menu'].add_command(label=jogador2, command=tk._setit(perdedor_var, jogador2))

    return jogador1, jogador2

def registrar_partida():
    global vencedor_atual
    vencedor = vencedor_var.get()
    perdedor = perdedor_var.get()
    placar_vencedor = entry_placar_vencedor.get()
    placar_perdedor = entry_placar_perdedor.get()

    if not all([vencedor, perdedor, placar_vencedor, placar_perdedor]):
        messagebox.showwarning("Aviso", "Preencha todos os campos para registrar a partida.")
        return

    if vencedor == perdedor:
        messagebox.showwarning("Aviso", "O vencedor e o perdedor não podem ser a mesma pessoa.")
        return

    # Inserir partida no banco de dados
    cursor.execute('''
        INSERT INTO partidas (vencedor, perdedor, placar_vencedor, placar_perdedor)
        VALUES (?, ?, ?, ?)
    ''', (vencedor, perdedor, placar_vencedor, placar_perdedor))
    conn.commit()

    fila_jogadores.append(perdedor)

    if vencedor != vencedor_atual:
        vencedor_atual = vencedor

    atualizar_fila()
    limpar_campos()
    proximo_jogo()

def atualizar_fila():
    fila_str = "\n".join(fila_jogadores)
    lbl_fila.config(text=fila_str)

def exibir_historico():
    cursor.execute('SELECT vencedor, perdedor, placar_vencedor, placar_perdedor, data_partida FROM partidas')
    partidas = cursor.fetchall()

    historico_window = tk.Toplevel(window)
    historico_window.title("Histórico de Partidas")

    for partida in partidas:
        vencedor, perdedor, placar_vencedor, placar_perdedor, data_partida = partida
        label = tk.Label(historico_window, text=f"{data_partida}: {vencedor} {placar_vencedor} x {placar_perdedor} {perdedor}")
        label.pack()

def limpar_campos():
    vencedor_var.set('')
    perdedor_var.set('')
    entry_placar_vencedor.delete(0, tk.END)
    entry_placar_perdedor.delete(0, tk.END)

window = tk.Tk()
window.title("Gerenciamento de Fila Ping Pong")

frame_add_jogador = tk.Frame(window)
frame_add_jogador.pack(pady=10)

lbl_add_jogador = tk.Label(frame_add_jogador, text="Adicionar Jogador:")
lbl_add_jogador.pack(side=tk.LEFT)

entry_jogador = tk.Entry(frame_add_jogador)
entry_jogador.pack(side=tk.LEFT)

btn_add_jogador = tk.Button(frame_add_jogador, text="Adicionar", command=lambda: adicionar_jogador(entry_jogador.get()))
btn_add_jogador.pack(side=tk.LEFT)

lbl_fila_titulo = tk.Label(window, text="Fila de Jogadores:")
lbl_fila_titulo.pack()

lbl_fila = tk.Label(window, text="", font=("Arial", 12), justify=tk.LEFT)
lbl_fila.pack(pady=5)

btn_proximo_jogo = tk.Button(window, text="Iniciar Próximo Jogo", command=proximo_jogo)
btn_proximo_jogo.pack(pady=5)

lbl_jogo_atual = tk.Label(window, text="Nenhum jogo em andamento.", font=("Arial", 14))
lbl_jogo_atual.pack(pady=5)

frame_registrar_partida = tk.Frame(window)
frame_registrar_partida.pack(pady=10)

vencedor_var = StringVar()
perdedor_var = StringVar()

lbl_vencedor = tk.Label(frame_registrar_partida, text="Vencedor:")
lbl_vencedor.grid(row=0, column=0)

menu_vencedor = tk.OptionMenu(frame_registrar_partida, vencedor_var, "")
menu_vencedor.grid(row=0, column=1)

lbl_perdedor = tk.Label(frame_registrar_partida, text="Perdedor:")
lbl_perdedor.grid(row=1, column=0)

menu_perdedor = tk.OptionMenu(frame_registrar_partida, perdedor_var, "")
menu_perdedor.grid(row=1, column=1)

lbl_placar_vencedor = tk.Label(frame_registrar_partida, text="Placar Vencedor:")
lbl_placar_vencedor.grid(row=2, column=0)

entry_placar_vencedor = tk.Entry(frame_registrar_partida)
entry_placar_vencedor.grid(row=2, column=1)

lbl_placar_perdedor = tk.Label(frame_registrar_partida, text="Placar Perdedor:")
lbl_placar_perdedor.grid(row=3, column=0)

entry_placar_perdedor = tk.Entry(frame_registrar_partida)
entry_placar_perdedor.grid(row=3, column=1)

btn_registrar = tk.Button(window, text="Registrar Partida", command=registrar_partida)
btn_registrar.pack(pady=10)

btn_historico = tk.Button(window, text="Exibir Histórico", command=exibir_historico)
btn_historico.pack(pady=5)

window.mainloop()

conn.close()
