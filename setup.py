from cx_Freeze import setup, Executable

# Dependências são automaticamente detectadas, mas pode ser necessário
# adicionar pacotes adicionais em 'packages'
build_exe_options = {
    "packages": ["os"],  # Adicione quaisquer pacotes adicionais necessários
    "include_files": [("document_loader.py")]
    # "include_files": [("caminho/para/create_facts.txt", "create_facts.txt")]  # Adicione quaisquer arquivos adicionais necessários
}

# Configuração do executável
setup(
    name="doc_spli_freeze",
    version="0.1",
    description="Aplicatido de controle de qualidade para manuais",
    options={"build_exe": build_exe_options},
    executables=[Executable("page.py")]  # Substitua pelo nome do seu script principal
)
