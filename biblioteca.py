from datetime import date
def cadastrar_livro(livros):
    print("\n--- Cadastro de Livro ---")
    codigo = input("Codigo do livro: ").strip()

    if buscar_livro_por_codigo(livros, codigo) is not None:
        print("Ja existe um livro com esse codigo!")
        return

    titulo = input("Titulo: ").strip()
    autor = input("Autor: ").strip()

    try:
        quantidade = int(input("Quantidade de exemplares: "))
    except ValueError:
        print("Quantidade invalida. Cadastro cancelado.")
        return

    livro = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "quantidade_total": quantidade,
        "quantidade_disponivel": quantidade,
    }

    livros.append(livro)
    print(f"Livro '{titulo}' cadastrado com sucesso!")


def cadastrar_usuario(usuarios):
    print("\n--- Cadastro de Usuario ---")
    codigo = input("Codigo do usuario: ").strip()

    if buscar_usuario_por_codigo(usuarios, codigo) is not None:
        print("Ja existe um usuario com esse codigo!")
        return

    nome = input("Nome do usuario: ").strip()

    usuario = {
        "codigo": codigo,
        "nome": nome,
    }

    usuarios.append(usuario)
    print(f"Usuario '{nome}' cadastrado com sucesso!")


def buscar_livro_por_codigo(livros, codigo):
    for livro in livros:
        if livro["codigo"] == codigo:
            return livro
    return None


def buscar_usuario_por_codigo(usuarios, codigo):
    for usuario in usuarios:
        if usuario["codigo"] == codigo:
            return usuario
    return None


def consultar_livros_disponiveis(livros):
    print("\n--- Livros Disponiveis ---")

    disponiveis = [livro for livro in livros if livro["quantidade_disponivel"] > 0]

    if not disponiveis:
        print("Nenhum livro disponivel no momento.")
        return

    for livro in disponiveis:
        print(
            f"[{livro['codigo']}] {livro['titulo']} - {livro['autor']} "
            f"(Disponivel: {livro['quantidade_disponivel']}/{livro['quantidade_total']})"
        )


def listar_todos_livros(livros):
    print("\n--- Todos os Livros Cadastrados ---")
    if not livros:
        print("Nenhum livro cadastrado.")
        return

    for livro in livros:
        print(
            f"[{livro['codigo']}] {livro['titulo']} - {livro['autor']} "
            f"(Disponivel: {livro['quantidade_disponivel']}/{livro['quantidade_total']})"
        )


def listar_todos_usuarios(usuarios):
    print("\n--- Usuarios Cadastrados ---")
    if not usuarios:
        print("Nenhum usuario cadastrado.")
        return

    for usuario in usuarios:
        print(f"[{usuario['codigo']}] {usuario['nome']}")


def emprestar_livro(livros, usuarios, emprestimos):
    print("\n--- Emprestar Livro ---")

    codigo_livro = input("Codigo do livro: ").strip()
    livro = buscar_livro_por_codigo(livros, codigo_livro)

    if livro is None:
        print("Livro nao encontrado.")
        return

    if livro["quantidade_disponivel"] <= 0:
        print("Nao ha exemplares disponiveis para emprestimo.")
        return

    codigo_usuario = input("Codigo do usuario: ").strip()
    usuario = buscar_usuario_por_codigo(usuarios, codigo_usuario)

    if usuario is None:
        print("Usuario nao encontrado.")
        return

    emprestimo = {
        "codigo_livro": livro["codigo"],
        "titulo_livro": livro["titulo"],
        "codigo_usuario": usuario["codigo"],
        "nome_usuario": usuario["nome"],
        "data_emprestimo": str(date.today()),
        "devolvido": False,
        "data_devolucao": None,
    }

    emprestimos.append(emprestimo)
    livro["quantidade_disponivel"] -= 1

    print(f"Emprestimo realizado! '{livro['titulo']}' emprestado para {usuario['nome']}.")


def devolver_livro(livros, emprestimos):
    print("\n--- Devolver Livro ---")

    codigo_usuario = input("Codigo do usuario: ").strip()
    codigo_livro = input("Codigo do livro: ").strip()

    emprestimo_encontrado = None
    for emprestimo in emprestimos:
        if (
            emprestimo["codigo_usuario"] == codigo_usuario
            and emprestimo["codigo_livro"] == codigo_livro
            and not emprestimo["devolvido"]
        ):
            emprestimo_encontrado = emprestimo
            break

    if emprestimo_encontrado is None:
        print("Nao foi encontrado um emprestimo em aberto com esses dados.")
        return

    emprestimo_encontrado["devolvido"] = True
    emprestimo_encontrado["data_devolucao"] = str(date.today())

    livro = buscar_livro_por_codigo(livros, codigo_livro)
    if livro is not None:
        livro["quantidade_disponivel"] += 1

    print("Devolucao registrada com sucesso!")


def gerar_matriz_relatorio(emprestimos):
    matriz = []

    cabecalho = ["Livro", "Usuario", "Data Emprestimo", "Status", "Data Devolucao"]
    matriz.append(cabecalho)

    for emprestimo in emprestimos:
        status = "Devolvido" if emprestimo["devolvido"] else "Em aberto"
        data_devolucao = emprestimo["data_devolucao"] if emprestimo["data_devolucao"] else "-"

        linha = [
            emprestimo["titulo_livro"],
            emprestimo["nome_usuario"],
            emprestimo["data_emprestimo"],
            status,
            data_devolucao,
        ]
        matriz.append(linha)

    return matriz


def exibir_relatorio_emprestimos(emprestimos):
    print("\n--- Relatorio de Emprestimos ---")

    if not emprestimos:
        print("Nenhum emprestimo registrado ainda.")
        return

    matriz = gerar_matriz_relatorio(emprestimos)


    num_colunas = len(matriz[0])
    largura_colunas = [0] * num_colunas

    for linha in matriz:
        for indice_coluna in range(num_colunas):
            tamanho = len(str(linha[indice_coluna]))
            if tamanho > largura_colunas[indice_coluna]:
                largura_colunas[indice_coluna] = tamanho


    for indice_linha, linha in enumerate(matriz):
        texto_linha = ""
        for indice_coluna in range(num_colunas):
            texto_linha += str(linha[indice_coluna]).ljust(largura_colunas[indice_coluna] + 3)
        print(texto_linha)

        if indice_linha == 0:
            print("-" * sum(largura_colunas) + "-" * (num_colunas * 3))



def exibir_menu():
    print("\n===== SISTEMA DE BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Cadastrar usuario")
    print("3 - Emprestar livro")
    print("4 - Devolver livro")
    print("5 - Consultar livros disponiveis")
    print("6 - Listar todos os livros")
    print("7 - Listar todos os usuarios")
    print("8 - Relatorio de emprestimos")
    print("0 - Sair")


def main():
    livros = []
    usuarios = []
    emprestimos = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_livro(livros)
        elif opcao == "2":
            cadastrar_usuario(usuarios)
        elif opcao == "3":
            emprestar_livro(livros, usuarios, emprestimos)
        elif opcao == "4":
            devolver_livro(livros, emprestimos)
        elif opcao == "5":
            consultar_livros_disponiveis(livros)
        elif opcao == "6":
            listar_todos_livros(livros)
        elif opcao == "7":
            listar_todos_usuarios(usuarios)
        elif opcao == "8":
            exibir_relatorio_emprestimos(emprestimos)
        elif opcao == "0":
            print("Encerrando o sistema. Ate mais!")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
