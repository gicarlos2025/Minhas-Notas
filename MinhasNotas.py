import os
import sys
import ctypes
from dataclasses import dataclass

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, font
except ModuleNotFoundError:  # pragma: no cover - ambiente sem suporte ao GUI
    tk = None
    filedialog = None
    messagebox = None
    font = None


__all__ = ["BlocoDeNotas", "EstatisticasTexto", "RepositorioArquivosTexto"]


@dataclass(frozen=True)
class ConfiguracaoFonte:
    familia: str = "Segoe UI"
    tamanho: int = 12


class EstatisticasTexto:
    @staticmethod
    def calcular(conteudo: str) -> dict[str, int]:
        texto = conteudo or ""
        linhas = len(texto.splitlines()) if texto else 1
        palavras = len(texto.split()) if texto.strip() else 0
        caracteres = len(texto)
        return {"linhas": linhas, "palavras": palavras, "caracteres": caracteres}


class RepositorioArquivosTexto:
    @staticmethod
    def salvar(caminho: str, conteudo: str) -> None:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

    @staticmethod
    def ler(caminho: str) -> str:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def aplicar_icone_janela(janela, caminho_icone):
    caminho = get_resource_path(caminho_icone)
    if not os.path.exists(caminho):
        return

    try:
        if caminho.lower().endswith(".png"):
            imagem = tk.PhotoImage(file=caminho)
            janela.iconphoto(True, imagem)
        else:
            janela.iconbitmap(caminho)
    except Exception:
        try:
            janela.iconbitmap(caminho)
        except Exception:
            pass


