
#  Testes  

import tkinter as tk
from tkinter import ttk
import threading, time
from puzzle import manhattan, solvable, extract, apply_move, GOAL
from genetico import genetic_algorithm

CORES = {
    1:("#0d2137","#4f9eff"), 2:("#1a0d37","#9b6fff"),
    3:("#370d1a","#ff4f7b"), 4:("#371d0d","#ff8c4f"),
    5:("#0d3718","#4fff82"), 6:("#0d3333","#4fffff"),
    7:("#1a0d37","#bf4fff"), 8:("#373010","#ffe04f"),
}

PRESETS = {
    "Fácil":         ((1,2,3,4,5,6,7,0,8), dict(pop_size=150, seq_len=30,  max_gen=500,  pm=0.05)),
    "Médio":         ((1,2,3,4,0,6,7,5,8), dict(pop_size=200, seq_len=60,  max_gen=800,  pm=0.04)),
    "Difícil":       ((8,1,3,4,0,2,7,6,5), dict(pop_size=400, seq_len=150, max_gen=3000, pm=0.03)),
    "Médio-Difícil": ((2,8,3,1,6,4,7,0,5), dict(pop_size=350, seq_len=120, max_gen=2000, pm=0.03)),
}

class App:
    def __init__(self, root):
        self.root   = root
        self.root.title("8-Puzzle · Algoritmo Genético")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(False, False)
        self.sol    = []
        self.busy   = False
        self._build()
        self.load("Médio")

    def _build(self):
        BG, PAN = "#0a0a0a", "#111111"

        tk.Label(self.root, text="8 - P U Z Z L E",
                 font=("Courier",18,"bold"), bg=BG, fg="#4f9eff").pack(pady=(20,2))
        tk.Label(self.root, text="Algoritmo Genético",
                 font=("Courier",9), bg=BG, fg="#444").pack(pady=(0,16))

        row = tk.Frame(self.root, bg=BG)
        row.pack(padx=28)

        # ── Tabuleiro 
        left = tk.Frame(row, bg=BG)
        left.pack(side=tk.LEFT, padx=(0,20))

        board = tk.Frame(left, bg="#222", padx=3, pady=3)
        board.pack()
        self.tiles = []
        for i in range(3):
            r = []
            for j in range(3):
                c = tk.Frame(board, bg=BG, width=104, height=104)
                c.grid(row=i, column=j, padx=2, pady=2)
                c.grid_propagate(False)
                l = tk.Label(c, text="", font=("Courier",28,"bold"), bg=BG, fg="#fff")
                l.place(relx=.5, rely=.5, anchor="center")
                r.append((c, l))
            self.tiles.append(r)

        # Seletor
        sel = tk.Frame(left, bg=BG)
        sel.pack(pady=(12,0))
        tk.Label(sel, text="Config:", font=("Courier",9), bg=BG, fg="#444").pack(side=tk.LEFT, padx=(0,6))
        self.pvar = tk.StringVar(value="Médio")
        for name in PRESETS:
            tk.Radiobutton(sel, text=name, variable=self.pvar, value=name,
                           font=("Courier",9), bg=BG, fg="#ccc",
                           selectcolor=BG, activebackground=BG,
                           command=lambda n=name: self.load(n)).pack(side=tk.LEFT, padx=3)

        # ── Painel 
        pan = tk.Frame(row, bg=PAN, padx=20, pady=18)
        pan.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(pan, text="ESTATÍSTICAS", font=("Courier",9,"bold"),
                 bg=PAN, fg="#4f9eff").pack(anchor="w", pady=(0,10))

        self.sv = {}
        for label, key in [("Dist. Manhattan","dist"), ("Peças fora","pecas"),
                            ("Solúvel","soluvel"), ("Status","status"),
                            ("Gerações","geracoes"), ("Movimentos","movimentos"),
                            ("Tempo","tempo")]:
            f = tk.Frame(pan, bg=PAN); f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=f"{label}:", font=("Courier",10), bg=PAN,
                     fg="#444", width=15, anchor="w").pack(side=tk.LEFT)
            v = tk.StringVar(value="—")
            tk.Label(f, textvariable=v, font=("Courier",10,"bold"),
                     bg=PAN, fg="#ccc", anchor="w").pack(side=tk.LEFT)
            self.sv[key] = v

        self.pb   = ttk.Progressbar(pan, length=210, mode="indeterminate")
        self.pb.pack(fill=tk.X, pady=(14,2))
        self.slbl = tk.Label(pan, text="", font=("Courier",8), bg=PAN, fg="#444")
        self.slbl.pack(anchor="w")

        def btn(txt, bg, fg, cmd, **kw):
            return tk.Button(pan, text=txt, font=("Courier",10,"bold"),
                             bg=bg, fg=fg, activebackground="#222",
                             activeforeground=fg, relief="flat",
                             padx=14, pady=8, cursor="hand2",
                             command=cmd, **kw)

        tk.Label(pan, text="", bg=PAN).pack(pady=6)
        self.bsolve = btn("▶  RESOLVER",       "#4f9eff","#0a0a0a", self.solve)
        self.bsolve.pack(fill=tk.X, pady=(0,6))
        self.banim  = btn("⏵  ANIMAR SOLUÇÃO", "#1a1a1a","#ccc",    self.animate, state="disabled")
        self.banim.pack(fill=tk.X, pady=(0,6))
        self.breset = btn("↺  REINICIAR",      "#1a1a1a","#ccc",    self.reset)
        self.breset.pack(fill=tk.X)

        tk.Label(pan, text="Velocidade:", font=("Courier",8),
                 bg=PAN, fg="#444").pack(anchor="w", pady=(16,2))
        self.spd = tk.IntVar(value=5)
        tk.Scale(pan, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.spd,
                 bg=PAN, fg="#ccc", highlightthickness=0,
                 troughcolor="#1a1a1a", activebackground="#4f9eff",
                 length=210).pack(fill=tk.X)

    # ── Helpers 
    def load(self, name):
        self.pvar.set(name)
        self.state, self.params = PRESETS[name]
        self.sol = []
        self.slbl.config(text="")
        self.banim.config(state="disabled")
        for k in ("status","geracoes","movimentos","tempo"):
            self.sv[k].set("—")
        self.draw(self.state)
        self.sv["dist"].set(str(manhattan(self.state)))
        self.sv["pecas"].set(str(sum(v != GOAL[i] and v for i,v in enumerate(self.state))))
        self.sv["soluvel"].set("Sim" if solvable(self.state) else "NÃO")

    def draw(self, state):
        for i, v in enumerate(state):
            c, l = self.tiles[i//3][i%3]
            if v == 0:
                c.config(bg="#0a0a0a"); l.config(text="", bg="#0a0a0a")
            else:
                bg, fg = CORES[v]
                c.config(bg=bg); l.config(text=str(v), bg=bg, fg=fg)

    # ── Resolver

    def solve(self):
        if self.busy: return
        self.busy = True
        self.sol  = []
        self.bsolve.config(state="disabled", text="Resolvendo...")
        self.banim.config(state="disabled")
        self.sv["status"].set("Processando...")
        self.pb.start(12)
        threading.Thread(target=self._solve_thread, daemon=True).start()

    def _solve_thread(self):
        t0 = time.time()
        best, gen, fit = genetic_algorithm(self.state, **self.params)
        elapsed = time.time() - t0
        sol, final = extract(self.state, best)
        self.sol = sol
        self.root.after(0, self._solve_done, gen, elapsed, sol, final == GOAL)

    def _solve_done(self, gen, elapsed, sol, ok):
        self.pb.stop()
        self.busy = False
        self.sv["status"].set("Solução encontrada!" if ok else "Parcial (limite atingido)")
        self.sv["geracoes"].set(str(gen))
        self.sv["movimentos"].set(str(len(sol)))
        self.sv["tempo"].set(f"{elapsed:.2f}s")
        self.bsolve.config(state="normal", text="▶  RESOLVER")
        if sol: self.banim.config(state="normal")

    # ── Animar

    def animate(self):
        if self.busy or not self.sol: return
        self.busy = True
        self.banim.config(state="disabled")
        self.bsolve.config(state="disabled")
        self.draw(self.state)
        threading.Thread(target=self._anim_thread, daemon=True).start()

    def _anim_thread(self):
        state = self.state
        delay = max(0.04, 0.55 - (self.spd.get() - 1) * 0.055)
        for i, m in enumerate(self.sol, 1):
            r = apply_move(state, m)
            if r:
                state = r
                self.root.after(0, self.draw, state)
                self.root.after(0, self.slbl.config, {"text": f"passo {i}/{len(self.sol)}"})
                time.sleep(delay)
        self.root.after(0, self._anim_done)

    def _anim_done(self):
        self.busy = False
        self.banim.config(state="normal")
        self.bsolve.config(state="normal")
        self.slbl.config(text="concluído ✓")
        self.sv["dist"].set("0")

    def reset(self):
        if not self.busy: self.load(self.pvar.get())

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
