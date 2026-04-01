import os
import sqlite3
from colorama import Fore, init

init(autoreset=True)

NOME_BD = "pecas.db"


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para continuar...")


def msg_sucesso(texto):
    print(f"{Fore.GREEN}✅ {texto}")


def msg_erro(texto):
    print(f"{Fore.RED}❌ {texto}")


def msg_aviso(texto):
    print(f"{Fore.YELLOW}⚠️ {texto}")


def msg_info(texto):
    print(f"{Fore.CYAN}ℹ️ {texto}")


def titulo(texto):
    print(f"{Fore.MAGENTA}{'=' * 60}")
    print(texto.center(60))
    print(f"{Fore.MAGENTA}{'=' * 60}")


def subtitulo(texto):
    print(f"\n{Fore.BLUE}{texto}")


def criar_tabelas():
    with sqlite3.connect(NOME_BD) as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caixas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL CHECK(status IN ('aberta', 'fechada'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peso REAL NOT NULL,
                cor TEXT NOT NULL,
                comprimento REAL NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Aprovada', 'Reprovada')),
                motivos TEXT,
                caixa_id INTEGER,
                FOREIGN KEY (caixa_id) REFERENCES caixas(id)
            )
        """)


def validar_peca(peso, cor, comprimento):
    motivos = []

    if peso < 95 or peso > 105:
        motivos.append("Peso fora do intervalo permitido (95g a 105g)")

    if cor.lower() not in ["azul", "verde"]:
        motivos.append("Cor inválida (somente azul ou verde)")

    if comprimento < 10 or comprimento > 20:
        motivos.append("Comprimento fora do intervalo permitido (10cm a 20cm)")

    if not motivos:
        return "Aprovada", ""

    return "Reprovada", " | ".join(motivos)


def obter_ou_criar_caixa_aberta(cursor):
    cursor.execute("""
        SELECT id
        FROM caixas
        WHERE status = 'aberta'
        ORDER BY id ASC
        LIMIT 1
    """)
    caixa = cursor.fetchone()

    if caixa:
        return caixa[0]

    cursor.execute("""
        INSERT INTO caixas (status)
        VALUES ('aberta')
    """)
    return cursor.lastrowid


def verificar_fechamento_caixa(cursor, caixa_id):
    cursor.execute("""
        SELECT COUNT(*)
        FROM pecas
        WHERE caixa_id = ?
    """, (caixa_id,))
    total = cursor.fetchone()[0]

    if total >= 10:
        cursor.execute("""
            UPDATE caixas
            SET status = 'fechada'
            WHERE id = ?
        """, (caixa_id,))
        return True

    return False


def limpar_caixas_abertas_vazias(cursor):
    cursor.execute("""
        SELECT id
        FROM caixas
        WHERE status = 'aberta'
    """)
    caixas = cursor.fetchall()

    for caixa in caixas:
        caixa_id = caixa[0]
        cursor.execute("""
            SELECT COUNT(*)
            FROM pecas
            WHERE caixa_id = ?
        """, (caixa_id,))
        quantidade = cursor.fetchone()[0]

        if quantidade == 0:
            cursor.execute("""
                DELETE FROM caixas
                WHERE id = ?
            """, (caixa_id,))


def mostrar_pecas_sem_pausar(cursor):
    subtitulo("PEÇAS APROVADAS")
    cursor.execute("""
        SELECT id, peso, cor, comprimento, caixa_id
        FROM pecas
        WHERE status = 'Aprovada'
        ORDER BY id
    """)
    aprovadas = cursor.fetchall()

    if not aprovadas:
        print("Nenhuma peça aprovada cadastrada.")
    else:
        for p in aprovadas:
            print(
                f"ID: {p[0]} | Peso: {p[1]}g | "
                f"Cor: {p[2]} | Comprimento: {p[3]}cm | Caixa: {p[4]}"
            )

    subtitulo("PEÇAS REPROVADAS")
    cursor.execute("""
        SELECT id, peso, cor, comprimento, motivos
        FROM pecas
        WHERE status = 'Reprovada'
        ORDER BY id
    """)
    reprovadas = cursor.fetchall()

    if not reprovadas:
        print("Nenhuma peça reprovada cadastrada.")
    else:
        for p in reprovadas:
            print(
                f"ID: {p[0]} | Peso: {p[1]}g | "
                f"Cor: {p[2]} | Comprimento: {p[3]}cm"
            )
            print("Motivo(s):")
            for motivo in p[4].split(" | "):
                print(f"  - {motivo}")
            print()


def cadastrar_peca():
    limpar_tela()
    titulo("CADASTRAR NOVA PEÇA")

    try:
        peso = float(input("Digite o peso da peça (g): ").strip())
        cor = input("Digite a cor da peça: ").strip().lower()
        comprimento = float(input("Digite o comprimento da peça (cm): ").strip())
    except ValueError:
        msg_erro("Peso e comprimento devem ser números.")
        pausar()
        return

    status, motivos = validar_peca(peso, cor, comprimento)

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()

            caixa_id = None
            if status == "Aprovada":
                caixa_id = obter_ou_criar_caixa_aberta(cursor)

            cursor.execute("""
                INSERT INTO pecas (peso, cor, comprimento, status, motivos, caixa_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (peso, cor, comprimento, status, motivos, caixa_id))

            id_gerado = cursor.lastrowid

            if status == "Aprovada":
                msg_sucesso(f"Peça {id_gerado} cadastrada com sucesso: APROVADA.")
                if verificar_fechamento_caixa(cursor, caixa_id):
                    msg_info(f"Caixa {caixa_id} fechada com 10 peças.")
                else:
                    msg_info(f"Peça armazenada na caixa aberta {caixa_id}.")
            else:
                msg_erro(f"Peça {id_gerado} cadastrada com sucesso: REPROVADA.")
                print("Motivo(s) da reprovação:")
                for motivo in motivos.split(" | "):
                    print(f"- {motivo}")

    except sqlite3.Error as erro:
        msg_erro(f"Erro no banco de dados: {erro}")

    pausar()


def listar_pecas():
    limpar_tela()
    titulo("LISTAR PEÇAS APROVADAS/REPROVADAS")

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()
            mostrar_pecas_sem_pausar(cursor)
    except sqlite3.Error as erro:
        msg_erro(f"Erro ao listar peças: {erro}")

    pausar()


def remover_peca():
    limpar_tela()
    titulo("REMOVER PEÇA CADASTRADA")

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()

            mostrar_pecas_sem_pausar(cursor)
            print()

            try:
                id_peca = int(input("Digite o ID da peça: ").strip())
            except ValueError:
                msg_erro("ID inválido. Digite um número inteiro.")
                pausar()
                return

            cursor.execute("""
                SELECT p.caixa_id, c.status
                FROM pecas p
                LEFT JOIN caixas c ON p.caixa_id = c.id
                WHERE p.id = ?
            """, (id_peca,))
            peca = cursor.fetchone()

            if not peca:
                msg_erro("Peça não encontrada.")
                pausar()
                return

            if peca[0] is not None and peca[1] == "fechada":
                msg_aviso("Não é permitido remover peça de caixa fechada.")
                pausar()
                return

            confirmar = input("Confirmar exclusão (s/n)? ").strip().lower()
            if confirmar != "s":
                msg_info("Remoção cancelada.")
                pausar()
                return

            cursor.execute("""
                DELETE FROM pecas
                WHERE id = ?
            """, (id_peca,))
            limpar_caixas_abertas_vazias(cursor)

            msg_sucesso("Peça removida com sucesso.")

    except sqlite3.Error as erro:
        msg_erro(f"Erro ao remover peça: {erro}")

    pausar()


def listar_caixas_fechadas():
    limpar_tela()
    titulo("LISTAR CAIXAS FECHADAS")

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id
                FROM caixas
                WHERE status = 'fechada'
                ORDER BY id
            """)
            caixas = cursor.fetchall()

            if not caixas:
                print("Nenhuma caixa fechada até o momento.")
                pausar()
                return

            for caixa in caixas:
                caixa_id = caixa[0]
                subtitulo(f"Caixa {caixa_id}")

                cursor.execute("""
                    SELECT id
                    FROM pecas
                    WHERE caixa_id = ?
                    ORDER BY id
                """, (caixa_id,))
                pecas = cursor.fetchall()

                for peca in pecas:
                    print(f"- ID da peça: {peca[0]}")

    except sqlite3.Error as erro:
        msg_erro(f"Erro ao listar caixas fechadas: {erro}")

    pausar()


def listar_caixa_aberta():
    limpar_tela()
    titulo("LISTAR CAIXA ABERTA (EXTRA)")

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id
                FROM caixas
                WHERE status = 'aberta'
                ORDER BY id ASC
                LIMIT 1
            """)
            caixa = cursor.fetchone()

            if not caixa:
                print("Não há caixa aberta no momento.")
                pausar()
                return

            caixa_id = caixa[0]
            msg_info(f"Caixa aberta atual: {caixa_id}")

            cursor.execute("""
                SELECT id, peso, cor, comprimento
                FROM pecas
                WHERE caixa_id = ?
                ORDER BY id
            """, (caixa_id,))
            pecas = cursor.fetchall()

            print()
            if not pecas:
                print("A caixa aberta está vazia.")
            else:
                for peca in pecas:
                    print(
                        f"ID: {peca[0]} | Peso: {peca[1]}g | "
                        f"Cor: {peca[2]} | Comprimento: {peca[3]}cm"
                    )

                print(f"\nTotal de peças na caixa aberta: {len(pecas)}/10")

    except sqlite3.Error as erro:
        msg_erro(f"Erro ao listar caixa aberta: {erro}")

    pausar()


