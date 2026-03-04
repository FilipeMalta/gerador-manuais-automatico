"""
Módulo de Correção Ortográfica com Ollama (Otimizado)

Fornece correção ortográfica e gramatical em tempo real usando:
- LLM local (Ollama) - modo primário
- pyspellchecker - fallback se Ollama indisponível

Otimizações Implementadas:
- Cache LRU (até 100 correções) - não repete o mesmo texto
- Detecção inteligente (pula textos curtos/bons)
- Fallback automático a pyspellchecker
- Estatísticas de performance
- Compatibilidade total com código existente

Uso:
    corretor = CorretorOrtografico()
    if corretor.verificar_disponibilidade():
        texto_corrigido = corretor.corrigir_texto("tesste de ortografia")
        stats = corretor.obter_estatisticas()
        print(f"Cache hits: {stats['cache_hits']}")
"""

import requests
import time
from typing import Optional, Tuple, Dict
from pathlib import Path
from functools import lru_cache
from statistics import mean

# Importar configurações centralizadas
from .config import get_ollama_config
from .logger import get_logger

# Tentar importar pyspellchecker (fallback)
try:
    from spellchecker import SpellChecker
    SPELLCHECKER_DISPONIVEL = True
except ImportError:
    SPELLCHECKER_DISPONIVEL = False

# Logger para este módulo
logger = get_logger(__name__)


