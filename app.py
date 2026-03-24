from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Configuração Avançada do PDF Profissional
class ComprovanteProfissional(FPDF):
    def header(self):
        # 1. Borda de Segurança Estilizada
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.5)
        self.rect(8.0, 8.0, 194.0, 281.0)
        
        # 2. Logo da Instituição (Canto Esquerdo)
        logo_path = os.path.join('static', 'img', 'logo_instituicao.png')
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=14, w=35)

        # 3. TÍTULO "FODA" (Hierarquia Visual Premium)
        self.set_y(17) # Ajuste fino da altura
        
        # --- Linha 1: Sobretítulo espaçado (Ar de documento de segurança) ---
        self.set_x(55)
        self.set_font('helvetica', 'B', 9)
        self.set_text_color(120, 130, 140) # Cinza elegante
        self.cell(140, 6, 'D O C U M E N T O   O F I C I A L   D E   R E G I S T R O', align='C', new_x='LMARGIN', new_y='NEXT')
        
        # --- Linha 2: O Título Principal Imponente ---
        self.set_x(55)
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(10, 25, 45) # Azul acinzentado bem escuro (executivo)
        self.cell(140, 12, 'COMPROVANTE DE MATRÍCULA', align='C', new_x='LMARGIN', new_y='NEXT')
        
        # 4. Linha separadora dupla (Travada abaixo de tudo)
        self.set_y(40) 
        self.set_draw_color(10, 30, 70)
        self.set_line_width(1.0)
        self.line(15, 40, 195, 40)
        self.set_line_width(0.3)
        self.line(15, 42, 195, 42)
        self.ln(10)

    def footer(self):
        # Rodapé com rastreabilidade
        self.set_y(-25)
        self.set_draw_color(200, 200, 200)
        # CORREÇÃO AQUI: Use 'self' em vez de 'pdf'
        self.line(15, self.get_y(), 195, self.get_y())
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        data_hora = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        self.cell(0, 10, f'Documento gerado pelo Portal de Matrícula Inteligente (PMI) | Autenticidade: {data_hora} | Cód: VALID-ENGCMP-2026', align='C')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    # Coleta e higienização dos dados
    nome = request.form.get('nome', '').upper().strip()
    instituicao = request.form.get('instituicao', '').upper().strip()
    tipo = request.form.get('tipo')
    
    # Validação Básica
    if not nome or not instituicao:
        return "Erro: Nome e Instituição são obrigatórios."

    # Inicializa PDF
    pdf = ComprovanteProfissional(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # --- Corpo do Documento ---
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    
    # Usando MultiCell para formatação mais limpa
    txt_intro = f"A instituição {instituicao}, devidamente credenciada, certifica para os devidos fins que o(a) aluno(a) abaixo identificado(a) possui vínculo ativo para o período letivo vigente."
    pdf.multi_cell(0, 7, txt_intro, align='J')
    pdf.ln(10)

    # Bloco DADOS DO ALUNO
    pdf.set_fill_color(240, 240, 240) # Fundo cinza suave para cabeçalho
    pdf.set_font('helvetica', 'B', 13)
    pdf.cell(0, 10, ' 1. DADOS DO ALUNO', border='L', fill=True, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)
    
    pdf.set_font('helvetica', '', 11)
    pdf.cell(50, 8, 'Nome Completo:', border='B')
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, f' {nome}', border='B', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('helvetica', '', 11)
    pdf.cell(50, 8, 'Tipo de Ensino:', border='B')
    pdf.set_font('helvetica', 'B', 11)
    tipo_str = 'UNIVERSITÁRIO' if tipo == 'universidade' else 'CURSO TÉCNICO'
    pdf.cell(0, 8, f' {tipo_str}', border='B', new_x='LMARGIN', new_y='NEXT')
    # Campos Condicionais (com layout alinhado)
    if tipo == 'escola':
        escolaridade = request.form.get('escolaridade', '').upper()
        pdf.set_font('helvetica', '', 11)
        pdf.cell(50, 8, 'Escolaridade/Série:', border='B')
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, f' {escolaridade}', border='B', new_x='LMARGIN', new_y='NEXT')
    elif tipo == 'universidade':
        curso = request.form.get('curso', '').upper()
        periodo = request.form.get('periodo', '').upper()
        
        pdf.set_font('helvetica', '', 11)
        pdf.cell(50, 8, 'Curso:', border='B')
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, f' {curso}', border='B', new_x='LMARGIN', new_y='NEXT')
        
        pdf.set_font('helvetica', '', 11)
        pdf.cell(50, 8, 'Período/Semestre:', border='B')
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, f' {periodo}', border='B', new_x='LMARGIN', new_y='NEXT')

    # Bloco STATUS
    pdf.ln(10)
    pdf.set_fill_color(220, 240, 220) # Fundo verde suave
    pdf.set_font('helvetica', 'B', 13)
    pdf.cell(0, 10, ' 2. SITUAÇÃO DA MATRÍCULA', border='L', fill=True, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)
    
    # Criando um bloco sólido (badge) para o status, muito mais profissional
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(255, 255, 255) # Texto Branco
    pdf.set_fill_color(0, 100, 40) # Fundo Verde Escuro Oficial
    
    # O parâmetro fill=True preenche o fundo da célula com a cor acima
    pdf.cell(0, 12, ' MATRÍCULA REGULAR E ATIVA ', align='C', fill=True, new_x='LMARGIN', new_y='NEXT')

    # --- O CARIMBO REALISTA (Posição Absoluta) ---
    carimbo_path = os.path.join('static', 'img', 'carimbo_oficial.png')
    
    if os.path.exists(carimbo_path):
        # x=67.5 centraliza uma imagem de w=75. 
        # y=200 trava a altura do carimbo perto do rodapé, para nunca ser cortado.
        pdf.image(carimbo_path, x=67.5, y=200, w=75)
    else:
        pdf.ln(20)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, '[ERRO: IMAGEM DO CARIMBO NÃO ENCONTRADA]', align='C')

    # Salvando e enviando
    pdf_path = f"comprovante_{nome.replace(' ', '_')}.pdf"
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)