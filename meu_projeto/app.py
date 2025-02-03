import os
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Configurações ajustadas para as coordenadas solicitadas
COR_TEXTO = "black"
TAMANHO_FONTES = {"nome": 40, "dados": 35}
COORDENADAS = {
    "nome": (50, 175),
    "rg": (50, 225),
    "cpf": (50, 275),
    "foto": (220, 340),  # Coordenadas atualizadas
    "tamanho_foto": (225, 240)  # Tamanho atualizado
}

def carregar_fonte(tamanho: int) -> ImageFont.FreeTypeFont:
    """Carrega fonte com fallback seguro para acentos"""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
    except IOError:
        try:
            return ImageFont.truetype("arial.ttf", tamanho)
        except IOError:
            return ImageFont.load_default().font_variant(size=tamanho)

def processar_foto(arquivo_enviado) -> str:
    """Processa e redimensiona a foto para as dimensões corretas"""
    if not arquivo_enviado:
        return None
        
    try:
        with Image.open(arquivo_enviado) as img:
            img.verify()
            arquivo_enviado.seek(0)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                img.convert("RGB").resize(COORDENADAS["tamanho_foto"]).save(tmp, format="JPEG")
                return tmp.name
    except Exception as e:
        st.error(f"Erro na foto: {str(e)}")
        return None

def gerar_cracha(nome: str, rg: str, cpf: str, caminho_foto: str = None) -> bytes:
    """Gera o crachá com as coordenadas especificadas"""
    try:
        caminho_template = Path(__file__).parent / "static/template_cracha.jpg"
        with Image.open(caminho_template) as template:
            desenho = ImageDraw.Draw(template)

            # Adicionar textos
            desenho.text(COORDENADAS["nome"], f"Nome: {nome}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["nome"]))
            desenho.text(COORDENADAS["rg"], f"RG: {rg}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))
            desenho.text(COORDENADAS["cpf"], f"CPF: {cpf}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))

            # Adicionar foto redimensionada
            if caminho_foto:
                with Image.open(caminho_foto) as foto:
                    foto_resized = foto.resize(COORDENADAS["tamanho_foto"])
                    template.paste(foto_resized, COORDENADAS["foto"])

            # Gerar bytes da imagem
            buffer = BytesIO()
            template.save(buffer, format="PNG")
            return buffer.getvalue()

    except Exception as e:
        st.error(f"Erro na geração: {str(e)}")
        return None

def main():
    st.title("Gerador de Crachás Oficial")
    
    # Usar session_state para manter o crachá gerado
    if 'badge_data' not in st.session_state:
        st.session_state.badge_data = None
    
    with st.form("form_cracha"):
        nome = st.text_input("Nome completo:", max_chars=50)
        rg = st.text_input("RG:", max_chars=15)
        cpf = st.text_input("CPF:", max_chars=14)
        foto = st.file_uploader("Foto (opcional):", type=["jpg", "jpeg", "png"])
        
        if st.form_submit_button("Gerar Crachá"):
            if not all([nome, rg, cpf]):
                st.error("Preencha todos os campos obrigatórios!")
            else:
                with st.spinner("Processando..."):
                    foto_path = processar_foto(foto)
                    st.session_state.badge_data = gerar_cracha(nome, rg, cpf, foto_path)

    # Mostrar resultados fora do formulário
    if st.session_state.badge_data:
        st.success("Cracha gerado com sucesso!")
        st.image(st.session_state.badge_data)
        
        # Botão de download separado do formulário
        st.download_button(
            label="Baixar Crachá",
            data=st.session_state.badge_data,
            file_name=f"cracha_{nome[:20].replace(' ', '_')}.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
