import subprocess
import datetime
import os

# Caminho do arquivo de log — usa caminho absoluto relativo ao script
# para funcionar tanto localmente quanto no runner do GitHub Actions
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")


def registrar_log():
    """Adiciona uma linha de timestamp ao arquivo de log."""
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Execução registrada em: {agora}\n")
    print(f"[LOG] Registro adicionado: {agora}")


def executar_comando(comando):
    """
    Executa um comando de shell via subprocess e captura o resultado.
    check=False porque queremos tratar erros manualmente (ex: 'nothing to commit'
    não deveria derrubar o script).
    """
    resultado = subprocess.run(
        comando,
        shell=True,
        capture_output=True,
        text=True,
    )
    print(f"[CMD] {comando}")
    if resultado.stdout:
        print(resultado.stdout.strip())
    if resultado.returncode != 0 and resultado.stderr:
        print(f"[ERRO] {resultado.stderr.strip()}")
    return resultado.returncode


def git_commit_push():
    """Fluxo add -> commit -> push, com verificação de mudanças reais."""
    # git status --porcelain retorna vazio se não há nada para commitar
    status = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    if not status:
        print("[INFO] Nenhuma mudança detectada. Encerrando sem commit.")
        return

    executar_comando("git add log.txt")

    mensagem = f"chore: atualiza log automático em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    executar_comando(f'git commit -m "{mensagem}"')

    executar_comando("git push origin main")


if __name__ == "__main__":
    registrar_log()
    git_commit_push()