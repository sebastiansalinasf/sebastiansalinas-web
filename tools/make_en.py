"""Genera landing/en/index.html a partir de landing/index.html (español)."""
import re, json, os

import pathlib
_REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = str(_REPO / 'site' / 'index.html')
OUT = str(_REPO / 'site' / 'en' / 'index.html')
BASE = 'https://www.sebastiansalinas.cl/'

T = {
 # ---- head ----
 '<html lang="es-CL">': '<html lang="en">',
 'Sebastián Salinas Fuenzalida · Abogado, MBA y CEO de Dunora': 'Sebastián Salinas Fuenzalida · Lawyer, MBA and CEO of Dunora',
 'Sebastián Salinas Fuenzalida, abogado chileno: socio fundador de Salinas &amp; Cía. Abogados, Director Ejecutivo de REGIS y cofundador y CEO de Dunora (LegalTech).':
   'Sebastián Salinas Fuenzalida, Chilean lawyer: founding partner of Salinas &amp; Cía. Abogados, Executive Director of REGIS and co-founder and CEO of Dunora (LegalTech).',
 'Sebastián Salinas Fuenzalida · Abogado, MBA y fundador LegalTech': 'Sebastián Salinas Fuenzalida · Lawyer, MBA and LegalTech founder',
 'Abogado de empresa desde 2011, socio de Salinas & Cía. Abogados, cofundador de Dunora y velerista de competición.':
   'Business lawyer since 2011, partner at Salinas & Cía. Abogados, co-founder of Dunora and competitive sailor.',
 'Abogado de empresa desde 2011, socio de Salinas &amp; Cía. Abogados, Director Ejecutivo de REGIS y cofundador de Dunora.':
   'Business lawyer since 2011, partner at Salinas &amp; Cía. Abogados, Executive Director of REGIS and co-founder of Dunora.',
 '<link rel="canonical" href="https://www.sebastiansalinas.cl/" />': '<link rel="canonical" href="https://www.sebastiansalinas.cl/en/" />',
 '<meta property="og:url" content="https://www.sebastiansalinas.cl/" />': '<meta property="og:url" content="https://www.sebastiansalinas.cl/en/" />',
 '<meta property="og:locale" content="es_CL" />\n  <meta property="og:locale:alternate" content="en_US" />':
   '<meta property="og:locale" content="en_US" />\n  <meta property="og:locale:alternate" content="es_CL" />',
 'Sebastián Salinas Fuenzalida, abogado y cofundador de Dunora': 'Sebastián Salinas Fuenzalida, lawyer and co-founder of Dunora',
 'Resumen para modelos de IA': 'Summary for AI models',
 'href="assets/': 'href="../assets/', 'src="assets/': 'src="../assets/',
 # ---- nav ----
 'aria-label="Principal"': 'aria-label="Main"',
 '<span class="text-white" aria-current="true">ES</span> <span aria-hidden="true">/</span> <a href="en/" hreflang="en" lang="en" class="hover:text-copper-300">EN</a>':
   '<a href="../" hreflang="es" lang="es" class="hover:text-copper-300">ES</a> <span aria-hidden="true">/</span> <span class="text-white" aria-current="true">EN</span>',
 '>Perfil<': '>Profile<', '>Trayectoria<': '>Career<', '>Formación<': '>Education<', '>Vela<': '>Sailing<', '>Contacto<': '>Contact<',
 # ---- hero ----
 'Abogado · Empresario · Fundador LegalTech': 'Lawyer · Entrepreneur · LegalTech Founder',
 'Más de 15 años integrando el rigor jurídico con la visión de negocios. Socio fundador de': 'Over 15 years combining legal rigor with business vision. Founding partner of',
 ', Director Ejecutivo de\n': ', Executive Director of\n',
 ' y cofundador y CEO de\n': ' and co-founder and CEO of\n',
 ', el sistema operativo legal para Latinoamérica.': ', the legal operating system for Latin America.',
 '>Conversemos<': '>Let’s talk<',
 'Retrato de Sebastián Salinas Fuenzalida, abogado y cofundador de Dunora': 'Portrait of Sebastián Salinas Fuenzalida, lawyer and co-founder of Dunora',
 '>Abogado desde<': '>Lawyer since<', '>Postgrados<': '>Graduate degrees<', '>MBA + Máster<': '>3 Master’s<',
 '>Martillero Público<': '>Public Auctioneer<', '>N.º 1759<': '>No. 1759<',
 # ---- perfil ----
 'Derecho, empresa y negocios en una sola mirada': 'Law, business and strategy through a single lens',
 'Sebastián Salinas Fuenzalida, abogado de empresa, MBA': 'Sebastián Salinas Fuenzalida, business lawyer, MBA',
 ' es abogado chileno, investido por la Corte Suprema el 26 de agosto de 2011. Se especializa en la intersección entre el derecho, la empresa y los negocios.':
   ' is a Chilean lawyer, admitted to the bar by the Supreme Court of Chile on 26 August 2011. He specializes in the intersection of law, companies and business.',
 'Asesora a empresas, empresarios, empresas familiares y personas en estructuración y reorganización societaria, gobierno corporativo, negociación, contratación y resolución de conflictos. También dirige asuntos civiles, inmobiliarios y de familia, incluida la litigación estratégica. Ha participado en directorios y en la organización de empresas de minería, construcción, medios e inmobiliario.':
   'He advises companies, business owners, family businesses and individuals on corporate structuring and restructuring, corporate governance, negotiation, contracts and dispute resolution. He also leads civil, real estate and family matters, including strategic litigation. He has served on boards and helped organize companies in mining, construction, media and real estate.',
 'Su formación combina un Máster en Derecho de la Empresa con un MBA y estudios en negocios internacionales y derecho inmobiliario. Así aborda cada desafío más allá de lo estrictamente legal, considerando también los objetivos comerciales, los riesgos y la sostenibilidad de cada organización.':
   'His education combines a Master’s in Business Law with an MBA and studies in international business and real estate law. This lets him approach each challenge beyond the strictly legal, also weighing each organization’s commercial goals, risks and sustainability.',
 '>Derecho de la empresa<': '>Business law<', '>Gobierno corporativo<': '>Corporate governance<', '>Empresas familiares<': '>Family businesses<',
 '>Derecho inmobiliario<': '>Real estate law<', '>Embargos y remates<': '>Foreclosures and auctions<', '>Litigación estratégica<': '>Strategic litigation<',
 '>Familia<': '>Family law<', '>LegalTech e IA<': '>LegalTech and AI<',
 # ---- trayectoria ----
 'Cargos y responsabilidades': 'Roles and responsibilities',
 '2011 – presente · Vitacura, Santiago': '2011 – present · Vitacura, Santiago',
 'Socio fundador · Salinas &amp; Cía. Abogados': 'Founding partner · Salinas &amp; Cía. Abogados',
 'Dirige la estrategia y el desarrollo comercial de la firma, especializada en la asesoría integral a empresas, empresas familiares y personas. Su trabajo abarca derecho corporativo, contratación, gestión de riesgos legales, directorios y litigación estratégica.':
   'He leads the strategy and business development of the firm, which provides comprehensive legal advice to companies, family businesses and individuals. His work covers corporate law, contracts, legal risk management, boards and strategic litigation.',
 'Director Ejecutivo · Vitacura, Santiago': 'Executive Director · Vitacura, Santiago',
 'Estudio especializado en propiedades: embargos y remates, negociación con acreedores, estudios de títulos, compraventas, arriendos, herencias, regularizaciones y proyectos inmobiliarios.':
   'Law firm specialized in property: foreclosures and auctions, creditor negotiations, title reviews, sales, leases, inheritance, regularizations and real estate projects.',
 '2026 – presente · América Latina': '2026 – present · Latin America',
 'Cofundador y CEO · Dunora (LEXINNOVA SpA)': 'Co-founder and CEO · Dunora (LEXINNOVA SpA)',
 'Lidera la estrategia y el desarrollo de negocio de Dunora, una plataforma LegalTech que integra tecnología, inteligencia artificial y gestión jurídica para modernizar la operación de los estudios de abogados.':
   'He leads the strategy and business development of Dunora, a LegalTech platform that brings together technology, artificial intelligence and legal management to modernize how law firms operate.',
 '2017 – presente · Registro N.º 1759': '2017 – present · Registry No. 1759',
 'Inscrito en el Registro Nacional de Martilleros del Ministerio de Economía, Fomento y Turismo (Res. Ex. N.º 1204, 20/04/2017), según la Ley N.º 18.118. Gestiona y ejecuta remates voluntarios, en complemento de su práctica legal y patrimonial.':
   'Registered in Chile’s National Registry of Auctioneers of the Ministry of Economy, Development and Tourism (Exempt Resolution No. 1204, 20/04/2017), under Law No. 18,118. He manages and conducts voluntary auctions, complementing his legal and asset-management practice.',
 'Inscripción vigente · Registro de Martilleros, Ministerio de Economía ↗': 'Active registration · Registry of Auctioneers, Ministry of Economy ↗',
 # ---- dunora ----
 'Logotipo de Dunora': 'Dunora logo',
 'LegalTech · Inteligencia artificial': 'LegalTech · Artificial intelligence',
 'Dunora: el sistema operativo legal para Latinoamérica': 'Dunora: the legal operating system for Latin America',
 'Desde su experiencia dirigiendo un estudio jurídico desde 2011, Sebastián vio que sumar herramientas de IA aisladas a flujos fragmentados no resuelve el problema de fondo. Con Dunora construye la capa operativa que hace el trabajo legal estructurado, medible, trazable y listo para la IA. Comienza en Chile y proyecta su expansión a la región.':
   'Having run a law firm since 2011, Sebastián saw that adding isolated AI tools to fragmented workflows does not solve the underlying problem. With Dunora he is building the operating layer that makes legal work structured, measurable, traceable and AI-ready, starting in Chile with plans to expand across the region.',
 'Su mirada sobre la innovación también tiene raíces internacionales: durante su MBA visitó el CEEILleida, el Centro Europeo de Empresas e Innovación de Lleida (España), que integra la red europea EBN de incubadoras de empresas innovadoras.':
   'His view of innovation also has international roots: during his MBA he visited CEEILleida, the European Business and Innovation Centre of Lleida (Spain), part of the EBN European network of innovation-driven business incubators.',
 '>Ver nota<': '>See article<',
 'Conocer Dunora ↗': 'Discover Dunora ↗',
 'Sebastián Salinas Fuenzalida, cofundador y CEO de Dunora': 'Sebastián Salinas Fuenzalida, co-founder and CEO of Dunora',
 '>Gestión integral<': '>End-to-end management<', 'Clientes, causas, plazos, tareas y documentos en un solo flujo.': 'Clients, cases, deadlines, tasks and documents in a single workflow.',
 '>IA gobernada<': '>Governed AI<', 'Inteligencia artificial aplicada a documentos y asuntos reales, con permisos y supervisión.': 'Artificial intelligence applied to real documents and matters, with permissions and oversight.',
 '>Honorarios y cobranza<': '>Billing and collections<', 'Del asunto al cobro: visibilidad operacional del estudio.': 'From matter to cash: operational visibility for the firm.',
 '>Trazabilidad<': '>Traceability<', 'Evidencias, auditoría y control de acceso desde el diseño.': 'Evidence, audit trails and access control by design.',
 # ---- formación ----
 'Formación académica': 'Education', 'Postgrados y certificaciones': 'Degrees and certifications',
 '>Licenciado en Ciencias Jurídicas y Sociales<': '>Bachelor of Laws (Licenciado en Ciencias Jurídicas y Sociales)<',
 '>Título de Abogado<': '>Law degree and admission to the bar<', 'Excma. Corte Suprema de Chile · Colegio de Abogados de Chile': 'Supreme Court of Chile · Chilean Bar Association',
 '>Máster en Derecho de la Empresa<': '>Master’s in Business Law (Máster en Derecho de la Empresa)<',
 '>Magíster en Dirección General de Empresas – MBA Executive<': '>Executive MBA – Master’s in General Management<',
 '>Máster en Dirección General de Empresas<': '>Master’s in General Management<',
 'Diplomado de Especialización en Entornos Globales y Dirección de Negocios Internacionales': 'Specialization Diploma in Global Environments and International Business Management',
 '>Diplomado en Derecho Inmobiliario de la Empresa<': '>Diploma in Corporate Real Estate Law<',
 '>Nuevas Tendencias en Materia de Arbitraje<': '>New Trends in Arbitration<',
 '>El Derecho del Trabajo frente al COVID-19<': '>Labor Law and COVID-19<',
 '>Planificación y Ordenamiento Territorial<': '>Land-Use and Territorial Planning<',
 'CEPAL · Comisión Económica para América Latina y el Caribe': 'ECLAC · UN Economic Commission for Latin America and the Caribbean',
 '>Bachillerato en Servicio Público<': '>Public Service Program (Bachillerato en Servicio Público)<',
 'Universitat de Lleida (España)': 'Universitat de Lleida (Spain)',
 'Facultad de Derecho, Universidad de los Andes': 'School of Law, Universidad de los Andes',
 # ---- publicaciones ----
 'Enriquecimiento sin causa en los cuasicontratos. El concubinato: evolución y tendencias jurisprudenciales</h3>': 'Enriquecimiento sin causa en los cuasicontratos. El concubinato: evolución y tendencias jurisprudenciales <span class="block mt-2 text-sm font-sans text-slate2-500">(Unjust enrichment in quasi-contracts. Cohabitation: evolution and case-law trends)</span></h3>',
 'Ver en PUCV ↗': 'View at PUCV ↗', 'Ver en Universidad Gabriela Mistral ↗': 'View at Universidad Gabriela Mistral ↗',
 'Publicado por la Universidad Gabriela Mistral y la Pontificia Universidad Católica de Valparaíso.': 'Published by Universidad Gabriela Mistral and Pontificia Universidad Católica de Valparaíso (PUCV).',
 'Guía práctica · 2021': 'Practical guide · 2021',
 'Guía para la constitución de personas jurídicas sin fines de lucro</h3>': 'Guide to setting up non-profit legal entities</h3>',
 'Elaborada para el Colegio de Kinesiólogos de Chile y publicada en su sitio para las sociedades científicas.': 'Written for the Chilean College of Kinesiologists and published on its website for scientific societies.',
 'Ver guía (PDF) ↗': 'View guide (PDF) ↗',
 'Publicaciones y litigación': 'Publications and litigation', 'Pensamiento jurídico': 'Legal thinking',
 'El enriquecimiento injusto en los cuasicontratos; el concubinato, evolución y tendencias jurisprudenciales':
   'El enriquecimiento injusto en los cuasicontratos; el concubinato, evolución y tendencias jurisprudenciales <span class="block mt-2 text-sm font-sans text-slate2-500">(Unjust enrichment in quasi-contracts; cohabitation, evolution and case-law trends)</span>',
 '>Guía práctica<': '>Practical guide<', '>Constitución de corporaciones y fundaciones<': '>Setting up non-profit corporations and foundations<',
 'Elaborada originalmente para el Colegio de Kinesiólogos de Chile.': 'Originally written for the Chilean College of Kinesiologists.',
 'El Conservador debe inscribir la compraventa si la precautoria se decretó después de pedir la inscripción':
   'The Property Registrar must record a sale if the injunction was ordered after registration was requested',
 'Sebastián Salinas Fuenzalida patrocinó la causa y llevó adelante el juicio: un reclamo acogido contra la negativa del Conservador de Bienes Raíces de Pozo Almonte (Juzgado de Letras y Garantía de Pozo Almonte).':
   'Sebastián Salinas Fuenzalida was counsel of record and led the case: a successful challenge to the Pozo Almonte Property Registrar’s refusal to record a sale (Pozo Almonte Civil and Criminal Court). Article in Spanish.',
 'Leer en Diario Constitucional ↗': 'Read on Diario Constitucional ↗',
 # ---- vela ----
 'aria-label="Membresía ISCYRA"': 'aria-label="ISCYRA membership"', '>Miembro de la Clase Star<': '>Star Class member<',
 'Socio registrado de la International Star Class Yacht Racing Association (ISCYRA) · N.º 6870 · Flota Valparaíso, Distrito 18 (Chile).': 'Registered member of the International Star Class Yacht Racing Association (ISCYRA) · No. 6870 · Valparaíso Fleet, District 18 (Chile).',
 'Verificar membresía ↗': 'Verify membership ↗',
 'Más allá del derecho · Vela de competición': 'Beyond the law · Competitive sailing',
 'Representación internacional y espíritu competitivo:': 'International representation and competitive spirit:',
 '>Clase Star<': '>Star Class<',
 'En noviembre de 2019, Sebastián Salinas Fuenzalida llevó el pabellón chileno al Río de la Plata. Como proel de la vela': 'In November 2019, Sebastián Salinas Fuenzalida carried the Chilean flag to the Río de la Plata. As crew of sail',
 ', junto al timonel': ', alongside skipper',
 ', integró la única tripulación de Chile en el Campeonato Sudamericano de la Clase Star, disputado en el Club Náutico Olivos, Buenos Aires.':
   ', he was part of Chile’s only team at the Star Class South American Championship, held at Club Náutico Olivos, Buenos Aires.',
 'La Star es una embarcación olímpica histórica de quilla fija. Exige lectura táctica del viento, resistencia física y una coordinación milimétrica entre timonel y proel. Es la misma disciplina que se necesita en una negociación compleja: decidir rápido, con información incompleta y en equipo.':
   'The Star is a historic Olympic keelboat. It demands tactical reading of the wind, physical endurance and split-second coordination between skipper and crew: the same discipline a complex negotiation requires — deciding fast, with incomplete information, as a team.',
 'Sebastián Salinas Fuenzalida y Jorge Montero navegando la embarcación Star N.º 20 en el Campeonato Sudamericano 2019, Club Náutico Olivos, Río de la Plata':
   'Sebastián Salinas Fuenzalida and Jorge Montero sailing Star boat No. 20 at the 2019 South American Championship, Club Náutico Olivos, Río de la Plata',
 'Sudamericano Clase Star 2019 · Río de la Plata': 'Star Class South American Championship 2019 · Río de la Plata',
 'Foto: Jorge Cousillas / El Ojo Náutico': 'Photo: Jorge Cousillas / El Ojo Náutico',
 '>Único equipo chileno<': '>Only Chilean team<', 'La sola embarcación que representó a Chile en la regata.': 'The only boat representing Chile in the regatta.',
 '>7 países<': '>7 countries<', '>Flota internacional de 21 embarcaciones<': '>International fleet of 21 boats<',
 'Argentina, Brasil, Chile, Alemania, Estados Unidos, Italia y Uruguay.': 'Argentina, Brazil, Chile, Germany, the United States, Italy and Uruguay.',
 '>Club Náutico Olivos · Sudamericano Clase Star<': '>Club Náutico Olivos · Star South American Championship<',
 'Del 14 al 18 de noviembre, Río de la Plata, Buenos Aires.': '14–18 November, Río de la Plata, Buenos Aires.',
 '>Trayectoria náutica<': '>Sailing record<',
 '2019 · Representación internacional': '2019 · International representation',
 'Campeonato Sudamericano Clase Star · Club Náutico Olivos, Argentina': 'Star Class South American Championship · Club Náutico Olivos, Argentina',
 'Proel de la vela CHI 8502 junto al timonel Jorge Montero, la única embarcación chilena de la flota.': 'Crew of sail CHI 8502 with skipper Jorge Montero, the only Chilean boat in the fleet.',
 '2023 · 1.<sup>er</sup> lugar, categoría Cruceros': '2023 · 1<sup>st</sup> place, Cruiser category',
 'Tripulante del velero <em>Riday</em>, ganador de su categoría en la vigésima edición de esta regata tradicional, organizada junto a la Reserva Naval Yates de la Armada de Chile.':
   'Crew member of the yacht <em>Riday</em>, winner of its category in the 20th edition of this traditional regatta, organized with the Chilean Navy’s Yacht Naval Reserve.',
 'Medalla de 1.er lugar de la XX Regata Arbotante, 2023': 'First-place medal, XX Regata Arbotante, 2023',
 'Ver en Instagram ↗': 'View on Instagram ↗',
 'aria-label="Registro oficial"': 'aria-label="Official record"', '>Registro oficial<': '>Official record<',
 'Archivo del Campeonato Sudamericano Star 2019 · International Star Class Yacht Racing Association (ISCYRA).': '2019 Star South American Championship archive · International Star Class Yacht Racing Association (ISCYRA).',
 'Archivo oficial 2019 ↗': 'Official 2019 archive ↗',
 # ---- blog ----
 '>Blog · Comentarios<': '>Blog · Commentary<',
 '>Derecho, empresa y mercado inmobiliario<': '>Law, business and real estate<',
 'Comentarios de Sebastián Salinas Fuenzalida sobre noticias de negocios, el mercado inmobiliario y fallos judiciales con impacto para empresas y personas.': 'Commentary by Sebastián Salinas Fuenzalida on business news, the real estate market and court rulings that matter to companies and individuals (articles in Spanish).',
 '>Primeros comentarios, muy pronto<': '>First articles coming soon<',
 'Análisis breves sobre actualidad empresarial, mercado inmobiliario y fallos judiciales relevantes para empresas y personas. Nuevas publicaciones dos veces por semana.': 'Short analyses of business news, the real estate market and relevant court rulings. New articles twice a week (in Spanish).',
 'Ver todos los comentarios →': 'See all articles (Spanish) →', 'Leer comentario →': 'Read article (Spanish) →',
 'href="blog/': 'href="../blog/',
 '>Blog<': '>Blog<',
 # ---- faq / contacto ----
 '>Preguntas frecuentes<': '>Frequently asked questions<', 'Sobre Sebastián Salinas Fuenzalida': 'About Sebastián Salinas Fuenzalida',
 'Conversemos sobre su próximo desafío': 'Let’s talk about your next challenge',
 'aria-label="Cuenta verificada"': 'aria-label="Verified account"',
 '© 2026 Sebastián Salinas Fuenzalida · Abogado · Santiago, Chile · Última actualización: noviembre de 2026': '© 2026 Sebastián Salinas Fuenzalida · Lawyer · Santiago, Chile · Last updated: November 2026',
}