def gerar_relatorio():
    limpar_tela()
    titulo("GERAR RELATÓRIO FINAL")

    try:
        with sqlite3.connect(NOME_BD) as conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT COUNT(*) FROM pecas")
            total_pecas = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM pecas WHERE status = 'Aprovada'")
            total_aprovadas = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM pecas WHERE status = 'Reprovada'")
            total_reprovadas = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM caixas WHERE status = 'fechada'")
            total_caixas_fechadas = cursor.fetchone()[0]

            cursor.execute("""
                SELECT id
                FROM caixas
                WHERE status = 'aberta'
                ORDER BY id ASC
                LIMIT 1
            """)
            caixa_aberta = cursor.fetchone()

            pecas_na_caixa_aberta = 0
            total_caixas_utilizadas = total_caixas_fechadas

            if caixa_aberta:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM pecas
                    WHERE caixa_id = ?
                """, (caixa_aberta[0],))
                pecas_na_caixa_aberta = cursor.fetchone()[0]

                if pecas_na_caixa_aberta > 0:
                    total_caixas_utilizadas += 1

            print(f"Total de peças cadastradas: {total_pecas}")
            print(f"Total de peças aprovadas: {total_aprovadas}")
            print(f"Total de peças reprovadas: {total_reprovadas}")
            print(f"Quantidade de caixas fechadas: {total_caixas_fechadas}")
            print(f"Quantidade de caixas utilizadas: {total_caixas_utilizadas}")
            print(f"Peças na caixa aberta atual: {pecas_na_caixa_aberta}")

            subtitulo("Motivos de reprovação:")
            cursor.execute("""
                SELECT motivos
                FROM pecas
                WHERE status = 'Reprovada'
            """)
            reprovadas = cursor.fetchall()

            if not reprovadas:
                print("Nenhuma peça foi reprovada.")
            else:
                contagem_motivos = {}

                for item in reprovadas:
                    motivos = item[0].split(" | ")
                    for motivo in motivos:
                        contagem_motivos[motivo] = contagem_motivos.get(motivo, 0) + 1

                for motivo, quantidade in contagem_motivos.items():
                    print(f"- {motivo}: {quantidade} ocorrência(s)")

    except sqlite3.Error as erro:
        msg_erro(f"Erro ao gerar relatório: {erro}")

    pausar()


def exibir_menu():
    limpar_tela()
    print(f"{Fore.MAGENTA}{'#' * 60}")
    print(" SISTEMA DE GERENCIAMENTO DE PEÇAS ".center(60))
    print(f"{Fore.MAGENTA}{'#' * 60}")

    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("6. Listar caixa aberta")
    print("0. Sair")

    print(f"{Fore.MAGENTA}{'#' * 60}")


def app():
    criar_tabelas()

    while True:
        exibir_menu()

        try:
            op = int(input("Opção: ").strip())
        except ValueError:
            msg_erro("Digite um número válido.")
            pausar()
            continue

        if op == 1:
            cadastrar_peca()
        elif op == 2:
            listar_pecas()
        elif op == 3:
            remover_peca()
        elif op == 4:
            listar_caixas_fechadas()
        elif op == 5:
            gerar_relatorio()
        elif op == 6:
            listar_caixa_aberta()
        elif op == 0:
            msg_info("Encerrando o sistema.")
            break
        else:
            msg_erro("Opção inválida.")
            pausar()


app()