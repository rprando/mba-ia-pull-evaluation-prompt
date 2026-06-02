import os
import sys
import yaml
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

# Carrega as variáveis de ambiente
load_dotenv()

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    try:
        messages = []
        
        # Constrói as mensagens a partir do YAML
        for msg in prompt_data.get('messages', []):
            msg_type = msg.get('type', 'human')
            content = msg.get('content', '')
            
            if msg_type == 'system':
                messages.append(('system', content))
            elif msg_type == 'human':
                messages.append(('human', content))
            elif msg_type == 'ai':
                messages.append(('ai', content))
        
        if not messages:
            print("❌ Nenhuma mensagem encontrada no prompt")
            return False
        
        # Cria o ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        # DEBUG DA CHAVE DE API
        api_key = os.getenv('LANGSMITH_API_KEY')
        print(f"🔍 DEBUG DE REDE E API:")
        print(f"   - A chave carregada tem {len(api_key) if api_key else 0} caracteres.")
        if api_key:
            print(f"   - Início da chave: {api_key[:7]}...")
        
        # Cria cliente do LangSmith forçando a chave explicitamente
        client = Client(api_key=api_key)
        
        # Faz push para o Hub
        print(f"📤 Tentando conectar e fazer push para: {prompt_name}...")
        client.push_prompt(
            prompt_name,
            object=prompt_template
        )
        
        print(f"✅ Prompt '{prompt_name}' publicado com sucesso!")
        print(f"🔗 Visualize em: https://smith.langchain.com/hub/{prompt_name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro crítico ao fazer push do prompt: {e}")
        print("\n💡 DICA DE DEBUG:")
        print("Se o erro acima for 'JSONDecodeError: Expecting value: line 1 column 1',")
        print("isso indica que o LangSmith bloqueou a requisição ou sua rede (VPN/Firewall) interceptou a chamada.")
        return False

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors = []
    
    if 'messages' not in prompt_data:
        errors.append("Campo 'messages' não encontrado")
    elif not prompt_data['messages']:
        errors.append("Lista de mensagens está vazia")
    
    messages = prompt_data.get('messages', [])
    for i, msg in enumerate(messages):
        if 'type' not in msg:
            errors.append(f"Mensagem {i}: campo 'type' não encontrado")
        if 'content' not in msg:
            errors.append(f"Mensagem {i}: campo 'content' não encontrado")
        elif not msg['content'].strip():
            errors.append(f"Mensagem {i}: conteúdo vazio")
    
    has_system_or_human = any(msg.get('type') in ['system', 'human'] for msg in messages)
    if not has_system_or_human:
        errors.append("Prompt deve ter pelo menos uma mensagem 'system' ou 'human'")
    
    return (len(errors) == 0, errors)

def main():
    print("=" * 60)
    print("Push de Prompts para o LangSmith")
    print("=" * 60)
    
    # 1. Carrega o prompt otimizado (v2) forçando UTF-8
    prompt_file = "prompts/bug_to_user_story_v2.yml"
    print(f"📂 Carregando prompt: {prompt_file}")
    
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo YAML: {e}")
        return 1
        
    if not prompt_data:
        print(f"❌ Erro ao carregar {prompt_file} (Arquivo vazio ou inválido)")
        return 1
    
    print("✅ Prompt carregado com sucesso")
    
    # 2. Valida o prompt
    print("🔍 Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    
    if not is_valid:
        print("❌ Prompt inválido. Erros encontrados:")
        for error in errors:
            print(f"   - {error}")
        return 1
    
    print("✅ Prompt válido\n")
    
    # 3. Faz push usando EXATAMENTE a variável do seu .env
    username = os.getenv('USERNAME_LANGSMITH_HUB')
    if not username:
        print("❌ Erro: Variável 'USERNAME_LANGSMITH_HUB' não encontrada no .env")
        return 1
        
    prompt_name = f"{username}/bug_to_user_story_v2"
    
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    
    if success:
        print("\n📁 Próximos passos:")
        print("   1. Verifique o prompt no dashboard do LangSmith")
        print("   2. Execute a avaliação: python src/evaluate.py")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())