FAQ_EN = [
 ("Who is Sebastián Salinas Fuenzalida?",
  "Sebastián Salinas Fuenzalida is a Chilean lawyer, admitted to the bar by the Supreme Court of Chile on 26 August 2011. He is the founding partner of Salinas & Cía. Abogados, Executive Director of REGIS Abogados Inmobiliarios, co-founder and CEO of Dunora (LegalTech) and a registered Public Auctioneer (No. 1759). He holds a Bachelor of Laws from Universidad Gabriela Mistral, a Master’s in Business Law (Universidad de los Andes) and an Executive MBA (Universidad Gabriela Mistral / Universitat de Lleida)."),
 ("What is Dunora and what is Sebastián Salinas’s role?",
  "Dunora is a legal operating system for law firms in Latin America, developed by LEXINNOVA SpA. It brings clients, cases, deadlines, documents, billing and governed artificial intelligence together in a single workflow. Sebastián Salinas Fuenzalida has been its co-founder and CEO since 2026."),
 ("What areas of law does Sebastián Salinas practice?",
  "Corporate and business law, corporate governance and family businesses, real estate law (including foreclosures and auctions), contracts and negotiation, strategic civil litigation and family law."),
 ("Does Sebastián Salinas Fuenzalida sail competitively?",
  "Yes. In 2019 he represented Chile as crew of sail CHI 8502, alongside skipper Jorge Montero, at the Star Class South American Championship at Club Náutico Olivos (Argentina). In 2023 he won first place in the Cruiser category of the XX Regata Arbotantes in Algarrobo, Chile, as a crew member of the yacht Riday."),
 ("How can I contact Sebastián Salinas Fuenzalida?",
  "By email at ssalinas@salinasycia.cl or via LinkedIn: linkedin.com/in/sebastian-salinas-fuenzalida."),
]

