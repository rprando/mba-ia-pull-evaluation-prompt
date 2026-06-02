"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture
def prompt_data():
    """Fixture que carrega os dados do prompt v2 para os testes."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
    return load_prompts(str(prompt_path))

def get_system_prompt(prompt_data):
    """Função auxiliar para extrair o conteúdo do system_prompt."""
    for msg in prompt_data.get('messages', []):
        if msg.get('type') == 'system':
            return msg.get('content', '')
    return ''

class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' (dentro de messages) existe e não está vazio."""
        system_prompt = get_system_prompt(prompt_data)
        assert system_prompt != "", "O system prompt não foi encontrado ou está vazio."

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = get_system_prompt(prompt_data)
        assert "Você é um Engenheiro de Requisitos" in system_prompt or "Product Manager" in system_prompt, \
            "Persona não definida no prompt."

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = get_system_prompt(prompt_data)
        assert "User Story" in system_prompt or "BDD" in system_prompt, \
            "O prompt não menciona o formato de User Story ou BDD."

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = get_system_prompt(prompt_data)
        # O nosso prompt v2 usa a tag [CENÁRIO para os exemplos
        assert "[CENÁRIO" in system_prompt or "Entrada:" in system_prompt, \
            "O prompt não contém os exemplos de Few-Shot Learning."

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = get_system_prompt(prompt_data)
        assert "[TODO]" not in system_prompt, "Ainda existem marcadores [TODO] no texto do prompt."

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get('metadata', {}).get('techniques_applied', [])
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])