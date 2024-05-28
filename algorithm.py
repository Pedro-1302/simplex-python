from flask import Flask, request, render_template, redirect, url_for
from logic import LogicCalc

app = Flask(__name__)
logic = LogicCalc()

class SimplexCalculator:
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

        logic = LogicCalc()
        logic.definir_fo(fo_values)
        for res in restr_values:
            logic.add_restricoes(res)

        logic.resolver()
        return render_template("resultado.html", tabelas=logic.tabelas, pivots=logic.pivots, zip=zip)


if __name__ == "__main__":
    app.run(debug=True)