def build():
    h = open(SRC, encoding='utf-8').read()
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', h, re.S)
    ld = json.loads(m.group(2))
    g = ld['@graph']
    prof = next(x for x in g if x['@type'] == 'ProfilePage')
    prof.update({'@id': BASE + 'en/#profile', 'url': BASE + 'en/', 'inLanguage': 'en'})
    per = next(x for x in g if x['@type'] == 'Person')
    per['description'] = ("Chilean lawyer admitted to the bar by the Supreme Court of Chile in 2011, specializing in business law, corporate governance, "
        "real estate law and strategic litigation. Founding partner of Salinas & Cía. Abogados, Executive Director of REGIS Abogados Inmobiliarios, "
        "co-founder and CEO of Dunora (LegalTech by LEXINNOVA SpA) and registered Public Auctioneer No. 1759.")
    per['jobTitle'] = ["Lawyer", "Founding Partner, Salinas & Cía. Abogados", "Co-founder and CEO, Dunora",
                       "Executive Director, REGIS Abogados Inmobiliarios", "Public Auctioneer"]
    per['knowsAbout'] = ["Business law", "Corporate governance", "Family businesses", "Real estate law", "Foreclosures and auctions",
                         "Civil litigation", "Family law", "Arbitration", "LegalTech", "Artificial intelligence in law", "Auctions", "Competitive sailing"]
    per['knowsLanguage'] = ["es", "en"]
    for mo in per.get('memberOf', []):
        if 'ISCYRA' in mo.get('name',''): mo['description'] = "Registered member No. 6870, Valparaíso Fleet, District 18 (Chile)"
        if mo.get('name') == 'Colegio de Abogados de Chile': mo['alternateName'] = 'Chilean Bar Association'
    per['award'] = ["1st place, Cruiser category, XX Regata Arbotantes (Cofradía Náutica del Pacífico, Algarrobo, Chile, 2023), crew of the yacht Riday",
                    "Represented Chile (sail CHI 8502) at the 2019 Star Class South American Championship, Club Náutico Olivos, Argentina"]
    faq = next(x for x in g if x['@type'] == 'FAQPage')
    faq['@id'] = BASE + 'en/#faq'
    faq['mainEntity'] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_EN]
    new_ld = json.dumps(ld, ensure_ascii=False, indent=2)
    h = h[:m.start(2)] + '\n' + new_ld + '\n  ' + h[m.end(2):]
    h = h.replace('<!-- ===== Datos estructurados: la pieza clave para buscadores y asistentes de IA ===== -->', '<!-- Structured data -->')

    # visible FAQ from FAQ_EN
    s = h.index('    <div class="mt-10 divide-y divide-slate2-100 border-y border-slate2-100">')
    e = h.index('    </div>\n  </div>\n</section>', s)
    items = [f'      <details class="group py-5"{" open" if i == 0 else ""}><summary class="cursor-pointer list-none font-serif text-xl">{q}</summary>'
             f'<p class="mt-3 leading-relaxed text-navy-800">{a.replace("&", "&amp;")}</p></details>' for i, (q, a) in enumerate(FAQ_EN)]
    h = h[:s] + '    <div class="mt-10 divide-y divide-slate2-100 border-y border-slate2-100">\n' + '\n'.join(items) + '\n' + h[e:]

    # translate outside JSON-LD
    m = re.search(r'<script type="application/ld\+json">.*?</script>', h, re.S)
    head, ldblock, tail = h[:m.start()], m.group(0), h[m.end():]
    def tr(x):
        for k in sorted(T, key=len, reverse=True):
            x = x.replace(k, T[k])
        return x
    h = tr(head) + ldblock + tr(tail)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    build()
    print('ok')
