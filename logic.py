class LogicCalc:
    # Definição do Construtor  
    def __init__(self):
        # Inicializa a tabela principal vazia
        self.table = []
        # Lista para armazenar todas as tabelas geradas durante o processo
        self.tabelas = []
        # Lista para armazenar os pivots utilizados durante o processo
        self.pivots = []

    # Função para definir a função objetivo
    def definir_fo(self, fo: list):
        # Negativa todos os valores da função objetivo, exceto o primeiro
        fo = [fo[0]] + [-j for j in fo[1:]]
        # Adiciona a função objetivo na tabela principal
        self.table.append(fo)

    # Função para adicionar restrições à tabela
    def add_restricoes(self, res: list):
        # Adiciona cada restrição fornecida à tabela principal
        self.table.append(res)

    # Função para encontrar a coluna pivot (coluna de entrada)
    def retornar_coluna_entrada(self) -> int:
        # Encontra o menor valor na linha da função objetivo (primeira linha da tabela)
        coluna_pivot = min(self.table[0])
        # Encontra o índice da coluna onde está o menor valor encontrado
        indice = self.table[0].index(coluna_pivot)
        # Retorna o índice da coluna pivot
        return indice

    # Função para encontrar a linha pivot (linha de saída)
    def retornar_linha_saida(self, coluna_entrada: int) -> int:
        # Dicionário para armazenar os resultados das divisões
        resultados = {}
        # Itera sobre todas as linhas (exceto a primeira) da tabela
        for linha in range(1, len(self.table)):
            # Verifica se o valor na coluna de entrada é positivo
            if self.table[linha][coluna_entrada] > 0:
                # Calcula a razão entre o valor do lado direito e o valor na coluna de entrada
                divisao = self.table[linha][-1] / self.table[linha][coluna_entrada]
                # Armazena o resultado da divisão na posição correspondente
                resultados[linha] = divisao
        # Encontra a linha com o menor resultado da divisão
        indice = min(resultados, key=resultados.get)
        # Retorna o índice dessa linha
        return indice

    # Função para calcular a nova linha pivot
    def calcular_nova_linha_pivot(self, coluna_entrada: int, linha_saida: int) -> list:
        # Obtém a linha de saída da tabela
        linha = self.table[linha_saida]
        # Identifica o valor pivot (interseção da linha de saída com a coluna de entrada)
        pivot = linha[coluna_entrada]
        # Divide todos os valores da linha pelo valor pivot para normalizar a linha
        nova_linha_pivot = [valor / pivot for valor in linha]
        # Formata os valores com 2 dígitos decimais
        nova_linha_pivot = [round(valor, 2) for valor in nova_linha_pivot]
        # Retorna a nova linha pivot normalizada
        return nova_linha_pivot

    # Função para calcular a nova linha da tabela
    def calcular_nova_linha(self, linha: list, coluna_entrada: int, linha_pivot: list) -> list:
        # Calcula o fator multiplicador negativo a partir do valor na coluna de entrada
        pivot = linha[coluna_entrada] * -1
        # Multiplica todos os valores da linha pivot pelo fator multiplicador
        linha_resultado = [valor * pivot for valor in linha_pivot]
        # Inicializa a lista para a nova linha
        nova_linha = []
        # Soma os valores da linha original com os valores calculados
        for i in range(len(linha_resultado)):
            soma = linha_resultado[i] + linha[i]
            nova_linha.append(soma)
        # Formata os valores com 2 dígitos decimais
        nova_linha = [round(valor, 2) for valor in nova_linha]
        # Retorna a nova linha atualizada
        return nova_linha

    # Função para verificar se há valores negativos na linha da função objetivo
    def eh_negativo(self) -> bool:
        # Filtra os valores negativos da linha da função objetivo
        negativa = list(filter(lambda x: x < 0, self.table[0]))
        # Retorna True se houver valores negativos, caso contrário, False
        return True if len(negativa) > 0 else False

    # Função principal para resolver o problema de otimização
    def resolver(self):
        # Armazena a tabela inicial e o par de pivots inicial
        self.tabelas.append([linha[:] for linha in self.table])
        self.pivots.append((None, None))
        # Continua o processo enquanto houver valores negativos na função objetivo
        while self.eh_negativo():
            # Encontra a coluna de entrada (pivot)
            coluna_entrada = self.retornar_coluna_entrada()
            # Encontra a linha de saída (pivot)
            linha_saida = self.retornar_linha_saida(coluna_entrada)
            # Calcula a nova linha pivot
            nova_linha_pivot = self.calcular_nova_linha_pivot(coluna_entrada, linha_saida)
            # Atualiza a linha de saída na tabela com a nova linha pivot
            self.table[linha_saida] = nova_linha_pivot
            # Cria uma cópia da tabela para evitar modificações simultâneas
            table_copy = self.table.copy()
            # Atualiza todas as outras linhas com base na nova linha pivot
            for i in range(len(self.table)):
                if i != linha_saida:
                    linha = table_copy[i]
                    nova_linha = self.calcular_nova_linha(linha, coluna_entrada, nova_linha_pivot)
                    self.table[i] = nova_linha
            # Armazena a nova tabela e o par de pivots atualizados
            self.tabelas.append([linha[:] for linha in self.table])
            self.pivots.append((linha_saida, coluna_entrada))
