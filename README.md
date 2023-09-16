# Projeto para automatizar a coleta de dados dos perfis do Becrowd

## Como usar

1. Com o python já configurado na máquina, instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

2. Após a instalação das dependências, execute o comando para instalar os pacotes do Playwright:

```bash
playwright install
```

> OBS: O comando abaixo é para instalar as dependências do Playwright, caso ocorra algum erro, execute o comando abaixo e tente novamente:

```bash
playwright install-deps
```

3. Execute o script:

```bash
python main.py
```

## Funcionamento

O programa vai fazer download dos dados da lista de IDs que será recebida, após executada vai criar o arquivo profiles_data.json
