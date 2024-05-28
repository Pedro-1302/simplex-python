from flask import Flask, request, render_template, redirect, url_for
from logic import LogicCalc

app = Flask(__name__)
logic = LogicCalc()

class SimplexCalculator:

    @app.route("/", methods=["GET"])
    def index():
        return render_template("./index.html")

    @app.route("/resultado.html")
    def resultado():
        # Processar os resultados e passar para o template

        fo_values = [int(val) for val in request.args.get("fo").split(",")]
        restr_quantity = int(request.args.get("restr_quantity"))

        restr_values = []
        for i in range(restr_quantity):
            restr_values.append(
                [int(val) for val in request.args.get(f"restr_{i+1}").split(",")]
            )

        logic.definir_fo(fo_values)
        for res in restr_values:
            logic.add_restricoes(res)

        logic.resolver()
        resultados = logic.processar_resultados()
        return render_template("/resultado.html", resultados=resultados)


if __name__ == "__main__":
    app.run(debug=True)
