import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
        self.LIMITE_SAQUE_VALOR = 500

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\nOperação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        if valor <= 0:
            print("\nOperação falhou! O valor informado é inválido.")
            return

        if valor > self.saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
            return

        if valor > self.LIMITE_SAQUE_VALOR:
            print("\nOperação falhou! O valor do saque excede o limite.")
            return

        if self.numero_saques >= self.LIMITE_SAQUES:
            print("\nOperação falhou! Número máximo de saques excedido.")
            return

        self.saldo -= valor
        self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        self.numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.AGENCIA = "0001"

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\nJá existe usuário com esse CPF!")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            numero_conta = len(self.contas) + 1
            nova_conta = Conta(self.AGENCIA, numero_conta, usuario)
            self.contas.append(nova_conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            if not banco.contas:
                print("\nNão há contas disponíveis. Crie uma conta primeiro.")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            valor = float(input("Informe o valor do depósito: "))
            conta.depositar(valor)

        elif opcao == "s":
            if not banco.contas:
                print("\nNão há contas disponíveis. Crie uma conta primeiro.")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            valor = float(input("Informe o valor do saque: "))
            conta.sacar(valor)

        elif opcao == "e":
            if not banco.contas:
                print("\nNão há contas disponíveis. Crie uma conta primeiro.")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            conta.exibir_extrato()

        elif opcao == "nu":
            banco.criar_usuario()

        elif opcao == "nc":
            banco.criar_conta()

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
