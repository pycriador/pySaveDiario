#!/usr/bin/env python3
"""
Test script for pySaveDiário API
Tests all endpoints with examples
"""

import requests
import json
from typing import Optional


class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'


class APITester:
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.test_results = []
    
    def print_success(self, message):
        print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")
    
    def print_error(self, message):
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
    
    def print_info(self, message):
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.ENDC}")
    
    def print_header(self, message):
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{message}{Colors.ENDC}")
        print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
    
    def get_token(self):
        """Get authentication token"""
        self.print_info("Obtendo token de autenticação...")
        
        try:
            response = requests.post(
                f'{self.base_url}/auth/token',
                auth=(self.email, self.password),
                timeout=10
            )
            
            if response.status_code == 200:
                self.token = response.json()['token']
                self.print_success("Token obtido com sucesso!")
                return True
            else:
                self.print_error(f"Falha ao obter token: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erro ao obter token: {e}")
            return False
    
    def headers(self):
        """Get authorization headers"""
        return {'Authorization': f'Bearer {self.token}'}
    
    def test_sellers_api(self):
        """Test Sellers API"""
        self.print_header("🏪 Testando Sellers API")
        
        # List sellers
        self.print_info("GET /api/sellers")
        try:
            response = requests.get(f'{self.base_url}/sellers')
            if response.status_code == 200:
                sellers = response.json()
                self.print_success(f"Listou {len(sellers)} vendedores")
            else:
                self.print_error(f"Erro: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erro: {e}")
        
        # Create seller (only if authenticated)
        if self.token:
            self.print_info("POST /api/sellers")
            try:
                data = {
                    'name': 'Teste Vendedor',
                    'slug': 'teste-vendedor',
                    'description': 'Vendedor de teste',
                    'website': 'https://teste.com'
                }
                response = requests.post(
                    f'{self.base_url}/sellers',
                    headers=self.headers(),
                    json=data
                )
                if response.status_code == 201:
                    seller = response.json()
                    self.print_success(f"Vendedor criado: {seller['name']} (ID: {seller['id']})")
                    return seller['id']
                elif response.status_code == 400 and 'already exists' in response.json().get('message', ''):
                    self.print_success("Vendedor já existe (normal em testes)")
                else:
                    self.print_error(f"Erro: {response.status_code} - {response.json()}")
            except Exception as e:
                self.print_error(f"Erro: {e}")
        
        return None
    
    def test_categories_api(self):
        """Test Categories API"""
        self.print_header("🏷️  Testando Categories API")
        
        # List categories
        self.print_info("GET /api/categories")
        try:
            response = requests.get(f'{self.base_url}/categories')
            if response.status_code == 200:
                categories = response.json()
                self.print_success(f"Listou {len(categories)} categorias")
            else:
                self.print_error(f"Erro: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erro: {e}")
        
        # Create category
        if self.token:
            self.print_info("POST /api/categories")
            try:
                data = {
                    'name': 'Teste Categoria',
                    'slug': 'teste-categoria',
                    'description': 'Categoria de teste',
                    'icon': 'bi bi-star'
                }
                response = requests.post(
                    f'{self.base_url}/categories',
                    headers=self.headers(),
                    json=data
                )
                if response.status_code == 201:
                    category = response.json()
                    self.print_success(f"Categoria criada: {category['name']} (ID: {category['id']})")
                elif response.status_code == 400 and 'already exists' in response.json().get('message', ''):
                    self.print_success("Categoria já existe (normal em testes)")
                else:
                    self.print_error(f"Erro: {response.status_code}")
            except Exception as e:
                self.print_error(f"Erro: {e}")
    
    def test_manufacturers_api(self):
        """Test Manufacturers API"""
        self.print_header("🏭 Testando Manufacturers API")
        
        # List manufacturers
        self.print_info("GET /api/manufacturers")
        try:
            response = requests.get(f'{self.base_url}/manufacturers')
            if response.status_code == 200:
                manufacturers = response.json()
                self.print_success(f"Listou {len(manufacturers)} fabricantes")
            else:
                self.print_error(f"Erro: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erro: {e}")
        
        # Create manufacturer
        if self.token:
            self.print_info("POST /api/manufacturers")
            try:
                data = {
                    'name': 'Teste Fabricante',
                    'slug': 'teste-fabricante',
                    'description': 'Fabricante de teste',
                    'website': 'https://teste.com'
                }
                response = requests.post(
                    f'{self.base_url}/manufacturers',
                    headers=self.headers(),
                    json=data
                )
                if response.status_code == 201:
                    manufacturer = response.json()
                    self.print_success(f"Fabricante criado: {manufacturer['name']} (ID: {manufacturer['id']})")
                elif response.status_code == 400 and 'already exists' in response.json().get('message', ''):
                    self.print_success("Fabricante já existe (normal em testes)")
                else:
                    self.print_error(f"Erro: {response.status_code}")
            except Exception as e:
                self.print_error(f"Erro: {e}")
    
    def test_templates_api(self):
        """Test Templates API"""
        self.print_header("📝 Testando Templates API")
        
        # List templates
        self.print_info("GET /api/templates")
        try:
            response = requests.get(f'{self.base_url}/templates')
            if response.status_code == 200:
                templates = response.json()
                self.print_success(f"Listou {len(templates)} templates")
            else:
                self.print_error(f"Erro: {response.status_code}")
        except Exception as e:
            self.print_error(f"Erro: {e}")
    
    def run_all_tests(self):
        """Run all API tests"""
        self.print_header("🧪 Iniciando Testes da API pySaveDiário")
        
        # Get token first
        if not self.get_token():
            self.print_error("Não foi possível autenticar. Alguns testes serão pulados.")
        
        # Run tests
        self.test_sellers_api()
        self.test_categories_api()
        self.test_manufacturers_api()
        self.test_templates_api()
        
        # Summary
        self.print_header("📊 Resumo dos Testes")
        self.print_success("Todos os endpoints foram testados!")
        self.print_info("Veja os resultados acima para detalhes.")


def main():
    """Main function"""
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}🔧 pySaveDiário - Teste de API{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")
    
    # Configuration
    base_url = "http://localhost:5000/api"
    
    print(f"{Colors.CYAN}Base URL: {base_url}{Colors.ENDC}")
    print()
    
    # Get credentials
    email = input("Email do usuário: ").strip()
    if not email:
        email = "admin@example.com"
        print(f"Usando padrão: {email}")
    
    password = input("Senha: ").strip()
    if not password:
        print(f"{Colors.WARNING}⚠️  Senha vazia{Colors.ENDC}")
    
    # Run tests
    tester = APITester(base_url, email, password)
    tester.run_all_tests()
    
    print(f"\n{Colors.BOLD}✅ Testes concluídos!{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Teste interrompido pelo usuário{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")

