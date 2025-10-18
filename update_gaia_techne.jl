# update_gaia_techne.jl: Automação do fluxo de atualização do repositório.

"""
Executa o ciclo completo de atualização do repositório:
1.  `git pull` para sincronizar com o repositório remoto.
2.  `git add .` para adicionar todas as novas modificações.
3.  `git commit` com uma mensagem padrão.
4.  `git push` para enviar as atualizações.
"""
function update_repository()
    try
        println("Iniciando a atualização do repositório AGI-GAIA-TECHNE...")

        # 1. Git Pull
        println("Executando 'git pull'...")
        run(`git pull`)

        # 2. Git Add
        println("Executando 'git add .'...")
        run(`git add .`)

        # 3. Git Commit
        commit_message = "Atualização automatizada do repositório."
        println("Executando 'git commit' com a mensagem: \"$commit_message\"")
        run(`git commit -m "$commit_message"`)

        # 4. Git Push
        println("Executando 'git push'...")
        run(`git push`)

        println("Repositório atualizado com sucesso!")

    catch e
        println("Ocorreu um erro durante a atualização do repositório: ", e)
    end
end

# Executa a função de atualização
update_repository()
