from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ── dados institucionais ──────────────────────────────────────────────────────
NOTICIAS = [
    {
        "id": 1,
        "titulo": "Alunos conquistam 1º lugar na Mostra de Educação Profissional",
        "data": "2024-11-15",
        "categoria": "Prêmios",
        "resumo": "Quatro primeiros lugares na etapa regional da MEP colocam a Pedro Meinerz no topo do RS.",
        "icone": "🏆"
    },
    {
        "id": 2,
        "titulo": "Prótese em fibra de carbono premiada na Escócia",
        "data": "2024-09-10",
        "categoria": "Inovação",
        "resumo": "Projeto desenvolvido por alunos do Técnico em Mecânica é reconhecido no Edinburgh International Science Festival.",
        "icone": "🌍"
    },
    {
        "id": 3,
        "titulo": "Projeto Papo de Responsa chega à escola",
        "data": "2024-08-22",
        "categoria": "Social",
        "resumo": "Polícia Civil do RS realiza ação de prevenção às drogas e violência com os estudantes.",
        "icone": "🤝"
    },
    {
        "id": 4,
        "titulo": "Semana da Sustentabilidade 2024",
        "data": "2024-06-05",
        "categoria": "Meio Ambiente",
        "resumo": "Ações de separação de resíduos, reaproveitamento de materiais e preservação da área verde.",
        "icone": "🌱"
    },
    {
        "id": 5,
        "titulo": "Laboratório de Informática renovado",
        "data": "2024-04-18",
        "categoria": "Estrutura",
        "resumo": "Novos computadores e internet de alta velocidade melhoram o aprendizado digital dos alunos.",
        "icone": "💻"
    },
    {
        "id": 6,
        "titulo": "Inscrições abertas para o Técnico em Mecânica 2025",
        "data": "2024-12-01",
        "categoria": "Cursos",
        "resumo": "Vagas limitadas para o curso técnico mais renomado da região noroeste do RS.",
        "icone": "📋"
    },
]

CURSOS = [
    {
        "nome": "Ensino Fundamental",
        "nivel": "Fundamental",
        "carga_horaria": "800h/ano",
        "publico": "Crianças e adolescentes de 6 a 14 anos",
        "descricao": "Formação básica sólida com foco em habilidades essenciais, pensamento crítico e preparação para o Ensino Médio.",
        "conteudo": ["Português e Literatura", "Matemática", "Ciências", "História", "Geografia", "Arte", "Educação Física"],
        "certificacao": "Certificado de Conclusão do Ensino Fundamental",
        "turnos": "Diurno",
        "icone": "📖"
    },
    {
        "nome": "Ensino Médio",
        "nivel": "Médio",
        "carga_horaria": "2.400h (3 anos)",
        "publico": "Jovens de 14 a 18 anos",
        "descricao": "Formação completa para o mercado de trabalho e vestibulares, com ênfase em ciências exatas e tecnologia.",
        "conteudo": ["Matemática Avançada", "Física", "Química", "Biologia", "Português e Redação", "Inglês", "Filosofia", "Sociologia"],
        "certificacao": "Diploma de Ensino Médio — SEDUC/RS",
        "turnos": "Diurno e Noturno",
        "icone": "🎓"
    },
    {
        "nome": "Técnico em Mecânica",
        "nivel": "Técnico",
        "carga_horaria": "1.200h",
        "publico": "Jovens e adultos a partir de 16 anos (concomitante ou subsequente)",
        "descricao": "Curso técnico de excelência reconhecido internacionalmente. Forma profissionais capacitados para atuar na indústria metalmecânica com projetos reais e premiados.",
        "conteudo": [
            "Desenho Técnico e CAD",
            "Resistência dos Materiais",
            "Processos de Fabricação",
            "Metrologia e Controle de Qualidade",
            "Manutenção Industrial",
            "Eletricidade Aplicada",
            "Segurança do Trabalho",
            "Projetos de Inovação"
        ],
        "certificacao": "Diploma de Técnico em Mecânica — MEC/SEDUC",
        "turnos": "Diurno e Noturno",
        "icone": "⚙️",
        "destaque": True
    },
]

DOCENTES = [
    {
        "nome": "Coordenação Pedagógica",
        "cargo": "Equipe Diretiva",
        "formacao": "Pedagogia e Gestão Escolar",
        "experiencia": "Gestão e coordenação do processo educativo da instituição",
        "icone": "👩‍💼"
    },
    {
        "nome": "Corpo Docente — Ciências Exatas",
        "cargo": "Professores de Matemática, Física e Química",
        "formacao": "Licenciaturas nas respectivas áreas — UFSM, UNIJUÍ, URI",
        "experiencia": "Ensino de ciências exatas com metodologia ativa e laboratórios práticos",
        "icone": "🔬"
    },
    {
        "nome": "Instrutores Técnicos — Mecânica",
        "cargo": "Professores do Curso Técnico",
        "formacao": "Engenharia Mecânica, Mecatrônica e áreas correlatas",
        "experiencia": "Profissionais com vivência industrial e acadêmica, orientadores de projetos premiados internacionalmente",
        "icone": "⚙️"
    },
    {
        "nome": "Corpo Docente — Humanas",
        "cargo": "Professores de Português, História e Filosofia",
        "formacao": "Licenciaturas em Letras, História, Filosofia e Sociologia",
        "experiencia": "Formação crítica e humanista para os estudantes da instituição",
        "icone": "📚"
    },
]

PARCEIROS = [
    {"nome": "SEDUC/RS", "tipo": "Governo", "descricao": "Secretaria de Educação do Estado do Rio Grande do Sul", "icone": "🏛️"},
    {"nome": "17ª CRE", "tipo": "Regional", "descricao": "17ª Coordenadoria Regional de Educação — Santa Rosa", "icone": "📋"},
    {"nome": "SENAI", "tipo": "Técnico", "descricao": "Parceria para formação técnica e certificações industriais", "icone": "🏭"},
    {"nome": "Prefeitura de Santa Rosa", "tipo": "Municipal", "descricao": "Apoio municipal a projetos educacionais e culturais", "icone": "🏙️"},
    {"nome": "Indústrias Regionais", "tipo": "Empresa", "descricao": "Empresas parceiras para estágios e projetos aplicados", "icone": "🔧"},
    {"nome": "UFSM / UNIJUÍ", "tipo": "Acadêmico", "descricao": "Universidades parceiras para extensão e pesquisa", "icone": "🎓"},
]

# ── rotas ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
                           noticias=NOTICIAS[:3],
                           cursos=CURSOS,
                           docentes=DOCENTES,
                           parceiros=PARCEIROS)

@app.route("/api/noticias")
def api_noticias():
    return jsonify(NOTICIAS)

@app.route("/api/cursos")
def api_cursos():
    return jsonify(CURSOS)

@app.route("/api/contato", methods=["POST"])
def api_contato():
    data = request.json
    # Em produção: enviar e-mail, salvar no banco, etc.
    print(f"[{datetime.now()}] Contato recebido: {data.get('nome')} — {data.get('assunto')}")
    return jsonify({"status": "ok", "mensagem": "Mensagem recebida! Entraremos em contato em breve."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)