class CorretorOrtografico:
    """
    Corretor ortográfico otimizado com cache LRU e fallback.
    
    Otimizações:
    - Cache LRU: até 100 últimas correções (não repete)
    - Detecção inteligente: pula textos curtos ou muito bons
    - Fallback: usa pyspellchecker se Ollama falhar
    - Estatísticas: rastreia performance
    """
    
    # Configurações centralizadas
    _config = get_ollama_config()
    DEFAULT_URL = _config.base_url
    DEFAULT_MODEL = _config.model
    DEFAULT_TIMEOUT = _config.timeout
    MAX_CHARS = _config.max_texto_chunk
    DEFAULT_CACHE_SIZE = 100
    
    def __init__(
        self,
        url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        verbose: bool = False,
        cache_size: int = DEFAULT_CACHE_SIZE,
    ):
        """Inicializar Protetor com cache LRU."""
        self.url = url or self.DEFAULT_URL
        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.verbose = verbose
        self.cache_size = cache_size
        self._disponivel: Optional[bool] = None
        
        # Estatísticas
        self.stats: Dict[str, any] = {
            "cache_hits": 0,
            "cache_misses": 0,
            "texto_pulado": 0,
            "fallback_usado": 0,
            "tempos": [],
        }
        
        # Decorator lru_cache
        self._corrigir_texto_cached = lru_cache(maxsize=cache_size)(
            self._corrigir_texto_impl
        )
        
        # SpellChecker fallback
        self.spell_checker = None
        if SPELLCHECKER_DISPONIVEL:
            try:
                self.spell_checker = SpellChecker(language='pt')
                logger.info("pyspellchecker carregado para fallback")
            except Exception as e:
                logger.warning(f"Erro ao inicializar pyspellchecker: {e}")
        
        logger.info(
            f"CorretorOrtografico | modelo={self.model} | cache={cache_size} | "
            f"fallback={'✓' if self.spell_checker else '✗'}"
        )
    
    def verificar_disponibilidade(self) -> bool:
        """Verifica se Ollama está disponível."""
        try:
            logger.info(f"Verificando {self.url}")
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                model_names = [m.get('name', '') for m in models]
                
                self._disponivel = any(self.model in m for m in model_names)
                
                if self._disponivel:
                    logger.info(f"✅ Ollama online (modelo: {self.model})")
                else:
                    logger.warning(f"⚠️ Modelo '{self.model}' não encontrado")
                
                return self._disponivel
            else:
                logger.error(f"HTTP {response.status_code}")
                self._disponivel = False
                return False
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ Conexão recusada (Ollama não está rodando)")
            self._disponivel = False
            return False
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            self._disponivel = False
            return False
    
    def _precisa_corrigir(self, texto: str) -> bool:
        """
        Detecta se texto realmente precisa de correção.
        
        Pula:
        - Textos muito curtos (< 10 chars)
        - Textos muito curtos (< 3 palavras)
        - Textos com >90% de precisão (muitas palavras válidas)
        """
        if not texto or len(texto) < 10:
            self.stats["texto_pulado"] += 1
            return False
        
        palavras = texto.split()
        
        if len(palavras) < 3:
            self.stats["texto_pulado"] += 1
            return False
        
        # Se temos spell checker, verificar taxa de erro
        if self.spell_checker:
            erros = self.spell_checker.unknown(palavras)
            taxa_erros = len(erros) / len(palavras)
            
            if taxa_erros < 0.1:  # < 10% de erro = >90% certo
                self.stats["texto_pulado"] += 1
                return False
        
        return True
    
    def _corrigir_fallback(self, texto: str) -> str:
        """Fallback com pyspellchecker."""
        if not self.spell_checker:
            return texto
        
        try:
            logger.info("Usando fallback (pyspellchecker)")
            palavras = texto.split()
            palavras_corrigidas = []
            
            for palavra in palavras:
                if self.spell_checker.unknown([palavra]):
                    corrigida = self.spell_checker.correction(palavra)
                    palavras_corrigidas.append(corrigida or palavra)
                else:
                    palavras_corrigidas.append(palavra)
            
            self.stats["fallback_usado"] += 1
            return ' '.join(palavras_corrigidas)
            
        except Exception as e:
            logger.error(f"Erro fallback: {e}")
            return texto
    
    def _dividir_em_chunks(self, texto: str) -> list:
        """Divide texto em chunks se > MAX_CHARS."""
        if len(texto) <= self.MAX_CHARS:
            return [texto]
        
        chunks = []
        paragrafo_atual = []
        chars_atuais = 0
        
        for paragrafo in texto.split('\n'):
            # Se um parágrafo sozinho é muito grande, dividi-lo por sentenças
            if len(paragrafo) > self.MAX_CHARS:
                # Primeiro, salvar paragrafo_atual
                if paragrafo_atual:
                    chunks.append('\n'.join(paragrafo_atual))
                    paragrafo_atual = []
                    chars_atuais = 0
                
                # Agora dividir o parágrafo grande em chunks menores
                sentencas = paragrafo.split('. ')
                chunk_temp = []
                chars_temp = 0
                
                for sentenca in sentencas:
                    if chars_temp + len(sentenca) + 2 > self.MAX_CHARS:  # +2 para ". "
                        if chunk_temp:
                            chunks.append('. '.join(chunk_temp) + '.')
                            chunk_temp = [sentenca]
                            chars_temp = len(sentenca)
                        else:
                            chunks.append(sentenca)
                            chars_temp = 0
                    else:
                        chunk_temp.append(sentenca)
                        chars_temp += len(sentenca) + 2
                
                if chunk_temp:
                    chunks.append('. '.join(chunk_temp))
            
            elif chars_atuais + len(paragrafo) > self.MAX_CHARS:
                if paragrafo_atual:
                    chunks.append('\n'.join(paragrafo_atual))
                    paragrafo_atual = [paragrafo]
                    chars_atuais = len(paragrafo)
                else:
                    chunks.append(paragrafo)
                    chars_atuais = 0
            else:
                paragrafo_atual.append(paragrafo)
                chars_atuais += len(paragrafo) + 1
        
        if paragrafo_atual:
            chunks.append('\n'.join(paragrafo_atual))
        
        return chunks
    
    def _corrigir_chunk(self, chunk: str) -> str:
        """Corrige um chunk via Ollama."""
        prompt = (
            "Corrija apenas os erros ortográficos e gramaticais do seguinte "
            "texto em português, mantendo o sentido original. Retorne apenas "
            "o texto corrigido sem explicações:\n\n" + chunk
        )
        
        try:
            tamanho = len(chunk)
            logger.info(f"Enviando {tamanho} chars para {self.model}")
            
            tempo_inicio = time.time()
            
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,
                },
                timeout=self.timeout
            )
            
            tempo_decorrido = time.time() - tempo_inicio
            
            if response.status_code == 200:
                resultado = response.json()
                texto_corrigido = resultado.get('response', '').strip()
                
                # Limpar prefixos comuns
                for prefixo in ["Texto corrigido:", "Corrigido:", "Corrigido"]:
                    if texto_corrigido.startswith(prefixo):
                        texto_corrigido = texto_corrigido[len(prefixo):].strip()
                        break
                
                logger.info(
                    f"✅ Chunk corrigido | tempo={tempo_decorrido:.2f}s | "
                    f"modelo={self.model} | chars={tamanho}"
                )
                return texto_corrigido
            else:
                logger.error(f"Erro HTTP {response.status_code}")
                return chunk
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ({self.timeout}s)")
            return chunk
        except requests.exceptions.ConnectionError:
            logger.error("Conexão perdida com Ollama")
            return chunk
        except Exception as e:
            logger.error(f"Erro: {e}")
            return chunk
    
    def _corrigir_texto_impl(self, texto: str) -> str:
        """Implementação real (decorada com lru_cache)."""
        if not self._precisa_corrigir(texto):
            return texto
        
        # Verificar Ollama
        if self._disponivel is None:
            if not self.verificar_disponibilidade():
                logger.info("Ollama indisponível, try fallback")
                return self._corrigir_fallback(texto)
        elif not self._disponivel:
            return self._corrigir_fallback(texto)
        
        # Processar chunks
        chunks = self._dividir_em_chunks(texto)
        
        if len(chunks) > 1:
            logger.info(f"Texto dividido em {len(chunks)} chunks")
        
        resultado = []
        for idx, chunk in enumerate(chunks):
            resultado.append(self._corrigir_chunk(chunk))
            if len(chunks) > 1:
                logger.info(f"Chunk {idx + 1}/{len(chunks)} ok")
        
        return '\n'.join(resultado)
    
    def corrigir_texto(self, texto: str) -> str:
        """
        Corrige texto com cache LRU.
        
        Interface pública - mantém compatibilidade.
        Usa cache para não corrigir o mesmo texto duas vezes.
        """
        tempo_inicio = time.time()
        
        try:
            resultado = self._corrigir_texto_cached(texto)
            tempo_decorrido = time.time() - tempo_inicio
            
            cache_info = self._corrigir_texto_cached.cache_info()
            
            if tempo_decorrido < 0.05:  # < 50ms = provavelmente cache hit
                self.stats["cache_hits"] += 1
                logger.info(
                    f"Cache hit! {tempo_decorrido*1000:.0f}ms | "
                    f"hits={cache_info.hits} | size={cache_info.currsize}/{self.cache_size}"
                )
            else:
                self.stats["cache_misses"] += 1
                self.stats["tempos"].append(tempo_decorrido)
            
            return resultado
        
        except Exception as e:
            logger.error(f"Erro: {e}")
            return texto
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas de performance."""
        cache_info = self._corrigir_texto_cached.cache_info()
        tempo_medio = mean(self.stats["tempos"]) if self.stats["tempos"] else 0
        
        return {
            "cache_enabled": True,
            "cache_size_max": self.cache_size,
            "cache_size_atual": cache_info.currsize,
            "cache_hits": cache_info.hits,
            "cache_misses": cache_info.misses,
            "taxa_acerto": (
                cache_info.hits / (cache_info.hits + cache_info.misses)
                if (cache_info.hits + cache_info.misses) > 0 else 0
            ),
            "fallback_disponivel": self.spell_checker is not None,
            "fallback_usado": self.stats["fallback_usado"],
            "texto_pulado": self.stats["texto_pulado"],
            "tempo_medio_ms": tempo_medio * 1000,
            "tempo_min_ms": min(self.stats["tempos"]) * 1000 if self.stats["tempos"] else 0,
            "tempo_max_ms": max(self.stats["tempos"]) * 1000 if self.stats["tempos"] else 0,
        }
    
    def limpar_cache(self) -> None:
        """Limpa o cache LRU."""
        self._corrigir_texto_cached.cache_clear()
        logger.info("Cache LRU limpo")
    
    def corrigir_arquivo(self, caminho_arquivo: str) -> Tuple[bool, str]:
        """Corrige um arquivo de texto inteiro."""
        try:
            arquivo = Path(caminho_arquivo)
            
            if not arquivo.exists():
                return False, f"Arquivo não encontrado: {caminho_arquivo}"
            
            if arquivo.suffix.lower() != '.txt':
                return False, "Apenas .txt suportado"
            
            logger.info(f"Lendo: {caminho_arquivo}")
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            conteudo_corrigido = self.corrigir_texto(conteudo)
            
            return True, conteudo_corrigido
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            return False, str(e)
    
    def corrigir_e_salvar(
        self,
        caminho_entrada: str,
        caminho_saida: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Corrige arquivo e salva o resultado."""
        sucesso, resultado = self.corrigir_arquivo(caminho_entrada)
        
        if not sucesso:
            return False, resultado
        
        try:
            if caminho_saida is None:
                entrada = Path(caminho_entrada)
                caminho_saida = entrada.parent / (entrada.stem + "_corrigido.txt")
            
            saida = Path(caminho_saida)
            logger.info(f"Salvando: {caminho_saida}")
            
            with open(saida, 'w', encoding='utf-8') as f:
                f.write(resultado)
            
            return True, f"Arquivo salvo: {caminho_saida}"
            
        except Exception as e:
            logger.error(f"Erro ao salvar: {e}")
            return False, str(e)
