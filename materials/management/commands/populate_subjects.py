from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from materials.models import Material
import random

class Command(BaseCommand):
    help = 'Populate database with Computer Engineering subjects'
    
    def handle(self, *args, **options):
        # Computer Engineering subject codes with their respective names and periods
        subjects = {
            # G1 (1º Período)
            'ENG4010': ('Introdução à Engenharia', 'G1'),
            'EMP1310': ('Desenho Técnico I', 'G1'),
            'ENG4025': ('Introdução ao Cálculo', 'G1'),
            'CTC4001': ('Física I', 'G1'),
            'CTC4002': ('Laboratório de Física I', 'G1'),
            'CTC4003': ('Química Geral', 'G1'),
            'CRE1200': ('Leitura e Produção de Textos', 'G1'),
            
            # G2 (2º Período)
            'ENG4021': ('Cálculo I', 'G2'),
            'EMP1320': ('Desenho Técnico II', 'G2'),
            'INF1037': ('Programação em C', 'G2'),
            'MAT4161': ('Álgebra Linear I', 'G2'),
            'FIS4001': ('Física II', 'G2'),
            'MAT4200': ('Geometria Analítica', 'G2'),
            
            # G3 (3º Período)
            'INF1012': ('Programação Modular', 'G3'),
            'INF1009': ('Lógica para Computação', 'G3'),
            'ENG4033': ('Cálculo II', 'G3'),
            'ENG4431': ('Estatística e Modelos Probabilísticos', 'G3'),
            'ENG4420': ('Física III', 'G3'),
            'MAT4162': ('Álgebra Linear II', 'G3'),
            
            # G4 (4º Período)
            'FIS4002': ('Física IV', 'G4'),
            'MAT4202': ('Equações Diferenciais', 'G4'),
            'INF1383': ('Linguagens de Programação', 'G4'),
            'ENG4007': ('Cálculo III', 'G4'),
            'ENG4040': ('Fenômenos de Transporte', 'G4'),
            'ENG4502': ('Modelagem de Sistemas Dinâmicos', 'G4'),
            
            # G5 (5º Período)
            'ENG4501': ('Sinais e Sistemas Lineares', 'G5'),
            'ENG4402': ('Análise de Circuitos I', 'G5'),
            'MAT4174': ('Cálculo Numérico', 'G5'),
            'INF1010': ('Estruturas de Dados', 'G5'),
            'INF1018': ('Software Básico', 'G5'),
            'ENG4011': ('Cálculo Vetorial', 'G5'),
            
            # G6 (6º Período)
            'ENG4051': ('Análise de Circuitos II', 'G6'),
            'ENG4013': ('Sinais e Sistemas', 'G6'),
            'ENG4421': ('Eletrônica I', 'G6'),
            'MAT1320': ('Variáveis Complexas', 'G6'),
            'FIS4003': ('Física Moderna', 'G6'),
            'INF1301': ('Programação Orientada a Objetos', 'G6'),
            
            # G7 (7º Período)
            'ENG4061': ('Microeletrônica', 'G7'),
            'ENG4448': ('Eletrônica II', 'G7'),
            'INF1022': ('Sistemas de Computação', 'G7'),
            'INF1631': ('Banco de Dados', 'G7'),
            'INF1636': ('Análise e Projeto de Algoritmos', 'G7'),
            'INF1316': ('Sistemas Operacionais', 'G7'),
            
            # G8 (8º Período)
            'CRE0712': ('Empreendedorismo em Informática', 'G8'),
            'ENG4405': ('Eletrônica Digital', 'G8'),
            'INF1721': ('Redes de Computadores', 'G8'),
            'INF1041': ('Inteligência Artificial', 'G8'),
            'ENG1451': ('Controle I', 'G8'),
            'INF1640': ('Engenharia de Software', 'G8'),
            
            # G9 (9º Período)
            'FIL0300': ('Ética', 'G9'),
            'CRE1241': ('Cristianismo', 'G9'),
            'ENG4030': ('Tecnologia, Ética e Meio Ambiente', 'G9'),
            'EMP1330': ('Administração', 'G9'),
            'ENG4500': ('Controle II', 'G9'),
            'INF0312': ('Sistemas Distribuídos', 'G9'),
            
            # G10 (10º Período)
            'INF0303': ('Arquitetura de Computadores', 'G10'),
            'INF0305': ('Projeto Final', 'G10'),
            'JUR0205': ('Introdução ao Direito', 'G10'),
            'ENG4134': ('Processamento Digital de Sinais', 'G10'),
            'ELL0900': ('Inglês Instrumental', 'G10'),
            'EXT0100': ('Atividades Complementares', 'G10'),
            'CRE1275': ('Teologia', 'G10'),
            'ENG4135': ('Comunicações', 'G10'),
            'ENG4153': ('Robótica', 'G10'),
            'ACP0900': ('Atividade Curricular de Pesquisa', 'G10'),
        }
        
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@aluno.puc-rio.br',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: admin/admin123')
        
        # Material types for different subjects
        tipos_materiais = {
            'resumo': ['Resumo', 'Resumo Teórico', 'Resumo de Conceitos'],
            'apostila': ['Apostila Completa', 'Material de Estudo', 'Apostila do Professor'],
            'exercicios': ['Lista de Exercícios', 'Exercícios Resolvidos', 'Problemas Práticos'],
            'prova': ['Prova Antiga', 'Exame Anterior', 'Teste Passado'],
            'projeto': ['Projeto de Curso', 'Trabalho Final', 'Projeto Prático'],
        }
        
        materiais_criados = 0
        
        for codigo, (nome_materia, periodo) in subjects.items():
            # Create 2-3 materials per subject
            for i in range(random.randint(2, 3)):
                tipo = random.choice(list(tipos_materiais.keys()))
                tipo_nome = random.choice(tipos_materiais[tipo])
                
                titulo = f"{tipo_nome} - {nome_materia} ({codigo})"
                descricao = f"Material de {nome_materia} para estudantes de Engenharia da Computação. Este {tipo_nome.lower()} aborda os principais conceitos da disciplina {codigo}."
                
                # Add relevant tags
                tags_base = [codigo, nome_materia.lower().replace(' ', '_'), periodo.lower()]
                if 'Cálculo' in nome_materia:
                    tags_base.extend(['matematica', 'calculo', 'derivadas', 'integrais'])
                elif 'Programação' in nome_materia or 'INF' in codigo:
                    tags_base.extend(['programacao', 'computacao', 'algoritmos', 'codigo'])
                elif 'Física' in nome_materia:
                    tags_base.extend(['fisica', 'experimentos', 'laboratorio'])
                elif 'Eletrônica' in nome_materia or 'Circuitos' in nome_materia:
                    tags_base.extend(['eletronica', 'circuitos', 'hardware'])
                elif 'Banco' in nome_materia:
                    tags_base.extend(['sql', 'database', 'modelagem'])
                
                tags = ', '.join(tags_base[:6])  # Limit to 6 tags
                
                material, created = Material.objects.get_or_create(
                    titulo=titulo,
                    autor=admin_user,
                    defaults={
                        'descricao': descricao,
                        'tipo': tipo,
                        'materia': f"{codigo} - {nome_materia}",
                        'serie': periodo,
                        'arquivo': f'materiais/sample_{codigo}_{i+1}.pdf',  # Placeholder file path
                        'downloads': random.randint(0, 50),
                        'visualizacoes': random.randint(10, 200),
                        'destaque': random.choice([True, False]) if random.random() < 0.2 else False,
                        'tags': tags,
                    }
                )
                
                if created:
                    materiais_criados += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {materiais_criados} materials '
                f'for {len(subjects)} Computer Engineering subjects'
            )
        )