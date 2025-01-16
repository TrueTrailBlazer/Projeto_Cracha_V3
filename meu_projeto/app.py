import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Caminho fixo para o template do crachá
TEMPLATE_PATH = "static/template_cracha.jpg"

# Função para gerar o crachá
def gerar_cracha(nome, rg, cpf, foto_path=None):
    try:
        # Abrir o template
        template = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(template)

        # Definir a fonte e as coordenadas do texto
        fonte = ImageFont.truetype("arial.ttf", 37)  # Substitua por uma fonte válida no seu sistema
        coord_nome = (50, 175)
        coord_rg = (50, 225)
        coord_cpf = (50, 275)

        # Adicionar os textos ao template
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

# Configuração do Streamlit
st.title("Gerador de Crachás")
st.write("Preencha as informações abaixo e envie a foto da pessoa para gerar o crachá.")

# Entradas do usuário
nome = st.text_input("Nome")
rg = st.text_input("RG")
cpf = st.text_input("CPF")
foto_file = st.file_uploader("Faça upload de uma foto", type=["jpg", "png", "jpeg"])

# Botão para gerar o crachá
if st.button("Gerar Crachá"):
    if not nome or not rg or not cpf:
        st.error("Por favor, preencha todos os campos de texto.")
    else:
        foto_path = None
        if foto_file:
            foto_path = f"temp_foto_{foto_file.name}"
            with open(foto_path, "wb") as f:
                f.write(foto_file.getbuffer())

        # Gerar o crachá
        output_path = gerar_cracha(nome, rg, cpf, foto_path)

        if output_path:
            st.success("Crachá gerado com sucesso!")
            st.image(output_path, caption="Crachá Gerado", use_column_width=True)
