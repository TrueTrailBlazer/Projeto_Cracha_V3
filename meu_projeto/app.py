import os
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Configurações
COR_TEXTO = "black"
TAMANHO_FONTES = {"nome": 45, "dados": 38}
COORDENADAS = {
    "nome": (50, 170),
    "rg": (50, 220),
    "cpf": (50, 270),
    "foto": (220, 330),
    "tamanho_foto": (230, 250)
}

def carregar_fonte(tamanho: int) -> ImageFont.FreeTypeFont:
    """Carrega fonte com fallback seguro"""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
    except IOError:
        try:
            return ImageFont.truetype("arial.ttf", tamanho)
        except IOError:
            return ImageFont.load_default().font_variant(size=tamanho)

def processar_foto(arquivo_enviado) -> str:
    """Processa foto com tratamento de recursos"""
    if not arquivo_enviado:
        return None
        
    try:
        with Image.open(arquivo_enviado) as img:
            img.verify()
            arquivo_enviado.seek(0)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(arquivo_enviado.read())
                return tmp.name
    except Exception as e:
        st.error(f"Erro na foto: {str(e)}")
        return None

def gerar_cracha(nome: str, rg: str, cpf: str, caminho_foto: str = None) -> bytes:
    """Gera crachá com tratamento robusto de erros"""
    try:
        caminho_template = Path(__file__).parent / "static/template_cracha.jpg"
        with Image.open(caminho_template) as template:
            desenho = ImageDraw.Draw(template)

            # Adicionar textos
            fonte_nome = carregar_fonte(TAMANHO_FONTES["nome"])
            desenho.text(COORDENADAS["nome"], f"Nome: {nome}", fill=COR_TEXTO, font=fonte_nome)
            desenho.text(COORDENADAS["rg"], f"RG: {rg}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))
            desenho.text(COORDENADAS["cpf"], f"CPF: {cpf}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))

            # Adicionar foto
            if caminho_foto:
                with Image.open(caminho_foto) as foto:
                    foto.thumbnail(COORDENADAS["tamanho_foto"])
                    template.paste(foto.convert("RGB"), COORDENADAS["foto"])

            # Gerar bytes
            buffer = BytesIO()
            template.save(buffer, format="PNG")
            return buffer.getvalue()

    except Exception as e:
        st.error(f"Falha crítica: {str(e)}")
        return None

def main():
    st.title("Gerador de Crachás Definitivo")
    
    with st.form("form_cracha"):
        nome = st.text_input("Nome completo:", max_chars=50)
        rg = st.text_input("RG:", max_chars=15)
        cpf = st.text_input("CPF:", max_chars=14)
        foto = st.file_uploader("Foto (opcional):", type=["jpg", "jpeg", "png"])
        
        if st.form_submit_button("Gerar Crachá"):
            if not all([nome, rg, cpf]):
                st.error("Preencha todos os campos!")
                return

            try:
                with st.spinner("Processando..."):
                    foto_path = processar_foto(foto)
                    badge_data = gerar_cracha(nome, rg, cpf, foto_path)
                    
                    if badge_data:
                        st.success("Pronto!")
                        st.image(badge_data)
                        
                        # Botão de download isolado
                        st.markdown("---")
                        st.download_button(
                            label="⬇️ Download do Crachá",
                            data=badge_data,
                            file_name=f"cracha_{nome[:20].replace(' ', '_')}.png",
                            mime="image/png",
                            key="unique_download_button"
                        )
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()
