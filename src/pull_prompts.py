import os
import yaml
from langchain import hub

def pull_and_save_prompt():
    print("Conectando ao LangSmith para baixar o prompt...")
    
    # Faz o pull do prompt v1 diretamente do Hub do LangSmith
    prompt = hub.pull("leonanluppi/bug_to_user_story_v1")

    # Garante que a pasta 'prompts' exista na raiz do seu projeto
    os.makedirs("prompts", exist_ok=True)
    
    # Salva o resultado no arquivo yml exigido
    file_path = "prompts/bug_to_user_story_v1.yml"
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(prompt.dict(), f, allow_unicode=True, default_flow_style=False)
        
    print(f"Sucesso! Prompt salvo em {file_path}")

if __name__ == "__main__":
    pull_and_save_prompt()