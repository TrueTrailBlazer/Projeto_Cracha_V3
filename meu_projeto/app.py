import os
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Configurações (ajuste conforme seu template)
COR_TEXTO = "black"
TAMANHO_FONTES = {"nome": 40, "dados": 35}
COORDENADAS = {
    "nome": (50, 175),
    "rg": (50, 225),
    "cpf": (50, 275),
    "foto": (220, 340),
    "tamanho_foto": (225, 240)
}

def carregar_fonte(tamanho: int) -> ImageFont.FreeTypeFont:
    """Carrega fonte com fallback para diferentes sistemas"""
    try:
        # Tenta primeiro a fonte Arial Bold
        return ImageFont.truetype("arialbd.ttf", tamanho)
    except IOError:
        try:  # Fallback para fonte comum
            return ImageFont.truetype("arial.ttf", tamanho)
        except IOError:
            return ImageFont.load_default()  # Último fallback

def processar_foto(arquivo_enviado) -> str:
    """Processa e valida a foto enviada"""
    if not arquivo_enviado:
        return None
        
    try:
        img = Image.open(arquivo_enviado)
        img.verify()
        arquivo_enviado.seek(0)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(arquivo_enviado.read())
            return tmp.name
    except Exception as e:
        st.error(f"Erro no processamento da foto: {str(e)}")
        return None

def gerar_cracha(nome: str, rg: str, cpf: str, caminho_foto: str = None) -> bytes:
    """Gera o crachá em memória e retorna bytes PNG"""
    try:
        # Carrega template
        caminho_template = Path(__file__).parent / "static/template_cracha.jpg"
        if not caminho_template.exists():
            raise FileNotFoundError(f"Template não encontrado em {caminho_template}")
            
        template = Image.open(caminho_template)
        desenho = ImageDraw.Draw(template)

        # Adiciona textos
        desenho.text(
            COORDENADAS["nome"], 
            f"Nome: {nome}", 
            fill=COR_TEXTO, 
            font=carregar_fonte(TAMANHO_FONTES["nome"])
        )
        desenho.text(
            COORDENADAS["rg"], 
            f"RG: {rg}", 
            fill=COR_TEXTO, 
            font=carregar_fonte(TAMANHO_FONTES["dados"])
        )
        desenho.text(
            COORDENADAS["cpf"], 
            f"CPF: {cpf}", 
            fill=COR_TEXTO, 
            font=carregar_fonte(TAMANHO_FONTES["dados"])
        )

        # Adiciona foto
        if caminho_foto:
            foto = Image.open(caminho_foto).convert("RGB")
            foto.thumbnail(COORDENADAS["tamanho_foto"])
            template.paste(foto, COORDENADAS["foto"])

        # Salva em memória
        buffer_imagem = BytesIO()
        template.save(buffer_imagem, format="PNG")
        return buffer_imagem.getvalue()

    except Exception as e:
        st.error(f"Erro na geração do crachá: {str(e)}")
        return None

# Interface do usuário
def main():
    st.title("Gerador de Crachás Oficial")
    
    with st.form("formulario_cracha"):
        nome = st.text_input("Nome completo:", max_chars=50)
        rg = st.text_input("RG:", max_chars=15)
        cpf = st.text_input("CPF:", max_chars=14)
        foto = st.file_uploader("Foto (opcional):", type=["jpg", "jpeg", "png"])
        
        if st.form_submit_button("Gerar Crachá"):
            if not all([nome, rg, cpf]):
                st.error("Preencha todos os campos obrigatórios!")
                return
                
            caminho_foto = processar_foto(foto)
            dados_cracha = gerar_cracha(nome, rg, cpf, caminho_foto)
            
            if dados_cracha:
                st.success("Cracha gerado com sucesso!")
                st.image(dados_cracha)
                st.download_button(
                    "Baixar Crachá",
                    data=dados_cracha,
                    file_name=f"cracha_{nome.replace(' ', '_')}.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()
