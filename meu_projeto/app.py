import os
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Constants (adjust these according to your template)
TEXT_COLOR = "black"
FONT_SIZES = {"name": 40, "data": 35}
COORDINATES = {
    "name": (50, 175),
    "rg": (50, 225),
    "cpf": (50, 275),
    "photo": (220, 340),
    "photo_size": (225, 240)
}

def load_font(font_size: int, font_path: str = None) -> ImageFont.FreeTypeFont:
    """Load font with fallback strategy."""
    try:
        font_path = font_path or os.path.join("fonts", "arialbd.ttf")
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        try:  # Try system fallback font
            return ImageFont.truetype("arialbd.ttf", font_size)
        except IOError:
            return ImageFont.load_default()  Ultimate fallback

def process_photo(uploaded_file) -> str:
    """Process and save uploaded photo with validation."""
    if not uploaded_file:
        return None
        
    try:
        img = Image.open(uploaded_file)
        img.verify()  # Basic image validation
        uploaded_file.seek(0)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.read())
            return tmp.name
    except Exception as e:
        st.error(f"Invalid image file: {str(e)}")
        return None

def generate_badge(name: str, rg: str, cpf: str, photo_path: str = None) -> str:
    """Generate badge image with user information."""
    try:
        # Load template
        template_path = Path(__file__).parent / "static/template_cracha.jpg"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found at {template_path}")
            
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)

        # Add text information
        draw.text(COORDINATES["name"], f"Nome: {name}", 
                 fill=TEXT_COLOR, font=load_font(FONT_SIZES["name"]))
        draw.text(COORDINATES["rg"], f"RG: {rg}", 
                 fill=TEXT_COLOR, font=load_font(FONT_SIZES["data"]))
        draw.text(COORDINATES["cpf"], f"CPF: {cpf}", 
                 fill=TEXT_COLOR, font=load_font(FONT_SIZES["data"]))

        # Add photo if provided
        if photo_path:
            photo = Image.open(photo_path).convert("RGB")
            photo.thumbnail(COORDINATES["photo_size"])  # Maintain aspect ratio
            template.paste(photo, COORDINATES["photo"])

        # Save to temporary file
        output_path = f"cracha_{name.replace(' ', '_')}.png"
        template.save(output_path)
        return output_path

    except Exception as e:
        st.error(f"Error generating badge: {str(e)}")
        return None

# Streamlit UI
def main():
    st.title("Gerador de Crachás Profissional")
    
    with st.form("badge_form"):
        name = st.text_input("Nome completo:", max_chars=50)
        rg = st.text_input("RG:", max_chars=15)
        cpf = st.text_input("CPF:", max_chars=14)
        photo = st.file_uploader("Foto (opcional):", 
                                type=["jpg", "jpeg", "png"],
                                accept_multiple_files=False)
        
        if st.form_submit_button("Gerar Crachá"):
            if not all([name, rg, cpf]):
                st.error("Preencha todos os campos obrigatórios!")
                return
                
            photo_path = process_photo(photo)
            output_path = generate_badge(name, rg, cpf, photo_path)
            
            if output_path and Path(output_path).exists():
                st.success("Crachá gerado com sucesso!")
                st.image(output_path)
                st.download_button("Baixar Crachá", 
                                  open(output_path, "rb").read(),
                                  file_name=output_path,
                                  mime="image/png")

if __name__ == "__main__":
    main()
