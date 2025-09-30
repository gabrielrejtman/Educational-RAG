from fpdf import FPDF
import os

def create_pdf_from_text(text_content: str, filename: str = "documento_gerado.pdf", title: str = "Documento Gerado"):
    pdf = FPDF()
    pdf.add_page()
    
    # Adiciona o título
    pdf.set_font("Arial", 'B', size=16)
    # Garante que a célula é centralizada e move o cursor para baixo
    pdf.multi_cell(0, 10, title, align='C')
    pdf.ln(10)

    # Adiciona o conteúdo
    pdf.set_font("Arial", size=12)
    
    # Divide o texto em blocos (parágrafos)
    paragraphs = [p.strip() for p in text_content.split('\n\n') if p.strip()]

    for paragraph in paragraphs:
        # Transforma o parágrafo em Latin-1 para evitar problemas de codificação
        safe_paragraph = paragraph.encode('latin-1', 'replace').decode('latin-1')
        
        # Usa multi_cell para quebrar o texto se for muito longo
        # w=0 (largura total restante), h=8 (altura da linha), txt=conteúdo
        pdf.multi_cell(w=0, h=8, text=safe_paragraph)
        
        # Adiciona uma linha em branco para espaçamento entre parágrafos
        pdf.ln(4)

    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    pdf.output(output_path)
    return output_path