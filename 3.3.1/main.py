from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import mathgenerator

app = Flask(__name__)
app.config.from_object('config')

problem_types = {
     "calculus": mathgenerator.calculus.definite_integral,
     "algebra": mathgenerator.algebra.basic_algebra,
     "arithmetic": mathgenerator.basic_math.addition,
     "geometry": mathgenerator.geometry.circumference
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
