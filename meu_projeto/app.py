import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Função para carregar a fonte
def carregar_fonte(tamanho):
    try:
        # Tente carregar a fonte padrão Arial
        return ImageFont.truetype("arial.ttf", tamanho)
    except IOError:
        # Caminho alternativo para Arial no Windows
        fonte_alternativa = os.path.join("C:\\Windows\\Fonts", "arial.ttf")
        if os.path.exists(fonte_alternativa):
            return ImageFont.truetype(fonte_alternativa, tamanho)
        else:
            # Fonte genérica do PIL se Arial não estiver disponível
            return ImageFont.load_default()

# Função para gerar o crachá
def gerar_cracha(nome, rg, cpf, foto_path=None):
    try:
        # Caminho absoluto do template
        template_path = os.path.join(os.path.dirname(__file__), 'static', 'template_cracha.jpg')

        # Abrir o template
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)

        # Carregar a fonte
        fonte = carregar_fonte(37)

        # Coordenadas para os campos de texto
        coord_nome = (50, 175)
        coord_rg = (50, 225)
        coord_cpf = (50, 275)

        # Adicionar os textos
        draw.text(coord_nome, f"Nome: {nome}", fill="black", font=fonte)
        draw.text(coord_rg, f"RG: {rg}", fill="black", font=fonte)
        draw.text(coord_cpf, f"CPF: {cpf}", fill="black", font=fonte)

        # Coordenadas e tamanho da foto
        coord_foto = (220, 340)
        tamanho_foto = (225, 240)

        # Adicionar a foto, se fornecida
        if foto_path:
            try:
                foto = Image.open(foto_path).resize(tamanho_foto)
                template.paste(foto, coord_foto)
            except Exception as e:
                st.error(f"Erro ao processar a foto: {e}")

        # Salvar o crachá gerado
        output_path = "cracha_gerado.png"
        template.save(output_path)
        template.close()

        return output_path
    except Exception as e:
        st.error(f"Erro ao gerar o crachá: {e}")
        return None

# Interface do Streamlit
st.title("Gerador de Crachá")

# Entradas do usuário
nome = st.text_input("Digite o nome:")
rg = st.text_input("Digite o RG:")
cpf = st.text_input("Digite o CPF:")
foto = st.file_uploader("Envie a foto do usuário (opcional)", type=["jpg", "jpeg", "png"])

# Botão para gerar o crachá
if st.button("Gerar Crachá"):
    if nome and rg and cpf:
        foto_path = None
        if foto:
            foto_path = os.path.join(os.getcwd(), foto.name)
            with open(foto_path, "wb") as f:
                f.write(foto.read())

        # Gerar o crachá
        cracha_path = gerar_cracha(nome, rg, cpf, foto_path)
        if cracha_path:
            st.success("Crachá gerado com sucesso!")
            st.image(cracha_path, caption="Crachá Gerado")
    else:
        st.error("Preencha todos os campos obrigatórios!")
