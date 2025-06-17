import re
import os
from collections import Counter

BANCO_DE_DOENCAS = {
    "influenza": {
        "categoria": "infecciosa",
        "descricao": "Doença respiratória viral aguda",
        "sintomas": ["febre", "tosse", "dor de garganta", "dores musculares"],
        "tratamentos": ["repouso", "hidratação", "antivirais", "analgésicos"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "gripe comum": {
        "categoria": "infecciosa",
        "descricao": "Infecção viral do sistema respiratório",
        "sintomas": ["febre", "coriza", "dor de cabeça", "fadiga"],
        "tratamentos": ["repouso", "hidratação", "analgésicos"],
        "profissional": ["O profissional recomendado é: clínico geral"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "covid 19": {
        "categoria": "infecciosa",
        "descricao": "Doença respiratória causada pelo coronavírus SARS-CoV-2",
        "sintomas": ["febre", "tosse seca", "cansaço", "perda de paladar ou olfato"],
        "tratamentos": ["isolamento", "medicação sintomática", "vacinação"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "tuberculose": {
        "categoria": "infecciosa",
        "descricao": "Doença bacteriana que afeta principalmente os pulmões",
        "sintomas": ["tosse persistente", "febre", "suor noturno", "perda de peso"],
        "tratamentos": ["antibióticos", "isolamento", "vacinação"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "pneumonia": {
        "categoria": "infecciosa",
        "descricao": "Infecção que inflama os sacos de ar nos pulmões",
        "sintomas": ["febre alta", "tosse com catarro", "dificuldade respiratória", "dor no peito"],
        "tratamentos": ["antibióticos", "repouso", "hidratação"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "dengue": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por mosquitos",
        "sintomas": ["febre alta", "dor muscular", "manchas na pele"],
        "tratamentos": ["hidratação", "repouso", "paracetamol"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "zika": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por mosquitos",
        "sintomas": ["febre leve", "erupções cutâneas", "conjuntivite", "dor nas articulações"],
        "tratamentos": ["repouso", "hidratação", "analgésicos"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "chikungunya": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por mosquitos",
        "sintomas": ["febre alta", "dor intensa nas articulações", "erupções cutâneas"],
        "tratamentos": ["repouso", "hidratação", "anti-inflamatórios"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hepatite a": {
        "categoria": "infecciosa",
        "descricao": "Inflamação do fígado causada pelo vírus da hepatite A",
        "sintomas": ["febre", "fadiga", "náusea", "icterícia"],
        "tratamentos": ["repouso", "dieta balanceada", "vacinação"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hepatite c": {
        "categoria": "infecciosa",
        "descricao": "Inflamação do fígado causada pelo vírus da hepatite C",
        "sintomas": ["fadiga", "dor abdominal", "icterícia", "urina escura"],
        "tratamentos": ["antivirais", "monitoramento", "transplante em casos graves"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "rubéola": {
        "categoria": "infecciosa",
        "descricao": "Doença viral contagiosa",
        "sintomas": ["febre leve", "erupções cutâneas", "gânglios inchados"],
        "tratamentos": ["repouso", "vacinação", "medicação sintomática"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "sarampo": {
        "categoria": "infecciosa",
        "descricao": "Doença viral altamente contagiosa",
        "sintomas": ["febre alta", "tosse", "coriza", "manchas brancas na boca"],
        "tratamentos": ["repouso", "vacinação", "vitamina A"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "caxumba": {
        "categoria": "infecciosa",
        "descricao": "Doença viral que afeta as glândulas salivares",
        "sintomas": ["inchaço das glândulas salivares", "febre", "dor de cabeça"],
        "tratamentos": ["repouso", "analgésicos", "vacinação"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "catapora": {
        "categoria": "infecciosa",
        "descricao": "Doença viral caracterizada por erupções cutâneas",
        "sintomas": ["erupções cutâneas", "febre", "coceira"],
        "tratamentos": ["antivirais", "antihistamínicos", "vacinação"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "herpes": {
        "categoria": "infecciosa",
        "descricao": "Infecção viral que causa feridas na pele",
        "sintomas": ["bolhas dolorosas", "coceira", "ardor"],
        "tratamentos": ["antivirais", "analgésicos", "medicação tópica"],
        "profissional": ["O profissional recomendado é: dermatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    }, 
    "sífilis": {
        "categoria": "infecciosa",
        "descricao": "Infecção bacteriana sexualmente transmissível",
        "sintomas": ["úlcera genital", "erupções cutâneas", "febre"],
        "tratamentos": ["antibióticos", "testes de acompanhamento"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "gonorreia": {
        "categoria": "infecciosa",
        "descricao": "Infecção bacteriana sexualmente transmissível",
        "sintomas": ["secreção uretral", "dor ao urinar", "dor pélvica"],
        "tratamentos": ["antibióticos", "tratamento do parceiro"],
        "profissional": ["O profissional recomendado é: urologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hpv": {
        "categoria": "infecciosa",
        "descricao": "Infecção viral que pode causar verrugas genitais",
        "sintomas": ["verrugas genitais", "alterações no colo do útero"],
        "tratamentos": ["crioterapia", "medicação tópica", "vacinação"],
        "profissional": ["O profissional recomendado é: ginecologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    }, 
    "cólera": {
        "categoria": "infecciosa",
        "descricao": "Infecção intestinal aguda causada por bactéria",
        "sintomas": ["diarreia intensa", "vômitos", "desidratação"],
        "tratamentos": ["reidratação", "antibióticos", "soro oral"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "febre tifoide": {
        "categoria": "infecciosa",
        "descricao": "Infecção bacteriana sistêmica",
        "sintomas": ["febre alta", "dor abdominal", "dor de cabeça"],
        "tratamentos": ["antibióticos", "hidratação", "vacinação"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "meningite bacteriana": {
        "categoria": "infecciosa",
        "descricao": "Inflamação das membranas que envolvem o cérebro",
        "sintomas": ["febre alta", "dor de cabeça intensa", "rigidez de nuca"],
        "tratamentos": ["antibióticos", "corticosteroides", "vacinação"],
        "profissional": ["O profissional recomendado é: neurologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "meningite viral": {
        "categoria": "infecciosa",
        "descricao": "Inflamação das membranas que envolvem o cérebro",
        "sintomas": ["febre", "dor de cabeça", "fotofobia"],
        "tratamentos": ["repouso", "hidratação", "medicação sintomática"],
        "profissional": ["O profissional recomendado é: neurologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "leptospirose": {
        "categoria": "infecciosa",
        "descricao": "Doença bacteriana transmitida por animais",
        "sintomas": ["febre alta", "dor muscular", "icterícia"],
        "tratamentos": ["antibióticos", "hidratação", "monitoramento"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "malária": {
        "categoria": "infecciosa",
        "descricao": "Doença parasitária transmitida por mosquitos",
        "sintomas": ["febre alta", "calafrios", "sudorese"],
        "tratamentos": ["antimaláricos", "repouso", "prevenção"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "toxoplasmose": {
        "categoria": "infecciosa",
        "descricao": "Infecção parasitária",
        "sintomas": ["febre", "gânglios inchados", "dor muscular"],
        "tratamentos": ["antibióticos", "repouso", "prevenção"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "lepra": {
        "categoria": "infecciosa",
        "descricao": "Doença bacteriana crônica que afeta a pele e nervos",
        "sintomas": ["manchas na pele", "perda de sensibilidade", "deformidades"],
        "tratamentos": ["antibióticos", "fisioterapia", "cirurgia"],
        "profissional": ["O profissional recomendado é: dermatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "doença de chagas": {
        "categoria": "infecciosa",
        "descricao": "Doença parasitária transmitida por insetos",
        "sintomas": ["febre", "inchaço no local da picada", "problemas cardíacos"],
        "tratamentos": ["antiparasitários", "tratamento sintomático"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "mononucleose infecciosa": {
        "categoria": "infecciosa",
        "descricao": "Doença viral conhecida como 'doença do beijo'",
        "sintomas": ["fadiga", "dor de garganta", "gânglios inchados"],
        "tratamentos": ["repouso", "hidratação", "analgésicos"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "febre amarela": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por mosquitos",
        "sintomas": ["febre alta", "icterícia", "dor de cabeça"],
        "tratamentos": ["repouso", "hidratação", "vacinação"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "raiva": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por animais",
        "sintomas": ["febre", "agitação", "hidrofobia"],
        "tratamentos": ["vacinação pós-exposição", "soro antirrábico"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "brucelose": {
        "categoria": "infecciosa",
        "descricao": "Doença bacteriana transmitida por animais",
        "sintomas": ["febre ondulante", "sudorese", "dor articular"],
        "tratamentos": ["antibióticos", "repouso"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hantavirose": {
        "categoria": "infecciosa",
        "descricao": "Doença viral transmitida por roedores",
        "sintomas": ["febre", "dores musculares", "dificuldade respiratória"],
        "tratamentos": ["suporte hospitalar", "oxigenoterapia"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "doença do legionario": {
        "categoria": "infecciosa",
        "descricao": "Forma grave de pneumonia",
        "sintomas": ["febre alta", "tosse", "falta de ar"],
        "tratamentos": ["antibióticos", "suporte respiratório"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "paracoccidiodomicose": {
        "categoria": "infecciosa",
        "descricao": "Doença fúngica sistêmica",
        "sintomas": ["lesões pulmonares", "úlceras cutâneas", "emagrecimento"],
        "tratamentos": ["antifúngicos", "tratamento prolongado"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "erliquiose": {
        "categoria": "infecciosa",
        "descricao": "Doença transmitida por carrapatos",
        "sintomas": ["febre", "dor de cabeça", "fadiga"],
        "tratamentos": ["antibióticos", "repouso"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "teníase": {
        "categoria": "infecciosa",
        "descricao": "Infecção intestinal por tênia",
        "sintomas": ["dor abdominal", "perda de peso", "segmentos do parasita nas fezes"],
        "tratamentos": ["anti-helmínticos", "higiene"],
        "profissional": ["O profissional recomendado é: infectologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "diabetes tipo 1": {
        "categoria": "crônica",
        "descricao": "Doença autoimune que destrói células produtoras de insulina",
        "sintomas": ["sede excessiva", "fome constante", "perda de peso"],
        "tratamentos": ["insulina", "monitoramento glicêmico", "dieta"],
        "profissional": ["O profissional recomendado é: endocrinologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "diabetes tipo 2": {
        "categoria": "crônica",
        "descricao": "Distúrbio no metabolismo da glicose",
        "sintomas": ["sede excessiva", "fome constante", "visão turva"],
        "tratamentos": ["medicação oral", "dieta balanceada", "exercícios"],
        "profissional": ["O profissional recomendado é: endocrinologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hipertensão": {
        "categoria": "crônica",
        "descricao": "Pressão arterial elevada",
        "sintomas": ["geralmente assintomática", "dor de cabeça", "tontura"],
        "tratamentos": ["medicação anti-hipertensiva", "dieta com pouco sal", "exercícios"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hipotireoidismo": {
        "categoria": "crônica",
        "descricao": "Produção insuficiente de hormônios tireoidianos",
        "sintomas": ["fadiga", "ganho de peso", "sensação de frio"],
        "tratamentos": ["reposição hormonal", "monitoramento"],
        "profissional": ["O profissional recomendado é: endocrinologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "gota": {
        "categoria": "crônica",
        "descricao": "Artrite por deposição de cristais de ácido úrico",
        "sintomas": ["dor intensa nas articulações", "vermelhidão", "inchaço"],
        "tratamentos": ["anti-inflamatórios", "alopurinol", "dieta"],
        "profissional": ["O profissional recomendado é: reumatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "osteoporose": {
        "categoria": "crônica",
        "descricao": "Perda de densidade óssea",
        "sintomas": ["fraturas frequentes", "diminuição da altura", "dor nas costas"],
        "tratamentos": ["suplementos de cálcio", "vitamina D", "exercícios"],
        "profissional": ["O profissional recomendado é: reumatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "artrite reumatóide": {
        "categoria": "crônica",
        "descricao": "Doença autoimune que afeta as articulações",
        "sintomas": ["dor articular", "rigidez matinal", "inchaço"],
        "tratamentos": ["anti-inflamatórios", "imunossupressores", "fisioterapia"],
        "profissional": ["O profissional recomendado é: reumatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "doença de crohn": {
        "categoria": "crônica",
        "descricao": "Doença inflamatória intestinal",
        "sintomas": ["dor abdominal", "diarreia", "perda de peso"],
        "tratamentos": ["imunossupressores", "dieta", "cirurgia em casos graves"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "síndrome do intestino irritável": {
        "categoria": "crônica",
        "descricao": "Distúrbio funcional do intestino",
        "sintomas": ["dor abdominal", "alteração do hábito intestinal", "inchaço"],
        "tratamentos": ["dieta", "redução de estresse", "medicação sintomática"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "miastenia gravis": {
        "categoria": "crônica",
        "descricao": "Doença neuromuscular autoimune",
        "sintomas": ["fraqueza muscular", "ptose palpebral", "dificuldade para engolir"],
        "tratamentos": ["anticolinesterásicos", "imunossupressores", "plasmaférese"],
        "profissional": ["O profissional recomendado é: neurologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "rinite alérgica": {
        "categoria": "crônica",
        "descricao": "Inflamação das mucosas nasais por alergia",
        "sintomas": ["espirros", "coriza", "coceira no nariz"],
        "tratamentos": ["anti-histamínicos", "corticosteroides nasais", "evitar alérgenos"],
        "profissional": ["O profissional recomendado é: otorrinolaringologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "asma": {
        "categoria": "crônica",
        "descricao": "Doença inflamatória crônica das vias aéreas",
        "sintomas": ["chiado no peito", "falta de ar", "tosse"],
        "tratamentos": ["broncodilatadores", "corticosteroides inalatórios", "evitar gatilhos"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "dpoc": {
        "categoria": "crônica",
        "descricao": "Doença pulmonar obstrutiva crônica",
        "sintomas": ["falta de ar", "tosse crônica", "produção de catarro"],
        "tratamentos": ["broncodilatadores", "oxigenoterapia", "parar de fumar"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "bronquite crônica": {
        "categoria": "crônica",
        "descricao": "Inflamação persistente dos brônquios",
        "sintomas": ["tosse com catarro", "falta de ar", "chiado no peito"],
        "tratamentos": ["broncodilatadores", "antibióticos em exacerbações", "parar de fumar"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "enfisema": {
        "categoria": "crônica",
        "descricao": "Destruição dos alvéolos pulmonares",
        "sintomas": ["falta de ar", "tosse", "diminuição da capacidade física"],
        "tratamentos": ["broncodilatadores", "oxigenoterapia", "reabilitação pulmonar"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "fibrose pulmonar": {
        "categoria": "crônica",
        "descricao": "Formação de tecido cicatricial nos pulmões",
        "sintomas": ["falta de ar progressiva", "tosse seca", "fadiga"],
        "tratamentos": ["medicação antifibrótica", "oxigenoterapia", "transplante"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "doença renal crônica": {
        "categoria": "crônica",
        "descricao": "Perda progressiva da função renal",
        "sintomas": ["fadiga", "inchaço", "anemia"],
        "tratamentos": ["controle da pressão", "dieta renal", "diálise"],
        "profissional": ["O profissional recomendado é: nefrologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "síndrome nefrótica": {
        "categoria": "crônica",
        "descricao": "Distúrbio renal com perda de proteínas na urina",
        "sintomas": ["inchaço", "urina espumosa", "aumento de peso"],
        "tratamentos": ["corticosteroides", "diuréticos", "dieta"],
        "profissional": ["O profissional recomendado é: nefrologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "cirrose hepática": {
        "categoria": "crônica",
        "descricao": "Fibrose avançada do fígado",
        "sintomas": ["icterícia", "ascite", "fadiga"],
        "tratamentos": ["abstinência alcoólica", "dieta", "transplante"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "esteatose hepática": {
        "categoria": "crônica",
        "descricao": "Acúmulo de gordura no fígado",
        "sintomas": ["geralmente assintomática", "fadiga", "dor abdominal"],
        "tratamentos": ["perda de peso", "controle do diabetes", "exercícios"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "glaucoma": {
        "categoria": "crônica",
        "descricao": "Lesão do nervo óptico por aumento da pressão ocular",
        "sintomas": ["perda gradual da visão periférica", "dor ocular"],
        "tratamentos": ["colírios", "laser", "cirurgia"],
        "profissional": ["O profissional recomendado é: oftalmologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "catarata": {
        "categoria": "crônica",
        "descricao": "Opacificação do cristalino",
        "sintomas": ["visão embaçada", "sensibilidade à luz", "mudança frequente de grau"],
        "tratamentos": ["cirurgia", "óculos"],
        "profissional": ["O profissional recomendado é: oftalmologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "doença arterial periferica": {
        "categoria": "crônica",
        "descricao": "Obstrução das artérias dos membros",
        "sintomas": ["dor nas pernas ao caminhar", "feridas que não cicatrizam"],
        "tratamentos": ["exercícios", "medicação", "angioplastia"],
        "profissional": ["O profissional recomendado é: angiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "infarto miocárdio": {
        "categoria": "cardiovascular",
        "descricao": "Obstrução do fluxo sanguíneo para o coração",
        "sintomas": ["dor no peito", "falta de ar", "sudorese"],
        "tratamentos": ["desobstrução arterial", "medicação", "reabilitação"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "insuficiencia cardíaca": {
        "categoria": "cardiovascular",
        "descricao": "Incapacidade do coração de bombear sangue adequadamente",
        "sintomas": ["falta de ar", "inchaço nas pernas", "fadiga"],
        "tratamentos": ["diuréticos", "medicação", "restrição de sal"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "arritmias": {
        "categoria": "cardiovascular",
        "descricao": "Alterações no ritmo cardíaco",
        "sintomas": ["palpitações", "tontura", "desmaio"],
        "tratamentos": ["medicação", "marcapasso", "ablação"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "endocardite": {
        "categoria": "cardiovascular",
        "descricao": "Infecção das válvulas cardíacas",
        "sintomas": ["febre", "sopro cardíaco", "fadiga"],
        "tratamentos": ["antibióticos", "cirurgia"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "miocardite": {
        "categoria": "cardiovascular",
        "descricao": "Inflamação do músculo cardíaco",
        "sintomas": ["dor no peito", "arritmia", "falta de ar"],
        "tratamentos": ["repouso", "medicação", "tratamento da causa"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "pericardite": {
        "categoria": "cardiovascular",
        "descricao": "Inflamação do pericárdio",
        "sintomas": ["dor no peito", "febre", "tosse"],
        "tratamentos": ["anti-inflamatórios", "repouso", "pericardiocentese"],
        "profissional": ["O profissional recomendado é: cardiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "avc": {
        "categoria": "cardiovascular",
        "descricao": "Interrupção do fluxo sanguíneo para o cérebro",
        "sintomas": ["fraqueza em um lado do corpo", "dificuldade para falar", "tontura"],
        "tratamentos": ["trombólise", "reabilitação", "prevenção secundária"],
        "profissional": ["O profissional recomendado é: neurologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "aneurisma": {
        "categoria": "cardiovascular",
        "descricao": "Dilatação anormal de um vaso sanguíneo",
        "sintomas": ["geralmente assintomático", "dor intensa se romper"],
        "tratamentos": ["monitoramento", "cirurgia"],
        "profissional": ["O profissional recomendado é: cirurgião vascular"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "trombose venenosa profunda": {
        "categoria": "cardiovascular",
        "descricao": "Formação de coágulos nas veias profundas",
        "sintomas": ["inchaço", "dor", "vermelhidão na perna"],
        "tratamentos": ["anticoagulantes", "meias de compressão"],
        "profissional": ["O profissional recomendado é: angiologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "embolia pulmonar": {
        "categoria": "cardiovascular",
        "descricao": "Obstrução da artéria pulmonar por coágulo",
        "sintomas": ["falta de ar súbita", "dor no peito", "tosse com sangue"],
        "tratamentos": ["anticoagulantes", "trombolíticos", "oxigenoterapia"],
        "profissional": ["O profissional recomendado é: pneumologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "gastrite": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do revestimento do estômago",
        "sintomas": ["dor abdominal", "náusea", "indigestão"],
        "tratamentos": ["antiácidos", "antibióticos se H. pylori", "mudança na dieta"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "úlcera gástrica": {
        "categoria": "gastrointestinal",
        "descricao": "Ferida no revestimento do estômago",
        "sintomas": ["dor abdominal", "náusea", "vômitos"],
        "tratamentos": ["inibidor de bomba de prótons", "antibióticos", "mudança na dieta"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "drge": {
        "categoria": "gastrointestinal",
        "descricao": "Doença do refluxo gastroesofágico",
        "sintomas": ["azia", "regurgitação", "dor no peito"],
        "tratamentos": ["elevação da cabeceira", "medicação", "mudança na dieta"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hepatite alcoólica": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do fígado pelo álcool",
        "sintomas": ["icterícia", "ascite", "fadiga"],
        "tratamentos": ["abstinência alcoólica", "nutrição", "corticosteroides"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "pancreatite": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do pâncreas",
        "sintomas": ["dor abdominal intensa", "náusea", "vômitos"],
        "tratamentos": ["jejum", "analgésicos", "tratamento da causa"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "apendicite": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do apêndice",
        "sintomas": ["dor abdominal", "náusea", "febre"],
        "tratamentos": ["cirurgia", "antibióticos"],
        "profissional": ["O profissional recomendado é: cirurgião geral"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "constipação crônica": {
        "categoria": "gastrointestinal",
        "descricao": "Dificuldade persistente para evacuar",
        "sintomas": ["evacuações infrequentes", "fezes duras", "esforço excessivo"],
        "tratamentos": ["fibras", "laxantes", "hidratação"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hemorróida": {
        "categoria": "gastrointestinal",
        "descricao": "Dilatação das veias do ânus",
        "sintomas": ["sangramento", "coceira", "dor"],
        "tratamentos": ["fibras", "banhos de assento", "cirurgia"],
        "profissional": ["O profissional recomendado é: proctologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hérnia umbilical": {
        "categoria": "gastrointestinal",
        "descricao": "Protrusão de conteúdo abdominal pelo umbigo",
        "sintomas": ["protuberância no umbigo", "dor"],
        "tratamentos": ["observação", "cirurgia"],
        "profissional": ["O profissional recomendado é: cirurgião geral"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "refluxo biliar": {
        "categoria": "gastrointestinal",
        "descricao": "Retorno da bile para o estômago",
        "sintomas": ["azia", "náusea", "vômito bilioso"],
        "tratamentos": ["medicação", "mudança na dieta", "cirurgia"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "esofagite": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do esôfago",
        "sintomas": ["azia", "dificuldade para engolir", "dor no peito"],
        "tratamentos": ["inibidor de bomba de prótons", "mudança na dieta"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "colangite": {
        "categoria": "gastrointestinal",
        "descricao": "Infecção das vias biliares",
        "sintomas": ["febre", "icterícia", "dor abdominal"],
        "tratamentos": ["antibióticos", "descompressão biliar"],
        "profissional": ["O profissional recomendado é: hepatologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "enterite bacteriana": {
        "categoria": "gastrointestinal",
        "descricao": "Infecção bacteriana do intestino",
        "sintomas": ["diarreia", "dor abdominal", "febre"],
        "tratamentos": ["antibióticos", "hidratação"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "gastroenterite": {
        "categoria": "gastrointestinal",
        "descricao": "Inflamação do estômago e intestinos",
        "sintomas": ["diarreia", "vômitos", "dor abdominal"],
        "tratamentos": ["hidratação", "repouso", "dieta branda"],
        "profissional": ["O profissional recomendado é: gastroenterologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "hérnia de disco": {
        "categoria": "musculoesquelética",
        "descricao": "Deslocamento do disco intervertebral",
        "sintomas": ["dor nas costas", "dor irradiada", "formigamento"],
        "tratamentos": ["fisioterapia", "analgésicos", "cirurgia"],
        "profissional": ["O profissional recomendado é: ortopedista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "tenossinovite": {
        "categoria": "musculoesquelética",
        "descricao": "Inflamação da bainha do tendão",
        "sintomas": ["dor", "inchaço", "dificuldade de movimento"],
        "tratamentos": ["repouso", "anti-inflamatórios", "fisioterapia"],
        "profissional": ["O profissional recomendado é: ortopedista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "bursite": {
        "categoria": "musculoesquelética",
        "descricao": "Inflamação da bursa",
        "sintomas": ["dor", "inchaço", "rigidez"],
        "tratamentos": ["repouso", "anti-inflamatórios", "fisioterapia"],
        "profissional": ["O profissional recomendado é: ortopedista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "câncer de pulmão": {
        "categoria": "oncológica",
        "descricao": "Crescimento descontrolado de células no pulmão",
        "sintomas": ["tosse persistente", "perda de peso", "dor no peito"],
        "tratamentos": ["cirurgia", "quimioterapia", "radioterapia"],
        "profissional": ["O profissional recomendado é: oncologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "cancer no intestino": {
        "categoria": "oncológica",
        "descricao": "Crescimento descontrolado de células no intestino",
        "sintomas": ["sangue nas fezes", "alteração do hábito intestinal", "perda de peso"],
        "tratamentos": ["cirurgia", "quimioterapia", "radioterapia"],
        "profissional": ["O profissional recomendado é: oncologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "leucemia": {
        "categoria": "oncológica",
        "descricao": "Câncer das células sanguíneas",
        "sintomas": ["fadiga", "infecções frequentes", "sangramentos"],
        "tratamentos": ["quimioterapia", "transplante de medula", "terapia alvo"],
        "profissional": ["O profissional recomendado é: hematologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "câncer colorretal": {
        "categoria": "oncológica",
        "descricao": "Câncer do cólon ou reto",
        "sintomas": ["sangue nas fezes", "alteração do hábito intestinal", "dor abdominal"],
        "tratamentos": ["cirurgia", "quimioterapia", "radioterapia"],
        "profissional": ["O profissional recomendado é: oncologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "câncer de fígado": {
        "categoria": "oncológica",
        "descricao": "Crescimento descontrolado de células no fígado",
        "sintomas": ["dor abdominal", "icterícia", "perda de peso"],
        "tratamentos": ["cirurgia", "quimioembolização", "transplante"],
        "profissional": ["O profissional recomendado é: oncologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "pedra nos rins": {
        "categoria": "urológica",
        "descricao": "Formação de cálculos no trato urinário",
        "sintomas": ["dor lombar intensa", "sangue na urina", "náusea"],
        "tratamentos": ["analgésicos", "hidratação", "litotripsia"],
        "profissional": ["O profissional recomendado é: urologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "insuficiência renal aguda": {
        "categoria": "urológica",
        "descricao": "Perda rápida da função renal",
        "sintomas": ["diminuição da diurese", "inchaço", "confusão"],
        "tratamentos": ["tratamento da causa", "diálise", "controle hidroeletrolítico"],
        "profissional": ["O profissional recomendado é: nefrologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    },
    "anemia": {
        "categoria": "hematológica",
        "descricao": "Redução da quantidade de hemoglobina no sangue",
        "sintomas": ["fadiga", "palidez", "falta de ar"],
        "tratamentos": ["suplementos de ferro", "vitamina B12"],
        "profissional": ["O profissional recomendado é: hematologista"],
        "indicação": ["Lembre de sempre procurar um médico especializado!"]
    }
}
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')

def words(text): 
    return re.findall(r'[\w\-]+', text.lower())

disease_names = ' '.join([nome.replace(' ', '-') for nome in BANCO_DE_DOENCAS.keys()])
WORDS = Counter(words(disease_names))

def P(word, N=sum(WORDS.values())): 
    return WORDS[word] / N

def correction(word): 
    candidates_list = candidates(word)
    return max(candidates_list, key=P) if candidates_list else word

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyzçáéíóúâêîôûãõàèìòùäëïöüñ0123456789 '
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def suggest_correction(word):
    if not word or not isinstance(word, str):
        return None
    corrected = correction(word.replace(' ', '-'))
    corrected_with_space = corrected.replace('-', ' ')
    
    if corrected != word and corrected_with_space in BANCO_DE_DOENCAS:
        return corrected_with_space
    
    possible_matches = [disease for disease in BANCO_DE_DOENCAS 
                       if disease.replace(' ', '').lower().startswith(word.replace(' ', '').lower()) 
                       and any(c.isdigit() for c in disease)]
    
    if possible_matches:
        return sorted(possible_matches, key=len)[0]
    
    return None



def exibir_menu():
    print("\n" + "="*30)
    print("  SISTEMA DE INFORMAÇÕES SOBRE DOENÇAS")
    print("="*30)
    print("1. Buscar doença")
    print("2. Listar doenças por categoria")
    print("3. Sintomas e tratamentos")
    print("4. Sair")
    print("="*30)


def buscar_doenca(nome=None):
    if nome is None:
        nome = input("\nDigite o nome da doença: ").strip().lower()
        limpar_tela()
    if not nome:
        print("Erro: Nome não pode estar vazio!")
        return
    
    if nome in BANCO_DE_DOENCAS:
        doenca = BANCO_DE_DOENCAS[nome]
        print(f"\n{'-'*30}\n{nome.upper()}\n{'-'*30}")
        print(f"Descrição: {doenca['descricao']}")
        print(f"Sintomas: {', '.join(doenca['sintomas'])}")
        print(f"Tratamentos: {', '.join(doenca['tratamentos'])}")
        print(f"Indicação: {', '.join(doenca['indicação'])}")
    else:
        suggestion = suggest_correction(nome)
        if suggestion:
            print(f"\nDoença não encontrada. Você quis dizer '{suggestion}'?")
            if input("(S/N): ").lower() == 's':
                buscar_doenca(suggestion)
        else:
            print("Doença não encontrada!")

def listar_por_categoria():
    categorias = set()
    for doenca in BANCO_DE_DOENCAS.values():
        categorias.add(doenca['categoria'])
    categoria_dict = {index: cat for index, cat in enumerate(categorias, start=1)}

    print("\nCategorias disponíveis:")
    for index, cat in categoria_dict.items():  
        print(f"{index}. {cat.capitalize()}")
    
    try:
        categoria_num = int(input("Digite o número da categoria: ").strip())
        limpar_tela()
        if categoria_num in categoria_dict:
            categoria = categoria_dict[categoria_num].upper()  
            print(f"\nCategoria selecionada: {categoria}")
            
            doencas_categoria = [nome for nome, dados in BANCO_DE_DOENCAS.items() if dados['categoria'] == categoria_dict[categoria_num]]
            
            if doencas_categoria:
                print(f"\nDoenças na categoria '{categoria}':")
                for i, nome in enumerate(doencas_categoria, 1):
                    print(f"{i}. {nome.capitalize()}")
            else:
                print(f"Nenhuma doença encontrada na categoria '{categoria}'.")
        else:
            print("Número inválido. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")

def sintomas_tratamentos(nome=None):
    if nome is None:
        nome = input("\nDigite o nome da doença: ").strip().lower()
        limpar_tela()
    if nome in BANCO_DE_DOENCAS:
        doenca = BANCO_DE_DOENCAS[nome]
        print(f"\n{'-'*30}\n{nome.upper()}\n{'-'*30}")
        print("Sintoma           | Tratamento")
        print("-"*30)
        
        max_len = max(len(doenca['sintomas']), len(doenca['tratamentos']))
        
        for i in range(max_len):
            sintoma = doenca['sintomas'][i] if i < len(doenca['sintomas']) else "-"
            tratamento = doenca['tratamentos'][i] if i < len(doenca['tratamentos']) else "-"
            print(f"{str(sintoma).ljust(18)}| {tratamento}")
        
       
        print("-"*30)
        print(f"{doenca['profissional'][0]}")  
        print("-"*30)
        print(f"{doenca['indicação'][0]}")
    else:
        suggestion = suggest_correction(nome)
        if suggestion:
            print(f"\nDoença não encontrada. Você quis dizer '{suggestion}'?")
            if input("(S/N): ").lower() == 's':
                sintomas_tratamentos(suggestion)
        else:
            print("Doença não encontrada!")

def menu():
    while True:
        limpar_tela()
        print("""
             ⣴⣶⣶⠶⠖⠲⠶⣶⣶⣦⡄
             ⣿⡟⠁⠀⣶⣶⠀⠈⢻⣿⡇
   ⣀⣀⣀⣀⣀⣀⡀⢸⣿⡇⢸⣿⣿⣿⣿⡇⢸⣿⡇
   ⣿⣿⣿⣿⣿⣿⡇⢸⣿⣧⡀⠀⠿⠿⠀⢀⣼⣿⡇⢸⣿⣿⣿⣿⣿⣿⡇
   ⣿⣇⣀⣿⣀⣸⡇⢸⣿⣿⣿⣷⣶⣶⣾⣿⣿⣿⡇⢸⣿⣀⣸⣇⣀⣿⡇
   ⣿⡏⠉⣿⠉⢹⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⠉⢹⡏⠉⣿⡇
   ⣿⡟⠛⣿⠛⢻⡇⢸⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿ ⢸⣿⠛⢻⡟⠛⣿⡇
   ⣿⣧⣴⣿⣤⣾⡇⢸⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡇⢸⣿⣤⣾⣧⣴⣿⡇
   ⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⡇
 ⣤⣤⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣤⣤⣤⣤⣼⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣤
 ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
""")
        exibir_menu()
        
        opcao = input("\nDigite sua opção: ").strip()
        limpar_tela()
        
        if opcao == "1":
            buscar_doenca()
        elif opcao == "2":
            listar_por_categoria()
        elif opcao == "3":
            sintomas_tratamentos()
        elif opcao == "4":
            if input("\nTem certeza que deseja sair? (s/n): ").lower() == 's':
                print("Encerrando programa...")
                break
        else:
            print("Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")



menu()
