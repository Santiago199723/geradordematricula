from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from datetime import datetime
import os
import random  # Adicionado para gerar matrículas e nomes aleatórios

app = Flask(__name__)

# TRUQUE PARA O VERCEL (Define a pasta raiz do projeto para achar as imagens)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuração Avançada do PDF Profissional
class ComprovanteProfissional(FPDF):
    def header(self):
        # 1. Borda de Segurança Estilizada
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.5)
        self.rect(8.0, 8.0, 194.0, 281.0)
        
        # 2. Logo da Instituição (Dinâmica - usa a que o usuário mandou ou a padrão)
        # getattr pega a logo customizada, se não existir, usa a default.
        logo_path = getattr(self, 'custom_logo_path', os.path.join(BASE_DIR, 'static', 'img', 'logo_instituicao.png'))
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=14, w=35)

        # 3. TÍTULO "FODA" (Hierarquia Visual Premium)
        self.set_y(17) # Ajuste fino da altura
        
        # --- Linha 1: Sobretítulo espaçado (Ar de documento de segurança) ---
        self.set_x(55)
        self.set_font('helvetica', 'B', 8) # Letra um pouco menor para dar contraste
        self.set_text_color(140, 150, 160) # Cinza um pouco mais sutil
        self.cell(140, 6, 'R E G I S T R O   A C A D Ê M I C O   O F I C I A L', align='C', new_x='LMARGIN', new_y='NEXT')
        
        # --- Linha 2: O Título Principal Imponente ---
        self.set_x(55)
        self.set_font('helvetica', 'B', 21) # Tamanho 21 respira melhor na página (mais responsivo visualmente)
        self.set_text_color(0, 32, 96) # Um Azul Marinho profundo e super institucional
        self.cell(140, 12, 'CERTIFICADO DE VÍNCULO ACADÊMICO', align='C', new_x='LMARGIN', new_y='NEXT')
        
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
    nome = request.form.get('nome', '').upper().strip()
    instituicao = request.form.get('instituicao', '').upper().strip()
    tipo = request.form.get('tipo')
    
    if not nome or not instituicao:
        return "Erro: Nome e Instituição são obrigatórios."

    # --- GERADORES DE DADOS PROFISSIONAIS ---
    # Matrícula aleatória estilo faculdade federal (ex: 202610482-9)
    ano_atual = datetime.now().year
    matricula = f"{ano_atual}{random.randint(10000, 99999)}-{random.randint(1, 9)}"
    
    # Sorteando um nome de Diretor
    diretores = [
        "Dr. Santiago Carvalho Albuquerque", 
        "Profa. Dra. Marina Silva Ramos", 
        "Eng. Roberto Almeida Cunha", 
        "Dra. Fernanda Lins e Silva",
        "Prof. Me. Carlos Eduardo Fontes"
    ]
    diretor_sorteado = random.choice(diretores)

    # --- INICIALIZA PDF E LIDA COM ARQUIVOS UPLOADADOS ---
    pdf = ComprovanteProfissional(orientation="P", unit="mm", format="A4")
    
    # Pega os arquivos do formulário
    logo_file = request.files.get('logo')
    carimbo_file = request.files.get('carimbo')

    # Salva logo customizada no /tmp se existir
    if logo_file and logo_file.filename:
        logo_temp = os.path.join('/tmp', 'custom_logo.png')
        logo_file.save(logo_temp)
        pdf.custom_logo_path = logo_temp # Injeta na classe do FPDF
        
    # Define o path do carimbo (customizado ou padrão)
    carimbo_path = os.path.join(BASE_DIR, 'static', 'img', 'carimbo_oficial.png')
    if carimbo_file and carimbo_file.filename:
        carimbo_temp = os.path.join('/tmp', 'custom_carimbo.png')
        carimbo_file.save(carimbo_temp)
        carimbo_path = carimbo_temp

    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # --- Corpo do Documento ---
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    
    # Captura o nome do curso dependendo se o usuário escolheu Técnico ou Universidade
    if tipo == 'escola':
        nome_curso = request.form.get('escolaridade', 'NÃO INFORMADO').upper()
    else:
        nome_curso = request.form.get('curso', 'NÃO INFORMADO').upper()

    # TEXTO ALTAMENTE PROFISSIONAL COM DADOS DINÂMICOS (Agora com o Curso incluído!)
    txt_intro = (f"A diretoria acadêmica da instituição {instituicao}, devidamente credenciada e autorizada pelos "
                 f"órgãos competentes, certifica para os devidos fins de direito que o(a) acadêmico(a) "
                 f"{nome}, portador(a) da matrícula de registro interno Nº {matricula}, "
                 f"encontra-se regularmente matriculado(a) no curso de {nome_curso}, com seu vínculo "
                 f"institucional e obrigações acadêmicas ativas para o período letivo vigente.")
    
    # align='J' faz o texto ficar justificado (alinhado dos dois lados como num livro)
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
    # Campos Condicionais (com layout alinhado)
    if tipo == 'escola':
        escolaridade = request.form.get('escolaridade', '').upper()
        pdf.set_font('helvetica', '', 11)
        # Substituído 'Escolaridade/Série:' por 'Curso:'
        pdf.cell(50, 8, 'Curso:', border='B')
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

    # --- O CARIMBO REALISTA (Com posição recalculada) ---
    # A variável carimbo_path já foi definida lá em cima agora
    if os.path.exists(carimbo_path):
        # y=180 sobe um pouco o carimbo para caber a assinatura embaixo
        pdf.image(carimbo_path, x=67.5, y=180, w=75)
    else:
        pdf.set_y(190)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, '[ERRO: IMAGEM DO CARIMBO NÃO ENCONTRADA]', align='C')

    # --- ASSINATURA DO DIRETOR ---
    pdf.set_y(250) # Empurra o texto lá pro final da folha, abaixo da imagem
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, diretor_sorteado, align='C', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(100, 100, 100) # Cinza para subtítulo
    pdf.cell(0, 5, 'Diretor(a) Acadêmico(a) / Assinatura Oficial Eletrônica', align='C')

    # Salvando e enviando
    pdf_path = f"comprovante_{nome.replace(' ', '_')}.pdf"
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
