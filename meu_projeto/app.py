import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Função para carregar fonte com suporte a negrito
def carregar_fonte(tamanho):
    try:
        # Verificando o caminho da fonte, ou usando uma fonte alternativa embutida
        fonte_path = os.path.join(os.path.dirname(__file__), "arialbd.ttf")
        if not os.path.exists(fonte_path):  # Se a fonte não for encontrada, usa uma fonte padrão
            fonte_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Fonte alternativa
        return ImageFont.truetype(fonte_path, tamanho)
    except Exception as e:
        print(f"Erro ao carregar a fonte: {e}")
        raise

# Função para gerar o crachá
def gerar_cracha(nome, rg, cpf, foto_path=None):
    try:
        # Caminho absoluto para o template
        template_path = os.path.join(os.path.dirname(__file__), "static", "template_cracha.jpg")
        
        # Verificar se o template existe
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template não encontrado: {template_path}")
        
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)

        # Configuração das fontes e tamanhos
        fonte_nome = carregar_fonte(35)  # Fonte maior para o nome
        fonte_dados = carregar_fonte(30)  # Fonte padrão para RG e CPF

        # Coordenadas para os campos de texto
        coord_nome = (50, 175)
        coord_rg = (50, 225)
        coord_cpf = (50, 275)

        # Coordenadas e tamanho da foto
        coord_foto = (220, 340)
        tamanho_foto = (225, 240)

        # Inserir o texto no template
        draw.text(coord_nome, f"Nome: {nome}", fill="black", font=fonte_nome)
        draw.text(coord_rg, f"RG: {rg}", fill="black", font=fonte_dados)
        draw.text(coord_cpf, f"CPF: {cpf}", fill="black", font=fonte_dados)

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
        return output_path

    except Exception as e:
        st.error(f"Erro ao gerar o crachá: {e}")

# Interface Streamlit
st.title("Gerador de Crachás")

# Criar colunas com mesmo tamanho e com espaçamento entre elas
col1, col2 = st.columns([1, 1])  # Ambas as colunas ocupam o mesmo tamanho (1:1)

# Adicionar um espaçamento entre as colunas
col1.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)  # Espaço acima da primeira coluna
col2.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)  # Espaço acima da segunda coluna

# Coluna da esquerda (campos de entrada)
with col1:
    st.markdown("### Preencha os dados abaixo")
    # Entrada de dados do usuário
    nome = st.text_input("Nome:")
    rg = st.text_input("RG:")
    cpf = st.text_input("CPF:")
    foto = st.file_uploader("Envie uma foto (opcional):", type=["jpg", "jpeg", "png"])

    # Botão para gerar o crachá
    if st.button("Gerar Crachá"):
        if nome and rg and cpf:
            # Salvar a foto carregada, se houver
            foto_path = None
            if foto:
                foto_path = os.path.join("static", "foto_temp.jpg")
                with open(foto_path, "wb") as f:
                    f.write(foto.read())
            # Gerar o crachá
            output_path = gerar_cracha(nome, rg, cpf, foto_path)
            if output_path:
                st.success("Crachá gerado com sucesso!")
                # Exibe o crachá gerado na coluna da direita
                with col2:
                    st.image(output_path, use_container_width=True)  # Usando container_width para a imagem se ajustar
                    # Botão para baixar o crachá
                    st.download_button(label="Baixar Crachá", data=open(output_path, "rb"), file_name="cracha_gerado.png", mime="image/png")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")
