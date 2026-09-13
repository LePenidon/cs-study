import time


class MemoriaPrincipal:
    def __init__(self):
        # Simulando a RAM, que possui grande capacidade de armazenamento
        self.dados = {
            100: "Variável X",
            101: "Variável Y",
            102: "Variável Z",
            103: "Instrução LOOP",
            104: "Resultado Soma"
        }

    def buscar(self, endereco):
        """Simula a lentidão absurda de buscar algo na RAM"""
        print(f"      [RAM] Buscando endereço {endereco}... (MUITO LENTO)")
        time.sleep(2)  # Pausa de 2 segundos para representar a alta latência
        return self.dados.get(endereco, "Endereço Vazio")


class CacheL1:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.linhas = {}           # Armazena os dados: {endereco: valor}
        # Controla quem foi usado por último (política LRU)
        self.ordem_acesso = []

    def acessar(self, endereco, ram):
        print(f"\n[CPU] Solicitou leitura do endereço {endereco}:")

        # CENÁRIO 1: CACHE HIT (O dado já está na Cache)
        if endereco in self.linhas:
            print("  -> [CACHE HIT] Sucesso! Dado retornado instantaneamente.")
            time.sleep(0.2)  # Quase sem latência

            # Atualiza o status de "uso recente" movendo o endereço para o fim da lista
            self.ordem_acesso.remove(endereco)
            self.ordem_acesso.append(endereco)

            return self.linhas[endereco]

        # CENÁRIO 2: CACHE MISS (O dado não está na Cache)
        else:
            print(
                "  -> [CACHE MISS] Falha. O dado não está aqui. Acionando a RAM...")
            dado_da_ram = ram.buscar(endereco)

            # Se a Cache estiver cheia, precisamos expulsar alguém (Evicção)
            if len(self.linhas) >= self.capacidade:
                # O primeiro item da lista é o mais antigo (Menos Recentemente Usado)
                alvo_expulsao = self.ordem_acesso.pop(0)
                del self.linhas[alvo_expulsao]
                print(
                    f"  -> [CACHE CHEIA] Expulsando o endereço {alvo_expulsao} (LRU) para liberar espaço.")

            # Salva o novo dado na Cache para os próximos acessos
            self.linhas[endereco] = dado_da_ram
            self.ordem_acesso.append(endereco)
            print(
                f"  -> [CACHE ATUALIZADA] Endereço {endereco} salvo na Cache.")

            return dado_da_ram

    def mostrar_estado(self):
        print(f"--- ESTADO DA CACHE L1: {list(self.linhas.keys())} ---")


# =========================================
# EXECUTANDO A SIMULAÇÃO
# =========================================
ram = MemoriaPrincipal()
cache = CacheL1(capacidade=3)  # Nossa Cache só cabe 3 itens!

# 1. CPU pede três variáveis em sequência (Todas darão MISS, pois a cache começa vazia)
cache.acessar(100, ram)
cache.acessar(101, ram)
cache.acessar(102, ram)
cache.mostrar_estado()

# 2. CPU pede a Variável X (endereço 100) novamente.
# Como está na cache, teremos um HIT super rápido!
cache.acessar(100, ram)

# 3. CPU pede um dado novo (endereço 103).
# Dará MISS. A cache está cheia (100, 101, 102).
# Quem ela vai expulsar? O endereço 101, pois o 100 acabou de ser usado (no passo 2) e o 102 é mais recente que o 101.
cache.acessar(103, ram)
cache.mostrar_estado()
