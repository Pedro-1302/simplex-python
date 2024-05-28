from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class SimplexCalculator:
    def __init__(self):
        self.tabelas = []
        self.table = []

    def definir_fo(self, fo: list):
        fo = [fo[0]] + [-j for j in fo[1:]]
        self.table.append(fo)

    def add_restricoes(self, res: list):
        self.table.append(res)

    def retornar_coluna_entrada(self) -> int:
        coluna_pivot = min(self.table[0])
        indice = self.table[0].index(coluna_pivot)
        return indice

    def retornar_linha_saida(self, coluna_entrada: int) -> int:
        resultados = {}
        for linha in range(1, len(self.table)):
            if self.table[linha][coluna_entrada] > 0:
                divisao = self.table[linha][-1] / self.table[linha][coluna_entrada]
                resultados[linha] = divisao
        indice = min(resultados, key=resultados.get)
        return indice

    def calcular_nova_linha_pivot(self, coluna_entrada: int, linha_saida: int) -> list:
        linha = self.table[linha_saida]
        pivot = linha[coluna_entrada]
        nova_linha_pivot = [valor / pivot for valor in linha]
        return nova_linha_pivot

    def calcular_nova_linha(self, linha: list, coluna_entrada: int, linha_pivot: list) -> list:
        pivot = linha[coluna_entrada] * -1
        linha_resultado = [valor * pivot for valor in linha_pivot]
        nova_linha = []
        for i in range(len(linha_resultado)):
            soma = linha_resultado[i] + linha[i]
            nova_linha.append(soma)
        return nova_linha

    def eh_negativo(self) -> bool:
        negativa = list(filter(lambda x: x < 0, self.table[0]))
        return True if len(negativa) > 0 else False

    def resolver(self):
        self.tabelas.append([linha[:] for linha in self.table])
        while self.eh_negativo():
            coluna_entrada = self.retornar_coluna_entrada()
            linha_saida = self.retornar_linha_saida(coluna_entrada)
            nova_linha_pivot = self.calcular_nova_linha_pivot(coluna_entrada, linha_saida)
            self.table[linha_saida] = nova_linha_pivot
            table_copy = self.table.copy()
            for i in range(len(self.table)):
                if i != linha_saida:
                    linha = table_copy[i]
                    nova_linha = self.calcular_nova_linha(linha, coluna_entrada, nova_linha_pivot)
                    self.table[i] = nova_linha
            self.tabelas.append([linha[:] for linha in self.table])

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/resultado.html", methods=["GET"])
def resultado():
    fo_values = [int(val) for val in request.args.get("fo").split(",")]
    restr_quantity = int(request.args.get("restr_quantity"))

    restr_values = []
    for i in range(restr_quantity):
        restr_values.append(
            [int(val) for val in request.args.get(f"restr_{i+1}").split(",")]
        )

    logic = SimplexCalculator()
    logic.definir_fo(fo_values)
    for res in restr_values:
        logic.add_restricoes(res)

    logic.resolver()
    return render_template("resultado.html", tabelas=logic.tabelas)

if __name__ == "__main__":
    app.run(debug=True)