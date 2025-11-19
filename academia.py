#!/usr/bin/env python3
"""
SITE COMPLETO DA ACADEMIA SAMUFIT
Um único arquivo Python com todas as funcionalidades
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
import json
from datetime import datetime

# =============================================
# CONFIGURAÇÃO DO FLASK
# =============================================
app = Flask(__name__)
app.secret_key = 'samufit_academia_secret_key_2025'

# =============================================
# DADOS DA ACADEMIA
# =============================================
PLANOS = [
    {
        'id': 1,
        'nome': 'Básico',
        'preco': 79.90,
        'recursos': [
            'Acesso à musculação',
            'Acesso à área de cardio', 
            'Avaliação física inicial',
            'App de treinos básico',
            'Água e toalhas de cortesia'
        ],
        'popular': False,
        'cor': 'outline-primary'
    },
    {
        'id': 2,
        'nome': 'Premium',
        'preco': 119.90,
        'recursos': [
            'Todos os recursos do plano Básico',
            'Acesso a todas as aulas coletivas',
            'Acesso à área de lutas', 
            'Acesso ilimitado',
            'App premium com treinos personalizados',
            'Avaliação física mensal'
        ],
        'popular': True,
        'cor': 'primary'
    },
    {
        'id': 3,
        'nome': 'Família',
        'preco': 199.90,
        'recursos': [
            'Todos os recursos do plano Premium',
            'Até 4 pessoas da mesma família',
            'Desconto em personal trainer',
            'Acesso à área kids',
            'Avaliação física mensal para todos',
            'Estacionamento gratuito'
        ],
        'popular': False,
        'cor': 'outline-success'
    }
]

HORARIOS = {
    'Musculação': {
        'Segunda': '05:00 - 23:00',
        'Terça': '05:00 - 23:00', 
        'Quarta': '05:00 - 23:00',
        'Quinta': '05:00 - 23:00',
        'Sexta': '05:00 - 22:00',
        'Sábado': '06:00 - 20:00',
        'Domingo': '08:00 - 18:00'
    },
    'Cross Training': {
        'Segunda': '06:00, 12:00, 18:00, 20:00',
        'Terça': '06:00, 12:00, 18:00, 20:00',
        'Quarta': '06:00, 12:00, 18:00, 20:00',
        'Quinta': '06:00, 12:00, 18:00, 20:00',
        'Sexta': '06:00, 12:00, 18:00',
        'Sábado': '08:00, 10:00, 14:00',
        'Domingo': '09:00, 11:00'
    },
    'Funcional': {
        'Segunda': '07:00, 09:00, 17:00, 19:00',
        'Terça': '07:00, 09:00, 17:00, 19:00',
        'Quarta': '07:00, 09:00, 17:00, 19:00',
        'Quinta': '07:00, 09:00, 17:00, 19:00', 
        'Sexta': '07:00, 09:00, 17:00',
        'Sábado': '08:00, 10:00',
        'Domingo': '09:00'
    },
    'Spinning': {
        'Segunda': '06:30, 12:30, 19:30',
        'Terça': '06:30, 12:30, 19:30',
        'Quarta': '06:30, 12:30, 19:30',
        'Quinta': '06:30, 12:30, 19:30',
        'Sexta': '06:30, 12:30',
        'Sábado': '09:00, 11:00',
        'Domingo': '10:00'
    },
    'Yoga': {
        'Segunda': '07:30, 18:30',
        'Terça': '07:30, 18:30',
        'Quarta': '07:30, 18:30',
        'Quinta': '07:30, 18:30',
        'Sexta': '07:30',
        'Sábado': '09:30',
        'Domingo': '10:30'
    },
    'Pilates': {
        'Segunda': '08:00, 14:00, 19:00',
        'Terça': '08:00, 14:00, 19:00',
        'Quarta': '08:00, 14:00, 19:00',
        'Quinta': '08:00, 14:00, 19:00',
        'Sexta': '08:00, 14:00',
        'Sábado': '09:00',
        'Domingo': 'Fechado'
    }
}

DEPOIMENTOS = [
    {
        'nome': 'Carlos Silva',
        'idade': 35,
        'tempo_academia': '2 anos',
        'texto': 'Há 2 anos na SamuFit e nunca me senti tão bem! Perdi 15kg e ganhei muita disposição para o trabalho e família.',
        'avaliacao': 5,
        'profissao': 'Engenheiro'
    },
    {
        'nome': 'Ana Paula', 
        'idade': 28,
        'tempo_academia': '1 ano',
        'texto': 'Os professores são excelentes e a estrutura é impecável. Recomendo para todas as idades! Melhorou minha autoestima.',
        'avaliacao': 5,
        'profissao': 'Professora'
    },
    {
        'nome': 'Roberto Alves',
        'idade': 65,
        'tempo_academia': '3 anos', 
        'texto': 'Comecei com 60 anos e hoje tenho mais energia que muitos jovens. A academia mudou minha vida após a aposentadoria!',
        'avaliacao': 5,
        'profissao': 'Aposentado'
    },
    {
        'nome': 'Mariana Costa',
        'idade': 42,
        'tempo_academia': '6 meses',
        'texto': 'Ambiente acolhedor e professores muito atenciosos. Perdi 8kg e me sinto mais confiante.',
        'avaliacao': 5,
        'profissao': 'Empresária'
    }
]

MODALIDADES = [
    {'nome': 'Musculação', 'icone': 'dumbbell', 'destaque': True},
    {'nome': 'Cross Training', 'icone': 'fire', 'destaque': True},
    {'nome': 'Funcional', 'icone': 'running', 'destaque': True},
    {'nome': 'Spinning', 'icone': 'bicycle', 'destaque': False},
    {'nome': 'Yoga', 'icone': 'spa', 'destaque': False},
    {'nome': 'Pilates', 'icone': 'procedures', 'destaque': False},
    {'nome': 'Boxe', 'icone': 'fist-raised', 'destaque': False},
    {'nome': 'Dança', 'icone': 'music', 'destaque': False}
]

# =============================================
# TEMPLATES HTML
# =============================================

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SamuFit Academia{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #007bff;
            --secondary-color: #6c757d;
            --accent-color: #ff6b6b;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding-top: 76px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .main-content {
            background: white;
            border-radius: 20px;
            margin: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            min-height: calc(100vh - 140px);
        }

        .hero-section {
            background: linear-gradient(135deg, var(--primary-color), #0056b3);
            border-radius: 20px 20px 0 0;
        }

        .card {
            transition: all 0.3s ease;
            border: none;
            border-radius: 15px;
            overflow: hidden;
        }

        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }

        .navbar {
            border-radius: 10px;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .btn-primary {
            background: linear-gradient(45deg, var(--primary-color), #0056b3);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.3);
        }

        .plan-card.popular {
            border: 3px solid var(--primary-color);
            position: relative;
            overflow: hidden;
        }

        .plan-card.popular::before {
            content: "MAIS POPULAR";
            position: absolute;
            top: 15px;
            right: -30px;
            background: var(--primary-color);
            color: white;
            padding: 5px 30px;
            transform: rotate(45deg);
            font-size: 12px;
            font-weight: bold;
        }

        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, var(--primary-color), #0056b3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
        }

        .feature-icon i {
            font-size: 24px;
            color: white;
        }

        .testimonial-card {
            border-left: 4px solid var(--primary-color);
        }

        .gallery-item {
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            height: 250px;
            background: linear-gradient(45deg, #f8f9fa, #e9ecef);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6c757d;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .gallery-item i {
            font-size: 48px;
            margin-bottom: 10px;
        }

        .schedule-table {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .schedule-table th {
            background: linear-gradient(45deg, var(--primary-color), #0056b3);
            color: white;
            border: none;
            padding: 15px;
        }

        .schedule-table td {
            padding: 12px 15px;
            border-color: #f1f3f4;
        }

        .schedule-table tr:hover {
            background-color: #f8f9fa;
        }

        .contact-form {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .floating-alert {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 1050;
            min-width: 300px;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-fade-in {
            animation: fadeInUp 0.6s ease;
        }

        .stats-number {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(45deg, var(--primary-color), #0056b3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-dumbbell me-2"></i>SamuFit
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Início</a></li>
                    <li class="nav-item"><a class="nav-link" href="/planos">Planos</a></li>
                    <li class="nav-item"><a class="nav-link" href="/horarios">Horários</a></li>
                    <li class="nav-item"><a class="nav-link" href="/modalidades">Modalidades</a></li>
                    <li class="nav-item"><a class="nav-link" href="/galeria">Galeria</a></li>
                    <li class="nav-item"><a class="nav-link" href="/depoimentos">Depoimentos</a></li>
                    <li class="nav-item"><a class="nav-link" href="/contato">Contato</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="floating-alert alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show animate-fade-in">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <div class="main-content">
        {% block content %}{% endblock %}
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <h5 class="fw-bold"><i class="fas fa-dumbbell me-2"></i>SamuFit</h5>
                    <p class="mb-0">Sua jornada para uma vida mais saudável começa aqui.</p>
                </div>
                <div class="col-md-4 mb-4">
                    <h6 class="fw-bold">Contato</h6>
                    <p class="mb-1"><i class="fas fa-map-marker-alt me-2"></i>Rua das Academias, 123 - Timon/MA</p>
                    <p class="mb-1"><i class="fas fa-phone me-2"></i>(99) 9999-9999</p>
                    <p class="mb-0"><i class="fas fa-envelope me-2"></i>contato@samufit.com</p>
                </div>
                <div class="col-md-4">
                    <h6 class="fw-bold">Horário de Funcionamento</h6>
                    <p class="mb-1">Segunda a Sexta: 5h às 23h</p>
                    <p class="mb-1">Sábado: 6h às 20h</p>
                    <p class="mb-0">Domingo: 8h às 18h</p>
                </div>
            </div>
            <hr class="my-4">
            <div class="text-center">
                <p class="mb-0">&copy; 2023 SamuFit Academia. Todos os direitos reservados.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-dismiss alerts after 5 seconds
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);

        // Phone number mask
        document.addEventListener('DOMContentLoaded', function() {
            const phoneInput = document.getElementById('telefone');
            if (phoneInput) {
                phoneInput.addEventListener('input', function(e) {
                    let value = e.target.value.replace(/\\D/g, '');
                    if (value.length > 11) value = value.substring(0, 11);
                    
                    if (value.length > 10) {
                        value = value.replace(/^(\\d{2})(\\d{5})(\\d{4})/, '($1) $2-$3');
                    } else if (value.length > 6) {
                        value = value.replace(/^(\\d{2})(\\d{4})(\\d{0,4})/, '($1) $2-$3');
                    } else if (value.length > 2) {
                        value = value.replace(/^(\\d{2})(\\d{0,5})/, '($1) $2');
                    } else if (value.length > 0) {
                        value = value.replace(/^(\\d*)/, '($1');
                    }
                    
                    e.target.value = value;
                });
            }

            // Form validation
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    let valid = true;
                    const requiredFields = form.querySelectorAll('[required]');
                    
                    requiredFields.forEach(field => {
                        if (!field.value.trim()) {
                            valid = false;
                            field.classList.add('is-invalid');
                        } else {
                            field.classList.remove('is-invalid');
                        }
                    });

                    if (!valid) {
                        e.preventDefault();
                        alert('Por favor, preencha todos os campos obrigatórios.');
                    }
                });
            });

            // Add animation to cards on scroll
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            document.querySelectorAll('.card').forEach(card => {
                card.style.opacity = '0';
                observer.observe(card);
            });
        });
    </script>
</body>
</html>
'''

INDEX_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<!-- Hero Section -->
<section class="hero-section text-white py-5">
    <div class="container py-5">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">Transforme seu corpo, transforme sua vida</h1>
                <p class="lead mb-4">Na SamuFit, oferecemos equipamentos de última geração, professores qualificados e um ambiente motivador para você alcançar seus objetivos.</p>
                <div class="d-flex gap-3 flex-wrap">
                    <a href="/planos" class="btn btn-light btn-lg">Conheça nossos planos</a>
                    <a href="/contato" class="btn btn-outline-light btn-lg">Agende uma visita</a>
                </div>
            </div>
            <div class="col-lg-6 text-center">
                <div class="gallery-item mx-auto" style="max-width: 500px; height: 400px;">
                    <div class="text-center text-dark">
                        <i class="fas fa-dumbbell fa-5x mb-3"></i>
                        <h4>Academia SamuFit</h4>
                        <p>Equipamentos de última geração</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Stats Section -->
<section class="py-5 bg-light">
    <div class="container">
        <div class="row text-center">
            <div class="col-md-3 mb-4">
                <div class="stats-number">2.000+</div>
                <p class="fw-bold">Alunos Satisfeitos</p>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stats-number">15</div>
                <p class="fw-bold">Modalidades</p>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stats-number">5</div>
                <p class="fw-bold">Anos no Mercado</p>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stats-number">24/7</div>
                <p class="fw-bold">App de Treinos</p>
            </div>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold mb-3">Por que escolher a SamuFit?</h2>
            <p class="lead">Tudo que você precisa para alcançar seus objetivos</p>
        </div>
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-dumbbell"></i>
                        </div>
                        <h4 class="fw-bold">Equipamentos Modernos</h4>
                        <p class="text-muted">Máquinas de última geração para todos os grupos musculares, importadas e com manutenção constante.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-user-md"></i>
                        </div>
                        <h4 class="fw-bold">Professores Qualificados</h4>
                        <p class="text-muted">Profissionais especializados com certificação CREF para orientar seu treino com segurança e eficiência.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-clock"></i>
                        </div>
                        <h4 class="fw-bold">Horários Flexíveis</h4>
                        <p class="text-muted">Funcionamos de segunda a domingo com horários estendidos para se adaptar à sua rotina.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="py-5 bg-primary text-white">
    <div class="container text-center">
        <h2 class="display-5 fw-bold mb-4">Pronto para começar sua transformação?</h2>
        <p class="lead mb-4">Junte-se aos mais de 2.000 alunos que já transformaram suas vidas na SamuFit</p>
        <a href="/contato" class="btn btn-light btn-lg px-5">Comece Agora</a>
    </div>
</section>
''')

PLANOS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3">Nossos Planos</h1>
        <p class="lead">Escolha o plano que melhor se adapta ao seu estilo de vida e objetivos</p>
    </div>

    <div class="row justify-content-center">
        {% for plano in planos %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100 plan-card shadow-sm {% if plano.popular %}popular{% endif %}">
                <div class="card-body text-center p-4">
                    <h3 class="card-title fw-bold text-primary">{{ plano.nome }}</h3>
                    <div class="price display-4 fw-bold text-dark my-4">
                        R$ <span>{{ "%.2f"|format(plano.preco) }}</span>
                    </div>
                    <p class="text-muted">por mês</p>
                    
                    <ul class="list-unstyled my-4">
                        {% for recurso in plano.recursos %}
                        <li class="mb-3">
                            <i class="fas fa-check-circle text-success me-2"></i>
                            {{ recurso }}
                        </li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="card-footer bg-transparent text-center py-4">
                    <button class="btn btn-{{ plano.cor }} btn-lg px-5" 
                            onclick="showContactForm('{{ plano.nome }}')">
                        {% if plano.popular %}
                        <i class="fas fa-crown me-2"></i>
                        {% endif %}
                        Assinar Agora
                    </button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Additional Info -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="card bg-light border-0">
                <div class="card-body p-5">
                    <h4 class="card-title text-center mb-4">Benefícios Inclusos em Todos os Planos</h4>
                    <div class="row text-center">
                        <div class="col-md-3 mb-3">
                            <i class="fas fa-wifi fa-2x text-primary mb-2"></i>
                            <h6>Wi-Fi Gratuito</h6>
                        </div>
                        <div class="col-md-3 mb-3">
                            <i class="fas fa-car fa-2x text-primary mb-2"></i>
                            <h6>Estacionamento</h6>
                        </div>
                        <div class="col-md-3 mb-3">
                            <i class="fas fa-lock fa-2x text-primary mb-2"></i>
                            <h6>Armários</h6>
                        </div>
                        <div class="col-md-3 mb-3">
                            <i class="fas fa-shower fa-2x text-primary mb-2"></i>
                            <h6>Vestiários</h6>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function showContactForm(plano) {
    if (confirm(`Deseja assinar o plano ${plano}? Você será redirecionado para nossa página de contato.`)) {
        window.location.href = "/contato";
    }
}
</script>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Planos - SamuFit Academia')

HORARIOS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3">Horários das Aulas</h1>
        <p class="lead">Confira os horários disponíveis para cada modalidade e planeje seus treinos</p>
    </div>

    {% for modalidade, dias in horarios.items() %}
    <div class="card shadow-sm mb-4">
        <div class="card-header bg-primary text-white">
            <h4 class="mb-0">
                <i class="fas fa-{{ modalidades | selectattr("nome", "equalto", modalidade) | map(attribute="icone") | first }} me-2"></i>
                {{ modalidade }}
            </h4>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0 schedule-table">
                    <thead>
                        <tr>
                            <th>Dia da Semana</th>
                            <th>Horários</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for dia, horario in dias.items() %}
                        <tr>
                            <td class="fw-bold">{{ dia }}</td>
                            <td>{{ horario }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endfor %}

    <!-- Important Information -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="alert alert-info">
                <h5><i class="fas fa-info-circle me-2"></i>Informações Importantes</h5>
                <ul class="mb-0">
                    <li>As aulas têm duração de 1 hora cada sessão</li>
                    <li>Recomendamos chegar 15 minutos antes do início da aula</li>
                    <li>É necessário fazer reserva para aulas coletivas através do nosso app</li>
                    <li>Em feriados, os horários podem sofrer alterações - consulte nossa programação especial</li>
                    <li>Vagas limitadas para garantir a qualidade do atendimento</li>
                </ul>
            </div>
        </div>
    </div>
</div>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Horários - SamuFit Academia')

MODALIDADES_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3">Nossas Modalidades</h1>
        <p class="lead">Diversas opções para você encontrar o exercício perfeito</p>
    </div>

    <div class="row">
        {% for modalidade in modalidades %}
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card h-100 text-center shadow-sm border-0">
                <div class="card-body p-4">
                    <div class="feature-icon mx-auto mb-3">
                        <i class="fas fa-{{ modalidade.icone }}"></i>
                    </div>
                    <h5 class="card-title fw-bold">{{ modalidade.nome }}</h5>
                    {% if modalidade.destaque %}
                    <span class="badge bg-primary">Mais Procurada</span>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Description Section -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="card bg-light border-0">
                <div class="card-body p-5">
                    <h3 class="text-center mb-4">Encontre sua Modalidade Ideal</h3>
                    <div class="row">
                        <div class="col-md-6">
                            <h5><i class="fas fa-dumbbell text-primary me-2"></i>Musculação</h5>
                            <p class="text-muted">Ideal para ganho de massa muscular, força e definição. Equipamentos de última geração.</p>
                            
                            <h5><i class="fas fa-fire text-primary me-2"></i>Cross Training</h5>
                            <p class="text-muted">Treinos funcionais de alta intensidade para queima calórica e condicionamento.</p>
                            
                            <h5><i class="fas fa-running text-primary me-2"></i>Funcional</h5>
                            <p class="text-muted">Exercícios que simulam movimentos do dia a dia, melhorando a funcionalidade corporal.</p>
                        </div>
                        <div class="col-md-6">
                            <h5><i class="fas fa-bicycle text-primary me-2"></i>Spinning</h5>
                            <p class="text-muted">Aulas de bike indoor com música motivadora para alto gasto calórico.</p>
                            
                            <h5><i class="fas fa-spa text-primary me-2"></i>Yoga & Pilates</h5>
                            <p class="text-muted">Alongamento, relaxamento e fortalecimento do core para bem-estar integral.</p>
                            
                            <h5><i class="fas fa-fist-raised text-primary me-2"></i>Artes Marciais</h5>
                            <p class="text-muted">Boxe e outras modalidades para defesa pessoal e condicionamento físico.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Modalidades - SamuFit Academia')

GALERIA_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3">Nossa Estrutura</h1>
        <p class="lead">Conheça nossas instalações e equipamentos de última geração</p>
    </div>

    <div class="row">
        {% for i in range(8) %}
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="gallery-item">
                <div class="text-center">
                    <i class="fas fa-{{ ['dumbbell', 'running', 'fire', 'bicycle', 'spa', 'procedures', 'users', 'shower'][i] }}"></i>
                    <p class="mt-2 mb-0">{{ ['Área de Musculação', 'Cardio', 'Cross Training', 'Spinning', 'Yoga', 'Pilates', 'Aulas Coletivas', 'Vestiários'][i] }}</p>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Facilities Description -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="card bg-light border-0">
                <div class="card-body p-5">
                    <h3 class="text-center mb-4">Estrutura Completa</h3>
                    <div class="row">
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-dumbbell text-primary me-2"></i>Área de Musculação</h5>
                            <p class="text-muted">2000m² com equipamentos importados, halteres, barras e máquinas de última geração.</p>
                        </div>
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-running text-primary me-2"></i>Área Cardio</h5>
                            <p class="text-muted">Esteiras, bikes elípticas, transport e escadas rolantes com sistema de entretenimento.</p>
                        </div>
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-users text-primary me-2"></i>Studios de Aula</h5>
                            <p class="text-muted">4 studios climatizados para aulas coletivas com piso especial e espelhos.</p>
                        </div>
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-shower text-primary me-2"></i>Vestiários</h5>
                            <p class="text-muted">Amplos vestiários masculino e feminino com armários, chuveiros e secadores.</p>
                        </div>
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-car text-primary me-2"></i>Estacionamento</h5>
                            <p class="text-muted">Estacionamento gratuito com 200 vagas cobertas e sistema de segurança 24h.</p>
                        </div>
                        <div class="col-md-4 mb-4">
                            <h5><i class="fas fa-couch text-primary me-2"></i>Área de Descanso</h5>
                            <p class="text-muted">Espaço lounge com Wi-Fi, tomadas e água mineral para relaxamento pós-treino.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Galeria - SamuFit Academia')

DEPOIMENTOS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-4 fw-bold mb-3">O que nossos alunos dizem</h1>
        <p class="lead">Histórias reais de transformação e superação</p>
    </div>

    <div class="row">
        {% for depoimento in depoimentos %}
        <div class="col-lg-6 mb-4">
            <div class="card h-100 testimonial-card shadow-sm border-0">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center mb-3">
                        <div class="feature-icon" style="width: 50px; height: 50px;">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="ms-3">
                            <h5 class="fw-bold mb-1">{{ depoimento.nome }}</h5>
                            <p class="text-muted mb-0">{{ depoimento.idade }} anos  {{ depoimento.tempo_academia }} na academia</p>
                        </div>
                    </div>
                    
                    <div class="text-warning mb-3">
                        {% for i in range(depoimento.avaliacao) %}
                        <i class="fas fa-star"></i>
                        {% endfor %}
                    </div>
                    
                    <p class="card-text fst-italic">"{{ depoimento.texto }}"</p>
                    
                    <div class="mt-3 pt-3 border-top">
                        <small class="text-muted">
                            <i class="fas fa-briefcase me-1"></i>{{ depoimento.profissao }}
                        </small>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Stats Section -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="card bg-primary text-white">
                <div class="card-body p-5 text-center">
                    <h3 class="mb-4">Junte-se aos nossos mais de 2.000 alunos satisfeitos</h3>
                    <p class="lead mb-4">98% dos nossos alunos recomendam a SamuFit para amigos e familiares</p>
                    <a href="/contato" class="btn btn-light btn-lg px-5">Comece sua jornada hoje</a>
                </div>
            </div>
        </div>
    </div>
</div>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Depoimentos - SamuFit Academia')

CONTATO_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8">
            <h1 class="display-4 fw-bold mb-4">Entre em Contato</h1>
            <p class="lead mb-4">Estamos aqui para responder todas as suas dúvidas e ajudar a começar sua jornada fitness</p>

            <div class="contact-form">
                <form method="POST" action="/contato">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nome" class="form-label fw-bold">Nome Completo *</label>
                            <input type="text" class="form-control form-control-lg" id="nome" name="nome" required placeholder="Seu nome completo">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label fw-bold">E-mail *</label>
                            <input type="email" class="form-control form-control-lg" id="email" name="email" required placeholder="seu@email.com">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="telefone" class="form-label fw-bold">Telefone *</label>
                        <input type="tel" class="form-control form-control-lg" id="telefone" name="telefone" required placeholder="(99) 99999-9999">
                    </div>
                    <div class="mb-3">
                        <label for="assunto" class="form-label fw-bold">Assunto *</label>
                        <select class="form-select form-select-lg" id="assunto" name="assunto" required>
                            <option value="">Selecione o assunto...</option>
                            <option value="orcamento">Solicitar Orçamento</option>
                            <option value="agendamento">Agendar Visita</option>
                            <option value="duvida">Tirar Dúvidas</option>
                            <option value="reclamacao">Reclamação</option>
                            <option value="sugestao">Sugestão</option>
                            <option value="outro">Outro</option>
                        </select>
                    </div>
                    <div class="mb-4">
                        <label for="mensagem" class="form-label fw-bold">Mensagem *</label>
                        <textarea class="form-control form-control-lg" id="mensagem" name="mensagem" rows="5" required placeholder="Descreva sua mensagem..."></textarea>
                    </div>
                    <div class="mb-4">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="newsletter" name="newsletter" checked>
                            <label class="form-check-label" for="newsletter">
                                Desejo receber novidades e promoções da SamuFit
                            </label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg w-100 py-3">
                        <i class="fas fa-paper-plane me-2"></i>Enviar Mensagem
                    </button>
                </form>
            </div>
        </div>
        
        <div class="col-lg-4">
            <!-- Contact Info -->
            <div class="card shadow-sm border-0 mb-4">
                <div class="card-body p-4">
                    <h5 class="card-title fw-bold mb-4">
                        <i class="fas fa-info-circle text-primary me-2"></i>Informações de Contato
                    </h5>
                    <div class="mb-3">
                        <i class="fas fa-map-marker-alt text-primary me-2"></i>
                        <strong>Endereço:</strong><br>
                        <span class="ms-4">Rua das Academias, 123<br>Centro, Timon - MA<br>CEP: 01234-567</span>
                    </div>
                    <div class="mb-3">
                        <i class="fas fa-phone text-primary me-2"></i>
                        <strong>Telefone:</strong><br>
                        <span class="ms-4">(99) 9999-9999</span>
                    </div>
                    <div class="mb-3">
                        <i class="fas fa-envelope text-primary me-2"></i>
                        <strong>E-mail:</strong><br>
                        <span class="ms-4">contato@samufit.com</span>
                    </div>
                    <div class="mb-3">
                        <i class="fas fa-clock text-primary me-2"></i>
                        <strong>Horário de Funcionamento:</strong><br>
                        <span class="ms-4">
                            Segunda a Sexta: 5h às 23h<br>
                            Sábado: 6h às 20h<br>
                            Domingo: 8h às 18h
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="card shadow-sm border-0">
                <div class="card-body p-4">
                    <h5 class="card-title fw-bold mb-4">
                        <i class="fas fa-bolt text-primary me-2"></i>Ações Rápidas
                    </h5>
                    <div class="d-grid gap-2">
                        <a href="/planos" class="btn btn-outline-primary btn-lg">
                            <i class="fas fa-crown me-2"></i>Ver Planos
                        </a>
                        <a href="/horarios" class="btn btn-outline-primary btn-lg">
                            <i class="fas fa-clock me-2"></i>Ver Horários
                        </a>
                        <a href="/agendamento" class="btn btn-outline-primary btn-lg">
                            <i class="fas fa-calendar me-2"></i>Agendar Aula Experimental
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Contato - SamuFit Academia')

AGENDAMENTO_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <h1 class="display-4 fw-bold text-center mb-4">Agende sua Aula Experimental</h1>
            <p class="lead text-center mb-5">Experimente nossa academia gratuitamente e descubra como podemos ajudar você a alcançar seus objetivos</p>

            <div class="contact-form">
                <form method="POST" action="/agendamento">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nome" class="form-label fw-bold">Nome Completo *</label>
                            <input type="text" class="form-control form-control-lg" id="nome" name="nome" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label fw-bold">E-mail *</label>
                            <input type="email" class="form-control form-control-lg" id="email" name="email" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="telefone" class="form-label fw-bold">Telefone *</label>
                        <input type="tel" class="form-control form-control-lg" id="telefone" name="telefone" required>
                    </div>
                    <div class="mb-3">
                        <label for="modalidade" class="form-label fw-bold">Modalidade de Interesse *</label>
                        <select class="form-select form-select-lg" id="modalidade" name="modalidade" required>
                            <option value="">Selecione uma modalidade...</option>
                            <option value="musculacao">Musculação</option>
                            <option value="crossfit">Cross Training</option>
                            <option value="funcional">Funcional</option>
                            <option value="spinning">Spinning</option>
                            <option value="yoga">Yoga</option>
                            <option value="pilates">Pilates</option>
                            <option value="boxe">Boxe</option>
                        </select>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="data" class="form-label fw-bold">Data Preferencial *</label>
                            <input type="date" class="form-control form-control-lg" id="data" name="data" required min="{{ now }}">
                        </div>
                        <div class="col-md-6 mb-4">
                            <label for="horario" class="form-label fw-bold">Horário Preferencial *</label>
                            <select class="form-select form-select-lg" id="horario" name="horario" required>
                                <option value="">Selecione um horário...</option>
                                <option value="manha">Manhã (6h - 12h)</option>
                                <option value="tarde">Tarde (12h - 18h)</option>
                                <option value="noite">Noite (18h - 22h)</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-4">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="newsletter" name="newsletter" checked>
                            <label class="form-check-label" for="newsletter">
                                Desejo receber novidades e promoções da SamuFit
                            </label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg w-100 py-3">
                        <i class="fas fa-calendar-check me-2"></i>Agendar Aula Experimental
                    </button>
                </form>
            </div>

            <!-- Benefits -->
            <div class="row mt-5">
                <div class="col-12">
                    <div class="card bg-light border-0">
                        <div class="card-body p-4">
                            <h5 class="text-center mb-4">Benefícios da Aula Experimental</h5>
                            <div class="row text-center">
                                <div class="col-md-4 mb-3">
                                    <i class="fas fa-dumbbell fa-2x text-primary mb-2"></i>
                                    <h6>Equipamentos</h6>
                                    <small class="text-muted">Teste nossos equipamentos de última geração</small>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <i class="fas fa-user-md fa-2x text-primary mb-2"></i>
                                    <h6>Avaliação</h6>
                                    <small class="text-muted">Avaliação física com profissional especializado</small>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <i class="fas fa-map fa-2x text-primary mb-2"></i>
                                    <h6>Tour Guiado</h6>
                                    <small class="text-muted">Conheça toda a estrutura da academia</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.getElementById('data').min = new Date().toISOString().split('T')[0];
</script>
''').replace('{% block title %}SamuFit Academia{% endblock %}', 'Agendamento - SamuFit Academia')

# =============================================
# ROTAS DA APLICAÇÃO
# =============================================

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/planos')
def planos():
    return render_template_string(PLANOS_TEMPLATE, planos=PLANOS)

@app.route('/horarios')
def horarios():
    return render_template_string(HORARIOS_TEMPLATE, horarios=HORARIOS, modalidades=MODALIDADES)

@app.route('/modalidades')
def modalidades():
    return render_template_string(MODALIDADES_TEMPLATE, modalidades=MODALIDADES)

@app.route('/galeria')
def galeria():
    return render_template_string(GALERIA_TEMPLATE)

@app.route('/depoimentos')
def depoimentos():
    return render_template_string(DEPOIMENTOS_TEMPLATE, depoimentos=DEPOIMENTOS)

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')
        newsletter = request.form.get('newsletter')
        
        if not all([nome, email, telefone, assunto, mensagem]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return render_template_string(CONTATO_TEMPLATE)
        
        # Simular salvamento
        contato_data = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'assunto': assunto,
            'mensagem': mensagem,
            'newsletter': bool(newsletter),
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        print(f"?? NOVO CONTATO: {contato_data}")
        
        flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('contato'))
    
    return render_template_string(CONTATO_TEMPLATE)

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        modalidade = request.form.get('modalidade')
        data = request.form.get('data')
        horario = request.form.get('horario')
        
        if not all([nome, email, telefone, modalidade, data, horario]):
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template_string(AGENDAMENTO_TEMPLATE, now=datetime.now().strftime('%Y-%m-%d'))
        
        # Simular agendamento
        agendamento_data = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'modalidade': modalidade,
            'data': data,
            'horario': horario,
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        print(f"?? NOVO AGENDAMENTO: {agendamento_data}")
        
        flash('Agendamento realizado com sucesso! Enviaremos uma confirmação por email.', 'success')
        return redirect(url_for('agendamento'))
    
    return render_template_string(AGENDAMENTO_TEMPLATE, now=datetime.now().strftime('%Y-%m-%d'))

# =============================================
# INICIALIZAÇÃO DA APLICAÇÃO
# =============================================

if __name__ == '__main__':
    print("=" * 70)
    print("??????  SITE DA ACADEMIA SAMUFIT - INICIANDO")
    print("=" * 70)
    print("?? Dados carregados:")
    print(f"    {len(PLANOS)} planos disponíveis")
    print(f"    {len(HORARIOS)} modalidades com horários")
    print(f"    {len(DEPOIMENTOS)} depoimentos de alunos")
    print(f"    {len(MODALIDADES)} modalidades oferecidas")
    print("=" * 70)
    print("?? Servidor iniciando...")
    print("?? Acesse: http://localhost:5000")
    print("\n?? Páginas disponíveis:")
    print("   /              - Página Inicial")
    print("   /planos        - Planos e Preços")
    print("   /horarios      - Horários das Aulas")
    print("   /modalidades   - Modalidades Oferecidas")
    print("   /galeria       - Galeria de Fotos")
    print("   /depoimentos   - Depoimentos de Alunos")
    print("   /contato       - Página de Contato")
    print("   /agendamento   - Agendamento de Aula Experimental")
    print("=" * 70)
    print("? Desenvolvido com Flask - Um único arquivo Python!")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    from pyngrok import ngrok

if __name__ == '__main__':
    # Iniciar túnel ngrok
    public_url = ngrok.connect(5000)
    print(f"?? Site disponível publicamente em: {public_url}")
    print("?? Compartilhe este link com qualquer pessoa!")
    
    app.run(debug=False, host='0.0.0.0', port=5000)