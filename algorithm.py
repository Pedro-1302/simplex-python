class SimplexCalculator:
    # Definição do Construtor  
    def __init__(self): 
        # Criação da Tabela vazia
        self.table = []


    # Definição da Função Objetiva 
    def definir_fo(self, fo: list): 
        # Adiciona a função objetiva na tabela
        self.table.append(fo)


    # Definição de Função para Criar Restrições 
    def add_restricoes(self, res: list): 
        # Adiciona restrições
        self.table.append(res)
    
    
    # Definição de Função para Retornar Coluna Pivot
    def retornar_coluna_entrada(self) -> int:
        # Pega o menor valor negativo da minha linha da função objetiva
        coluna_pivot = min(self.table[0])
        # Pega o indice da coluna em que encontrei o menor valor
        indice = self.table[0].index(coluna_pivot)
        # Retorna o indice dessa coluna pivot
        return indice
      
      
    # Definição de Função para Retornar Linha Pivot    
    def retornar_linha_saida(self, coluna_entrada: int) -> int: 
        resultados = {}
        for linha in range(len(self.table)): 
            # Se o nao for na linha da função objetiva
            if linha > 0: 
                if self.table[linha][coluna_entrada] > 0:
                    divisao = self.table[linha][-1] / self.table[linha][coluna_entrada]
                    resultados[linha] = divisao
        # Pega a linha que apresenta o menor valor entre as divisoes
        # Entao pega o menor valor que esta armazenado para a chave do dicionário
        # Se for chave 0, valor 10, ele pega valor 10
        indice = min(resultados, key=resultados.get)
        return indice 
    
    
    def calcular_nova_linha_pivot(self, coluna_entrada: int, linha_saida: int) -> list:
        linha = self.table[linha_saida]
        pivot = linha[coluna_entrada]
        nova_linha_pivot = [valor / pivot for valor in linha]
        return nova_linha_pivot 
    
    # Pego a linha e multiplico ela pelo valor negativo do numero que esta na intersecao 
    # coluna item desses itens 
    def calcular_nova_linha(self, linha: list, coluna_entrada: int, linha_pivot: list) -> list:
        pivot = linha[coluna_entrada] * -1
        linha_resultado = [valor * pivot for valor in linha_pivot]
        nova_linha = []
        for i in range(len(linha_resultado)):
            soma = linha_resultado[i] + linha[i]
            nova_linha.append(soma)
        return nova_linha


    # Vefifica se tem negativo na primeira linha da tabela
    def eh_negativo(self) -> bool: 
        # Se algum valor ser negativo (lambda: funcao/condicoes, iteravel)
        negativa = list(filter(lambda x: x < 0, self.table[0]))
        return True if len(negativa) > 0 else False 


    # Encontrar índice da coluna que apresenta um único valor 1 e o restante sendo 0
    def encontrar_coluna_unitaria(self) -> int:
        for j in range(1, len(self.table[0]) - 1):  # Ignorar a primeira e a última coluna
            col = [self.table[i][j] for i in range(len(self.table))]
            if col.count(1) == 1 and col.count(0) == len(col) - 1:
                return j
        return -1  # Retorna -1 se não encontrar
        
    # Retorna o valor da última coluna na linha onde está o 1
    def obter_valor_ultima_coluna(self, coluna_index: int) -> float:
        linha_index = [i for i in range(len(self.table)) if self.table[i][coluna_index] == 1][0]
        return self.table[linha_index][-1]

    # Retorna as variáveis básicas e seus valores
    def obter_variaveis_basicas(self) -> dict:
        variaveis_basicas = {}
        for i in range(1, len(self.table[0]) - 1):  # Ignorar a primeira e a última coluna
            col = [self.table[j][i] for j in range(len(self.table))]
            if col.count(1) == 1 and col.count(0) == len(col) - 1:
                linha_index = col.index(1)
                variavel = f"x{i}" if i != len(self.table[0]) - 2 else "Folga"  # Última coluna é a de folga
                variaveis_basicas[variavel] = self.table[linha_index][-1]
        return variaveis_basicas

    # Imprimir a tabela
    def mostrar_tabela(self):
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                print(f"{self.table[i][j]:.2f}\t", end="")
            print()
        coluna_unitaria = self.encontrar_coluna_unitaria()
        if coluna_unitaria != -1:
            valor_ultima_coluna = self.obter_valor_ultima_coluna(coluna_unitaria)
            print("O valor na última coluna correspondente à coluna unitária é:", valor_ultima_coluna)
        
        variaveis_basicas = self.obter_variaveis_basicas()
        print("Variáveis Básicas e seus valores:")
        for var, val in variaveis_basicas.items():
            print(f"{var}: {val}")
        
        
    # Recalcular a tabela
    def calcular(self): 
        coluna_entrada = self.retornar_coluna_entrada()
        linha_saida = self.retornar_linha_saida(coluna_entrada)
        nova_linha_pivot = self.calcular_nova_linha_pivot(coluna_entrada, linha_saida)
        self.table[linha_saida] = nova_linha_pivot
        table_copy = self.table.copy() 
        indice = 0 
        while indice < len(self.table): 
            if indice != linha_saida: 
                linha = table_copy[indice]
                nova_linha = self.calcular_nova_linha(linha, coluna_entrada, nova_linha_pivot)
                self.table[indice] = nova_linha
            indice += 1
    
    
    # Chamar o método para calcular novamente até não ter mais valores negativos
    def resolver(self): 
        self.calcular()   
        while self.eh_negativo(): 
            self.calcular() 
        self.mostrar_tabela()

if __name__ == "__main__": 
    simplex = SimplexCalculator()
    simplex.definir_fo([1, -20, -30, -10, 0, 0, 0 ,0])
    simplex.add_restricoes([0, 1, 1, 1, 1, 0, 0, 400])
    simplex.add_restricoes([0, 2, 1, -1, 0, 1, 0, 200])
    simplex.add_restricoes([0, 3, 2, -1, 0, 0, 1, 300])
    simplex.resolver()