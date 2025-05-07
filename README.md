Gerador de Crachás em Python com Streamlit
==========================================

Um gerador de crachás simples e funcional, feito com carinho em Python + Streamlit. Você insere os dados, escolhe uma foto (ou não) e gere o crachá com os dados.

🔗 Acesse o app online:
https://projetocrachav3-dnuusncivg5dpvybaena55.streamlit.app/

----------------------------------------

FUNCIONALIDADES

- Geração de crachás personalizados com:
  - Nome
  - RG
  - CPF
  - Foto (opcional)
- Interface web feita com Streamlit
- Geração automática de imagem .png
- Fontes com negrito para um visual mais profissional
- Tratamento de erros e mensagens amigáveis

----------------------------------------

REQUISITOS

- Python 3.7 ou superior
- As bibliotecas:
  - Pillow
  - Streamlit

Instale com:

pip install pillow streamlit

----------------------------------------

ESTRUTURA ESPERADA DO PROJETO

projeto/
├── gerador_cracha.py
├── static/
│   ├── template_cracha.jpg
│   └── foto_temp.jpg (gerado em tempo de execução)
├── arialbd.ttf (opcional - fonte negrito)

* Caso a fonte "arialbd.ttf" não seja encontrada, será usada uma alternativa padrão do sistema.

----------------------------------------

TEMPLATE DO CRACHÁ

O sistema usa uma imagem base chamada "template_cracha.jpg", localizada na pasta "static". Personalize esse template conforme a sua necessidade, mantendo espaço livre para os dados e a foto.

----------------------------------------

COMO EXECUTAR LOCALMENTE

Abra o terminal na pasta do projeto e execute:

streamlit run gerador_cracha.py

A aplicação abrirá automaticamente no navegador.

----------------------------------------

OBSERVAÇÕES

- A imagem final do crachá será salva como "cracha_gerado.png" na raiz do projeto.
- A foto, se fornecida, será redimensionada automaticamente para o espaço definido no template.
- Todos os campos (exceto a foto) são obrigatórios.

----------------------------------------
