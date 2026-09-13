import time


class CPU_VonNeumann:
    def __init__(self):
        # 1. Hierarquia de Memória: Simulando a Memória Principal (RAM)
        # No modelo de Von Neumann, dados e instruções dividem o mesmo espaço.
        self.memoria = [0] * 20

        # 2. Registradores (Memória ultrarrápida dentro da CPU)
        self.PC = 0                # Program Counter: aponta para a próxima instrução
        self.registradores = {
            'R1': 0,
            'R2': 0
        }

        self.rodando = True

    def carregar_programa(self, programa):
        """Carrega o código Assembly para dentro da Memória Principal"""
        for i, instrucao in enumerate(programa):
            self.memoria[i] = instrucao
        print("[SISTEMA] Programa carregado na memória.\n")

    def ciclo_instrucao(self):
        """Executa um ciclo completo de Fetch-Decode-Execute"""

        # --- ETAPA 1: FETCH (BUSCA) ---
        # A CPU vai na memória buscar a instrução indicada pelo PC
        instrucao_atual = self.memoria[self.PC]
        print(f"[{self.PC}] FETCH: Buscou a instrução '{instrucao_atual}'")

        # O PC avança para a próxima posição
        self.PC += 1

        # --- ETAPA 2: DECODE (DECODIFICAÇÃO) ---
        # A Unidade de Controle quebra a instrução para entender o que fazer
        if instrucao_atual == 0:
            return  # Memória vazia

        partes = instrucao_atual.split()
        opcode = partes[0]  # O comando em si (LOAD, ADD, etc)

        print(f"    DECODE: Comando é {opcode}")

        # --- ETAPA 3: EXECUTE (EXECUÇÃO) ---
        # A Unidade Lógica e Aritmética (ULA) executa a ação
        if opcode == "LOAD":
            # Ex: LOAD R1 10 (Carrega o valor 10 no registrador R1)
            reg = partes[1]
            valor = int(partes[2])
            self.registradores[reg] = valor
            print(f"    EXECUTE: {reg} agora vale {valor}")

        elif opcode == "ADD":
            # Ex: ADD R1 R2 (Soma R2 em R1)
            reg_destino = partes[1]
            reg_origem = partes[2]
            soma = self.registradores[reg_destino] + \
                self.registradores[reg_origem]
            self.registradores[reg_destino] = soma
            print(
                f"    EXECUTE: Somou {reg_origem} em {reg_destino}. Resultado: {soma}")

        elif opcode == "STORE":
            # Ex: STORE R1 15 (Salva o valor de R1 no endereço 15 da memória)
            reg = partes[1]
            endereco = int(partes[2])
            self.memoria[endereco] = self.registradores[reg]
            print(
                f"    EXECUTE: Salvou o valor {self.registradores[reg]} no endereço de memória {endereco}")

        elif opcode == "HALT":
            # Para a execução
            self.rodando = False
            print("    EXECUTE: Processador parado (HALT).")

    def executar(self):
        while self.rodando:
            self.ciclo_instrucao()
            time.sleep(1)  # Pausa para facilitar a leitura no terminal
            print(f"    ESTADO DOS REGISTRADORES: {self.registradores}")
            print("-" * 50)


# ==========================================
# TESTANDO A ARQUITETURA
# ==========================================
cpu = CPU_VonNeumann()

# Um programa simples escrito em "Assembly" inventado (ISA)
# O objetivo do programa é somar 5 + 7 e guardar na memória.
codigo_assembly = [
    "LOAD R1 5",    # Endereço 0
    "LOAD R2 7",    # Endereço 1
    "ADD R1 R2",    # Endereço 2: R1 = R1 + R2
    # Endereço 3: Salva o resultado (12) no endereço 15 da memória
    "STORE R1 15",
    "HALT"          # Endereço 4: Para a CPU
]

cpu.carregar_programa(codigo_assembly)
cpu.executar()

print(
    f"Verificando a Memória Principal no endereço 15: Valor = {cpu.memoria[15]}")
