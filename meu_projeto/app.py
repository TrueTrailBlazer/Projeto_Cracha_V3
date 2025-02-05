import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Configurações definitivas
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
    """Carrega fonte com fallback seguro"""
    try:
        return ImageFont.truetype("arial.ttf", tamanho)
    except IOError:
        try:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
        except:
            return ImageFont.load_default(tamanho)

def processar_foto(uploaded_file) -> str:
    """Processamento de foto totalmente reformulado"""
    if not uploaded_file:
        return None

    try:
        # Salvar diretamente em arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            # Escrever conteúdo original
            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        # Processar a imagem
        with Image.open(temp_path) as img:
            # Verificar e redimensionar
            img.verify()
            img = img.convert("RGB")
            img = img.resize(COORDENADAS["tamanho_foto"])
            
            # Sobrescrever com versão processada
            img.save(temp_path, "JPEG", quality=90)

        return temp_path

    except Exception as e:
        st.error(f"Erro na foto: {str(e)}")
        return None

def gerar_cracha(nome: str, rg: str, cpf: str, caminho_foto: str = None) -> bytes:
    """Geração do crachá com tratamento robusto"""
    try:
        template_path = Path(__file__).parent / "static/template_cracha.jpg"
        with Image.open(template_path) as template:
            draw = ImageDraw.Draw(template)

            # Textos com verificação de fonte
            fonte_nome = carregar_fonte(TAMANHO_FONTES["nome"])
            draw.text(COORDENADAS["nome"], f"Nome: {nome}", fill=COR_TEXTO, font=fonte_nome)
            draw.text(COORDENADAS["rg"], f"RG: {rg}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))
            draw.text(COORDENADAS["cpf"], f"CPF: {cpf}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))

            # Foto com posicionamento exato
            if caminho_foto:
                with Image.open(caminho_foto) as foto:
                    template.paste(foto, COORDENADAS["foto"])

            # Saída em memória
            buffer = BytesIO()
            template.save(buffer, format="PNG")
            return buffer.getvalue()

    except Exception as e:
        st.error(f"Falha na geração: {str(e)}")
        return None

def main():
    st.title("Gerador de Crachás Final")
    
    if 'badge_data' not in st.session_state:
        st.session_state.badge_data = None
    
    with st.form(key="form_principal"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome completo:", max_chars=50)
            rg = st.text_input("RG:", max_chars=15)
            cpf = st.text_input("CPF:", max_chars=14)
            
        with col2:
            foto = st.file_uploader("Upload da foto:", type=["jpg", "jpeg", "png"])
        
        if st.form_submit_button("🖨️ Gerar Crachá"):
            if not all([nome, rg, cpf]):
                st.error("Preencha nome, RG e CPF!")
            else:
                with st.spinner("Processando..."):
                    foto_path = processar_foto(foto)
                    st.session_state.badge_data = gerar_cracha(nome, rg, cpf, foto_path)

    # Exibição fora do formulário
    if st.session_state.badge_data:
        st.success("✅ Crachá pronto para download!")
        st.image(st.session_state.badge_data)
        
        st.download_button(
            "📥 Download do Crachá",
            data=st.session_state.badge_data,
            file_name=f"cracha_{nome[:30].replace(' ', '_')}.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
# Configurações atualizadas com as coordenadas solicitadas
COR_TEXTO = "black"
TAMANHO_FONTES = {"nome": 40, "dados": 35}
COORDENADAS = {
    "nome": (50, 175),
    "rg": (50, 225),
    "cpf": (50, 275),
    "foto": (220, 340),  # Posição exata solicitada
    "tamanho_foto": (225, 240)  # Dimensões exatas
}

def carregar_fonte(tamanho: int) -> ImageFont.FreeTypeFont:
    """Carrega fonte com suporte a caracteres especiais"""
    try:
        return ImageFont.truetype("arial.ttf", tamanho)
    except IOError:
        try:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho)
        except:
            return ImageFont.load_default(tamanho)

def processar_foto(uploaded_file) -> str:
    """Processa a foto com tratamento seguro de arquivos"""
    if not uploaded_file:
        return None

    try:
        # Criar buffer independente
        file_bytes = BytesIO(uploaded_file.read())
        file_bytes.seek(0)
        
        with Image.open(file_bytes) as img:
            img.verify()
            file_bytes.seek(0)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                img.convert("RGB").resize(COORDENADAS["tamanho_foto"]).save(tmp, format="JPEG")
                return tmp.name
                
    except Exception as e:
        st.error(f"Erro na foto: {str(e)}")
        return None

def gerar_cracha(nome: str, rg: str, cpf: str, caminho_foto: str = None) -> bytes:
    """Gera o crachá com posicionamento preciso"""
    try:
        template_path = Path(__file__).parent / "static/template_cracha.jpg"
        with Image.open(template_path) as template:
            draw = ImageDraw.Draw(template)

            # Adicionar textos
            draw.text(COORDENADAS["nome"], f"Nome: {nome}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["nome"]))
            draw.text(COORDENADAS["rg"], f"RG: {rg}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))
            draw.text(COORDENADAS["cpf"], f"CPF: {cpf}", fill=COR_TEXTO, font=carregar_fonte(TAMANHO_FONTES["dados"]))

            # Adicionar foto redimensionada
            if caminho_foto:
                with Image.open(caminho_foto) as foto:
                    foto_resized = foto.resize(COORDENADAS["tamanho_foto"])
                    template.paste(foto_resized, COORDENADAS["foto"])

            # Salvar em memória
            buffer = BytesIO()
            template.save(buffer, format="PNG")
            return buffer.getvalue()

    except Exception as e:
        st.error(f"Erro na geração: {str(e)}")
        return None

def main():
    st.title("Gerador de Crachás 2.0")
    
    st.session_state.badge_data = None
    
    with st.form("main_form"):
        nome = st.text_input("Nome completo:", max_chars=50)
        rg = st.text_input("RG:", max_chars=15)
        cpf = st.text_input("CPF:", max_chars=14)
        foto = st.file_uploader("Foto (opcional):", type=["jpg", "jpeg", "png"])
        
        if st.form_submit_button("Gerar Crachá"):
            if not all([nome, rg, cpf]):
                st.error("Preencha os campos obrigatórios!")
            else:
                with st.spinner("Criando crachá..."):
                    foto_path = processar_foto(foto)
                    st.session_state.badge_data = gerar_cracha(nome, rg, cpf, foto_path)

    # Exibição fora do formulário
    if st.session_state.badge_data:
        st.success("Pronto!")
        st.image(st.session_state.badge_data)
        st.download_button(
            "Baixar Crachá",
            data=st.session_state.badge_data,
            file_name=f"cracha_{nome.replace(' ', '_')}.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
