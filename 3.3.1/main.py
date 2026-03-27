from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import mathgenerator

app = Flask(__name__)
app.config.from_object('config')

problem_types = {
     "definite_integrals": mathgenerator.calculus.definite_integral,
     "basic_algebra": mathgenerator.algebra.basic_algebra,
     "addition": mathgenerator.basic_math.addition,
     "circumference": mathgenerator.geometry.circumference,
     "combine_like_terms": mathgenerator.algebra.combine_like_terms,
     "factoring": mathgenerator.algebra.factoring,
     "expanding": mathgenerator.algebra.expanding,
     "quadratic_equations": mathgenerator.algebra.quadratic_equation,
     "equation_from_points": mathgenerator.geometry.equation_of_line_from_two_points,
     "systems_of_equations": mathgenerator.algebra.system_of_equations,
     "divide_fractions": mathgenerator.basic_math.divide_fractions,
     "percentage": mathgenerator.basic_math.percentage
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/practice")
def practice():
    type = request.args.get("type")
    if not isinstance(type, str):
        return redirect(url_for('index'), code = 301)

    if type.lower() in problem_types:
        return render_template("practice.html", type = type)
    else:
        return redirect(url_for('index'), code = 301)

@app.route('/api/<string:problem_type>', methods=['GET'])
def api(problem_type: str):
    if problem_type in problem_types.keys():
        problem, solution = problem_types[problem_type]()
        json = {
            "problem": problem,
            "solution": solution
        }
        return jsonify(json)
    return abort(404)


if __name__ == "__main__":
    app.run()