class BlocoDeNotas:
    def __init__(self, root):
        if tk is None:
            raise RuntimeError("Tkinter não está disponível neste ambiente.")

        self.root = root
        self.root.title("Minhas Notas")
        self.root.geometry("900x640")
        self.root.minsize(700, 480)
        self.root.configure(bg="#f3f4f6")

        self.caminho_arquivo = None
        self.configuracao_fonte = ConfiguracaoFonte()
        self.fonte_texto = font.Font(
            family=self.configuracao_fonte.familia,
            size=self.configuracao_fonte.tamanho,
        )
        self.menu_bar = tk.Menu(self.root, bg="#ffffff", fg="#1f2937", activebackground="#e5e7eb", activeforeground="#111827", tearoff=0)
        self.root.config(menu=self.menu_bar)

        self.menu_arquivo = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.menu_arquivo.add_command(label="Novo", accelerator="Ctrl+N", command=self.novo_arquivo)
        self.menu_arquivo.add_command(label="Abrir...", accelerator="Ctrl+O", command=self.abrir_arquivo)
        self.menu_arquivo.add_command(label="Salvar", accelerator="Ctrl+S", command=self.salvar_arquivo)
        self.menu_arquivo.add_command(label="Salvar Como...", command=self.salvar_como)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label="Sair", command=self.root.quit)

        self.menu_editar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.menu_editar)
        self.menu_editar.add_command(label="Copiar", accelerator="Ctrl+C", command=self.copiar_texto)
        self.menu_editar.add_command(label="Recortar", accelerator="Ctrl+X", command=self.recortar_texto)
        self.menu_editar.add_command(label="Colar", accelerator="Ctrl+V", command=self.colar_texto)
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label="Selecionar Tudo", accelerator="Ctrl+A", command=self.selecionar_tudo)

        self.menu_formatar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Formatar", menu=self.menu_formatar)
        self.menu_formatar.add_command(label="Fonte...", command=self.abrir_janela_fonte)

        self.menu_ajuda = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.menu_ajuda.add_command(label="Sobre Minhas Notas", command=self.abrir_janela_sobre)

        self.barra_status = tk.Label(
            self.root,
            text="Linhas: 1 | Palavras: 0 | Caracteres: 0",
            anchor="e",
            padx=14,
            pady=6,
            bg="#eef2f7",
            fg="#374151",
            relief="flat",
            font=("Segoe UI", 9),
        )
        self.barra_status.pack(side="bottom", fill="x")

        container_texto = tk.Frame(self.root, bg="#f3f4f6")
        container_texto.pack(fill="both", expand=True, padx=12, pady=(10, 8))

        self.texto = tk.Text(
            container_texto,
            font=self.fonte_texto,
            wrap="word",
            undo=True,
            padx=12,
            pady=12,
            bg="#ffffff",
            fg="#111827",
            insertbackground="#111827",
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#dfe3eb",
            highlightcolor="#93c5fd",
        )
        self.texto.pack(fill="both", expand=True, side="left")

        self.scrollbar = tk.Scrollbar(container_texto, command=self.texto.yview, troughcolor="#f3f4f6", width=12)
        self.scrollbar.pack(side="right", fill="y")
        self.texto.config(yscrollcommand=self.scrollbar.set)

        self.texto.bind("<KeyRelease>", self.atualizar_status)
        self.texto.bind("<<Modified>>", self.ao_modificar_conteudo)

        self.root.bind("<Control-n>", lambda event: self.novo_arquivo())
        self.root.bind("<Control-o>", lambda event: self.abrir_arquivo())
        self.root.bind("<Control-s>", lambda event: self.salvar_arquivo())
        self.root.bind("<Control-c>", lambda event: self.copiar_texto())
        self.root.bind("<Control-x>", lambda event: self.recortar_texto())
        self.root.bind("<Control-v>", lambda event: self.colar_texto())
        self.root.bind("<Control-a>", lambda event: self.selecionar_tudo())

    def atualizar_status(self, event=None):
        conteudo = self.texto.get("1.0", "end-1c")
        estatisticas = EstatisticasTexto.calcular(conteudo)
        self.barra_status.config(
            text=(
                f"Linhas: {estatisticas['linhas']} | "
                f"Palavras: {estatisticas['palavras']} | "
                f"Caracteres: {estatisticas['caracteres']}"
            )
        )

    def ao_modificar_conteudo(self, event=None):
        if self.texto.edit_modified():
            self.atualizar_status()
            self.texto.edit_modified(False)

    def carregar_texto(self, conteudo: str) -> None:
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, conteudo)
        self.atualizar_status()

    def copiar_texto(self):
        try:
            self.texto.clipboard_clear()
            self.texto.clipboard_append(self.texto.get("sel.first", "sel.last"))
        except TclError:
            pass

    def recortar_texto(self):
        try:
            self.texto.event_generate("<<Cut>>")
        except Exception:
            pass

    def colar_texto(self):
        try:
            self.texto.event_generate("<<Paste>>")
        except Exception:
            pass

    def selecionar_tudo(self):
        self.texto.tag_add("sel", "1.0", "end-1c")
        self.texto.mark_set("insert", "1.0")
        self.texto.see("insert")

    def novo_arquivo(self):
        self.texto.delete("1.0", tk.END)
        self.caminho_arquivo = None
        self.root.title("Sem título - Minhas Notas")
        self.atualizar_status()

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            try:
                conteudo = RepositorioArquivosTexto.ler(caminho)
                self.carregar_texto(conteudo)
                self.caminho_arquivo = caminho
                self.root.title(f"{caminho} - Minhas Notas")
            except Exception as error:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{error}")

    def salvar_arquivo(self):
        if self.caminho_arquivo:
            try:
                conteudo = self.texto.get("1.0", tk.END)
                RepositorioArquivosTexto.salvar(self.caminho_arquivo, conteudo)
                self.root.title(f"{self.caminho_arquivo} - Minhas Notas")
            except Exception as error:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{error}")
        else:
            self.salvar_como()

    def salvar_como(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
        )
        if caminho:
            self.caminho_arquivo = caminho
            self.salvar_arquivo()

    def abrir_janela_fonte(self):
        janela_fonte = tk.Toplevel(self.root)
        janela_fonte.title("Formatar Fonte")
        janela_fonte.geometry("320x180")
        janela_fonte.resizable(False, False)
        aplicar_icone_janela(janela_fonte, "Notepad.png")

        tk.Label(janela_fonte, text="Família da Fonte:").pack(pady=(10, 0))
        var_familia = tk.StringVar(value=self.configuracao_fonte.familia)
        combo_fontes = tk.OptionMenu(
            janela_fonte,
            var_familia,
            "Segoe UI",
            "Arial",
            "Consolas",
            "Courier New",
            "Times New Roman",
        )
        combo_fontes.pack()

        tk.Label(janela_fonte, text="Tamanho:").pack(pady=(10, 0))
        var_tamanho = tk.IntVar(value=self.configuracao_fonte.tamanho)
        spin_tamanho = tk.Spinbox(janela_fonte, from_=8, to=72, textvariable=var_tamanho, width=5)
        spin_tamanho.pack()

        def aplicar():
            self.configuracao_fonte = ConfiguracaoFonte(
                familia=var_familia.get(),
                tamanho=var_tamanho.get(),
            )
            self.fonte_texto.config(
                family=self.configuracao_fonte.familia,
                size=self.configuracao_fonte.tamanho,
            )
            janela_fonte.destroy()

        tk.Button(janela_fonte, text="Aplicar", command=aplicar, width=10).pack(pady=15)

    def abrir_janela_sobre(self):
        janela_sobre = tk.Toplevel(self.root)
        janela_sobre.title("Sobre o Bloco de Notas")
        janela_sobre.geometry("360x180")
        janela_sobre.resizable(False, False)
        aplicar_icone_janela(janela_sobre, "Notepad.png")

        janela_sobre.transient(self.root)
        janela_sobre.grab_set()

        frame_info = tk.Frame(janela_sobre, padx=20, pady=20)
        frame_info.pack(fill="both", expand=True)

        tk.Label(frame_info, text="Minhas Notas", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(
            frame_info,
            text="Versão 1.0.0\nDesenvolvido por Gian Silva\nTodos os direitos reservados.",
            justify="left",
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(8, 15))

        tk.Button(frame_info, text="OK", width=10, command=janela_sobre.destroy).pack(anchor="e")


if __name__ == "__main__":
    if tk is None:
        raise RuntimeError("Tkinter não está disponível. Instale o pacote python3-tk para executar a aplicação.")

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("meuapp.blocodenotas.1.0")
    except Exception:
        pass

    app_root = tk.Tk()
    aplicar_icone_janela(app_root, "Notepad.png")
    app = BlocoDeNotas(app_root)
    app_root.mainloop()