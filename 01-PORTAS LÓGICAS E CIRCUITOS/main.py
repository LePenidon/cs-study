import struct

print("=== TÓPICO 1: PORTAS LÓGICAS E CIRCUITOS ===")

# 1. Definindo as Portas Lógicas Básicas (usando operadores bit a bit do Python)


def porta_AND(a, b): return a & b
def porta_OR(a, b): return a | b
def porta_XOR(a, b): return a ^ b

# 2. Criando um Circuito Combinacional: Half-Adder (Meio Somador)
# Soma dois bits e retorna o Resultado e o "Vai-um" (Carry)


def meio_somador(bit_a, bit_b):
    soma = porta_XOR(bit_a, bit_b)
    carry = porta_AND(bit_a, bit_b)
    return soma, carry


print("Teste do Meio Somador (Half-Adder):")
for a in (0, 1):
    for b in (0, 1):
        s, c = meio_somador(a, b)
        print(f"Entradas: A={a}, B={b} | Soma={s}, Carry (Vai-um)={c}")


print("\n=== TÓPICO 2: SISTEMAS DE NUMERAÇÃO E COMPLEMENTO DE DOIS ===")

numero = 10
print(f"Decimal: {numero}")
print(f"Binário nativo: {bin(numero)}")
print(f"Hexadecimal nativo: {hex(numero)}")

# Função para calcular o Complemento de 2 (simulando uma arquitetura de 8 bits)


def complemento_de_dois(valor, bits=8):
    if valor < 0:
        # Pega o valor absoluto, inverte os bits (XOR com uma máscara de 1s) e soma 1
        # No Python, (1 << bits) + valor faz o equivalente matemático direto
        valor_convertido = (1 << bits) + valor
    else:
        valor_convertido = valor

    # Formata para preencher com zeros à esquerda
    return format(valor_convertido, f'0{bits}b')


print("\nRepresentação em Complemento de 2 (8 bits):")
print(f" +5 em binário: {complemento_de_dois(5)}")
print(f" -5 em binário: {complemento_de_dois(-5)}")


print("\n=== TÓPICO 3: IEEE 754 E ESTOURO DE MEMÓRIA (OVERFLOW) ===")

# Função para extrair Sinal, Expoente e Mantissa de um Float (32 bits)


def float_para_ieee754(numero_float):
    # struct.pack empacota o float em bytes puros
    # struct.unpack('>I') desempacota esses bytes como um inteiro sem sinal
    [inteiro_desempacotado] = struct.unpack(
        '>I', struct.pack('>f', numero_float))

    # Converte o inteiro para uma string binária de exatos 32 caracteres
    binario = format(inteiro_desempacotado, '032b')

    sinal = binario[0]
    expoente = binario[1:9]
    mantissa = binario[9:]
    return sinal, expoente, mantissa


num_teste = -1.5
s, e, m = float_para_ieee754(num_teste)
print(f"IEEE 754 Precision Simple (32 bits) para o número {num_teste}:")
print(f"Sinal: {s} | Expoente: {e} | Mantissa: {m}")

# Simulando o Estouro de Memória (Overflow) em Inteiros com Sinal de 8 bits
# O Python moderno ajusta a memória automaticamente e não sofre overflow em inteiros,
# então precisamos forçar o comportamento de uma CPU clássica (como C ou Java).


def simular_overflow_8bits(valor):
    LIMITE_MAXIMO = 127

    print(f"\nTentando armazenar: {valor} num espaço de 8 bits...")

    # Máscara para manter apenas os últimos 8 bits (0xFF)
    valor_truncado = valor & 0xFF

    # Se o 8º bit (bit de sinal, valor 128) for 1, o número é interpretado como negativo
    if valor_truncado & 0x80:
        resultado_real = valor_truncado - 256
    else:
        resultado_real = valor_truncado

    print(f"Resultado na memória do computador: {resultado_real}")


# 127 é o máximo. Se somarmos 1, ele invade o bit de sinal.
simular_overflow_8bits(127 + 1)
