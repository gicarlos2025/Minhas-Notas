# Minhas Notas

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-3776AB)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Aplicativo simples de bloco de notas em Python com interface gráfica usando Tkinter.

## Sobre o projeto

Este projeto foi criado como um editor de texto leve, com foco em simplicidade, usabilidade e boa organização do código. Ele inclui operações básicas de edição, controle de arquivos e estatísticas do texto.

## Funcionalidades

- Novo arquivo
- Abrir arquivos de texto
- Salvar e salvar como
- Contagem de linhas, palavras e caracteres
- Ajuste de fonte
- Menu Editar com:
  - Copiar
  - Recortar
  - Colar
  - Selecionar tudo
- Compatibilidade com Linux, Windows e macOS

## Requisitos

- Python 3.9+
- Tkinter instalado no ambiente

### Linux

#### Fedora / RHEL / CentOS

```bash
sudo dnf install python3-tkinter
```

#### Ubuntu / Debian

```bash
sudo apt install python3-tk
```

#### Arch Linux

```bash
sudo pacman -S tk
```

### Windows

Use uma instalação oficial do Python e garanta que o módulo Tkinter esteja disponível.

### macOS

```bash
brew install python
```

## Como executar

Na raiz do projeto:

```bash
python3 MinhasNotas.py
```

No Windows:

```powershell
python MinhasNotas.py
```

## Testes

```bash
python -m unittest -q test_minhas_notas.py
```

## Estrutura do projeto

```text
.
├── MinhasNotas.py
├── test_minhas_notas.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── Notepad.png
├── Notepad.ico
├── .github/
│   └── workflows/
│       └── ci.yml
└── build/
```

## Observações de compatibilidade

- O projeto usa `tk.PhotoImage` com PNG para melhor compatibilidade em Linux/macOS.
- O arquivo `.ico` permanece disponível para cenários específicos no Windows.
- A lógica de domínio foi separada da camada gráfica para facilitar manutenção e testes.

## Contribuição

Contribuições são bem-vindas. Para propor melhorias ou correções:

1. Faça um fork do projeto
2. Crie uma branch para a funcionalidade
3. Envie um pull request com descrição clara

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
