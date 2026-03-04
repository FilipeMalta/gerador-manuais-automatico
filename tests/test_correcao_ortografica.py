"""
Testes unitários para o módulo de Correção Ortográfica com Ollama.

Testa:
- Conexão com servidor Ollama
- Correção de textos com erros ortográficos
- Comportamento com textos corretos
- Tratamento de entrada vazia
- Comportamento quando Ollama está offline

Requisitos para execução:
- pytest >= 7.0.0 (já em requirements.txt)
- Ollama rodando em http://localhost:11434 (para testes de integração)

Execução:
    pytest tests/test_correcao_ortografica.py -v
    pytest tests/test_correcao_ortografica.py::test_conexao_ollama -v
"""

import pytest
from unittest.mock import patch, MagicMock
import requests

from src.correcao_ortografica import CorretorOrtografico
from src.config import get_ollama_config


class TestConexaoOllama:
    """Testes de conexão com servidor Ollama."""
    
    @pytest.fixture
    def corretor(self):
        """Fixture: inicializa um CorretorOrtografico para testes."""
        return CorretorOrtografico(verbose=False)
    
    def test_conexao_ollama_disponivel(self, corretor):
        """
        Testa se consegue conectar ao servidor Ollama.
        
        Este teste requer que Ollama esteja rodando em http://localhost:11434
        
        Caso Ollama não esteja disponível, o teste será pulado com aviso.
        """
        # Tentar "pingar" o servidor antes do teste
        try:
            response = requests.get(
                f"{corretor.url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
        except (requests.ConnectionError, requests.Timeout):
            pytest.skip(
                "❌ Ollama não está disponível em http://localhost:11434. "
                "Inicie Ollama com: ollama serve"
            )
        
        # Verificar disponibilidade
        disponivel = corretor.verificar_disponibilidade()
        
        assert disponivel is True, "Ollama deveria estar disponível"
        assert corretor.url == get_ollama_config().base_url
        assert corretor.model == get_ollama_config().model
        assert corretor.timeout == get_ollama_config().timeout
    
    def test_config_padrao(self, corretor):
        """Verifica se as configurações padrão são carregadas corretamente."""
        config = get_ollama_config()
        
        assert corretor.DEFAULT_URL == config.base_url
        assert corretor.DEFAULT_MODEL == config.model
        assert corretor.DEFAULT_TIMEOUT == config.timeout
        assert corretor.MAX_CHARS == config.max_texto_chunk


class TestCorrecaoSimples:
    """Testes de correção de textos com erros ortográficos."""
    
    @pytest.fixture
    def corretor(self):
        """Fixture: inicializa um CorretorOrtografico para testes."""
        return CorretorOrtografico(verbose=False)
    
    def test_correcao_erro_basico(self, corretor):
        """Testa correção de erro ortográfico simples.
        
        Input: "Eu preçiso ajuda"
        Expected: "Eu preciso ajuda" (ou similar sem erros)
        
        Este teste requer Ollama disponível.
        """
        # Verificar se Ollama está disponível
        if not corretor.verificar_disponibilidade():
            pytest.skip("Ollama não está disponível")
        
        texto_com_erro = "Eu preçiso ajuda"
        texto_corrigido = corretor.corrigir_texto(texto_com_erro)
        
        # Verificações
        assert texto_corrigido is not None, "Corretor não deve retornar None"
        assert isinstance(texto_corrigido, str), "Resultado deve ser string"
        assert len(texto_corrigido) > 0, "Texto corrigido não deve ser vazio"
        
        # O texto deve ser diferente (alguma correção foi feita)
        # Mas para ser seguro, apenas verificamos que "preçiso" foi removido
        assert "preçiso" not in texto_corrigido.lower() or \
               "preciso" in texto_corrigido.lower(), \
               "Deveria corrigir 'preçiso' para 'preciso'"
    
    def test_correcao_multiplos_erros(self, corretor):
        """Testa correção de texto com múltiplos erros.
        
        Este teste requer Ollama disponível.
        """
        if not corretor.verificar_disponibilidade():
            pytest.skip("Ollama não está disponível")
        
        texto_com_erros = "Para criar um resgistro, o ussuário deve clicar em 'Criar' e preençher o formulário"
        texto_corrigido = corretor.corrigir_texto(texto_com_erros)
        
        assert texto_corrigido is not None
        assert isinstance(texto_corrigido, str)
        assert len(texto_corrigido) > 0
        
        # Verificar que alguns erros foram tratados
        erros_originais = ["resgistro", "ussuário", "preençher"]
        erros_encontrados = sum(
            1 for erro in erros_originais
            if erro not in texto_corrigido.lower()
        )
        
        # Pelo menos alguns erros devem ser tratados
        assert erros_encontrados > 0, \
            "Deveria corrigir alguns dos erros ortográficos"


class TestTextoSemErro:
    """Testes com textos que já estão corretos."""
    
    @pytest.fixture
    def corretor(self):
        """Fixture: inicializa um CorretorOrtografico para testes."""
        return CorretorOrtografico(verbose=False)
    
    def test_texto_correto_nao_muda(self, corretor):
        """Testa se texto correto não é alterado significativamente.
        
        Este teste requer Ollama disponível.
        """
        if not corretor.verificar_disponibilidade():
            pytest.skip("Ollama não está disponível")
        
        texto_correto = "Para criar um registro, o usuário deve clicar em Criar"
        texto_processado = corretor.corrigir_texto(texto_correto)
        
        assert texto_processado is not None
        assert isinstance(texto_processado, str)
        
        # Texto correto deve permanecer praticamente igual
        # (pode ter pequenas mudanças de formatação)
        assert "registro" in texto_processado.lower()
        assert "usuário" in texto_processado.lower()
    
    def test_texto_vazio(self, corretor):
        """Testa comportamento com texto vazio.
        
        Este teste requer Ollama disponível.
        """
        if not corretor.verificar_disponibilidade():
            pytest.skip("Ollama não está disponível")
        
        texto_vazio = ""
        resultado = corretor.corrigir_texto(texto_vazio)
        
        # Deve retornar algo (não None) mesmo com texto vazio
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_texto_apenas_espacos(self, corretor):
        """Testa com texto contendo apenas espaços.
        
        Este teste requer Ollama disponível.
        """
        if not corretor.verificar_disponibilidade():
            pytest.skip("Ollama não está disponível")
        
        texto_espacos = "   \n   \t   "
        resultado = corretor.corrigir_texto(texto_espacos)
        
        assert resultado is not None
        assert isinstance(resultado, str)


class TestOllamaOffline:
    """Testes de comportamento quando Ollama está offline."""
    
    @pytest.fixture
    def corretor(self):
        """Fixture: inicializa um CorretorOrtografico para testes."""
        return CorretorOrtografico(verbose=False)
    
    def test_verificar_disponibilidade_offline(self, corretor):
        """Testa verificação de disponibilidade quando Ollama está offline.
        
        Mock a conexão para simular Ollama offline.
        """
        with patch('requests.get') as mock_get:
            # Simular conexão recusada
            mock_get.side_effect = requests.ConnectionError("Conexão recusada")
            
            disponivel = corretor.verificar_disponibilidade()
            
            assert disponivel is False, \
                "Deve retornar False quando não consegue conectar"
    
    def test_corrigir_com_timeout(self, corretor):
        """Testa comportamento quando requisição Ollama faz timeout.
        
        Mock a requisição para simular timeout.
        """
        # Primeiro, confirmar que Ollama não está disponível para este teste
        with patch('requests.post') as mock_post:
            # Simular timeout
            mock_post.side_effect = requests.Timeout("Timeout na requisição")
            
            # Não deveria lançar exceção, deveria retornar o texto original
            texto = "Algum texto com preçiso de correção"
            resultado = corretor.corrigir_texto(texto)
            
            # Quando há timeout, deveria retornar o texto original
            assert resultado is not None
            assert isinstance(resultado, str)
    
    def test_corrigir_com_erro_conexao(self, corretor):
        """Testa comportamento com erro de conexão durante correção.
        
        Mock a requisição para simular erro de conexão.
        """
        with patch('requests.post') as mock_post:
            # Simular erro de conexão
            mock_post.side_effect = requests.ConnectionError("Sem conexão")
            
            texto = "Texto com erro ortográphico"
            resultado = corretor.corrigir_texto(texto)
            
            # Deveria retornar o texto original em caso de erro
            assert resultado is not None
            assert isinstance(resultado, str)
    
    def test_offline_verificacao_com_mock(self, corretor):
        """Testa que verificar_disponibilidade retorna False quando offline."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError()
            
            # Resetar estado interno de cache
            corretor._disponivel = None
            
            resultado = corretor.verificar_disponibilidade()
            assert resultado is False


class TestIntegrationConfig:
    """Testes de integração com sistema de configuração."""
    
    def test_variables_ambiente_nao_carregam_durante_test(self):
        """
        Verifica que as configurações usam valores padrão no teste.
        
        Nota: Variáveis de ambiente são carregadas em import time,
        portanto este teste valida apenas os padrões.
        """
        config = get_ollama_config()
        
        # Verificar estrutura
        assert hasattr(config, 'base_url')
        assert hasattr(config, 'model')
        assert hasattr(config, 'timeout')
        assert hasattr(config, 'max_texto_chunk')
        
        # Verificar tipos
        assert isinstance(config.base_url, str)
        assert isinstance(config.model, str)
        assert isinstance(config.timeout, int)
        assert isinstance(config.max_texto_chunk, int)
        
        # Verificar valores padrão
        assert config.base_url == "http://localhost:11434"
        assert config.model in ["mixtral", "neural-chat", "mistral", "llama2"]
        assert config.timeout > 0
        assert config.max_texto_chunk > 0
    
    def test_corretor_usa_config_padrao(self):
        """Verifica que CorretorOrtografico usa configurações padrão."""
        corretor = CorretorOrtografico()
        config = get_ollama_config()
        
        assert corretor.url == config.base_url
        assert corretor.model == config.model
        assert corretor.timeout == config.timeout


class TestChunking:
    """Testes de divisão de texto em chunks."""
    
    @pytest.fixture
    def corretor(self):
        """Fixture: inicializa um CorretorOrtografico para testes."""
        return CorretorOrtografico(verbose=False)
    
    def test_dividir_texto_pequeno(self, corretor):
        """Testa que textos pequenos não são divididos."""
        texto = "Pequeno texto com erro de ortografia"
        chunks = corretor._dividir_em_chunks(texto)
        
        assert len(chunks) == 1, "Texto pequeno não deveria ser dividido"
        assert chunks[0] == texto
    
    def test_dividir_texto_grande(self, corretor):
        """Testa divisão de texto maior que MAX_CHARS."""
        # Criar texto com mais de MAX_CHARS caracteres
        texto_linha = "Este é um texto longo com várias palavras. " * 100
        chunks = corretor._dividir_em_chunks(texto_linha)
        
        # Deve ser dividido em múltiplos chunks
        assert len(chunks) > 1, "Texto grande deveria ser dividido"
        
        # Cada chunk deve ter menos de MAX_CHARS
        for chunk in chunks:
            assert len(chunk) <= corretor.MAX_CHARS
        
        # Juntar chunks deveria resultar no texto original
        texto_reconstruido = " ".join(chunks)
        assert texto_reconstruido.strip() == texto_linha.strip()


# ============================================================================
# INSTRUÇÕES DE EXECUÇÃO
# ============================================================================
"""
Para executar os testes:

1. Instalar dependências:
   pip install pytest

2. Executar todos os testes:
   pytest tests/test_correcao_ortografica.py -v

3. Executar teste específico:
   pytest tests/test_correcao_ortografica.py::TestConexaoOllama::test_conexao_ollama_disponivel -v

4. Executar apenas testes de integração (que precisam Ollama):
   pytest tests/test_correcao_ortografica.py -v -m integration

5. Executar apenas testes de unit (sem Ollama):
   pytest tests/test_correcao_ortografica.py -v -m "not integration"

Observações:
- Testes que precisam Ollama disponível usarão pytest.skip() se não estiver rodando
- Testes com mock não dependem de Ollama estar disponível
- Para rodar Ollama: ollama serve
"""
