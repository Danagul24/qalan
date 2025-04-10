from flask import Flask, render_template_string, request

app = Flask(__name__)

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Оценка CSI и NPS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            height: 120vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .form-container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            width: 300px;
        }
        input[type="number"], input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-top: 8px;
            margin-bottom: 12px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        h3 {
            text-align: center;
        }
    </style>
</head>
<body>
    <h2>Введите данные</h2>
    <form method="post">
        Качество продукта: <input name="p1" type="number" min="1" max="5" required><br>
        Качество обратной связи: <input name="p2" type="number" min="1" max="5" required><br>
        Результативность: <input name="p3" type="number" min="1" max="5" required><br>
        NPS (1-10 или "не смогу оценить"): <input name="nps" required><br>
        <input type="submit" value="Рассчитать">
    </form>
    {% if result %}
        <h3>Результат:</h3>
        <p>NPS: {{ nps }}</p>
        <p>CSI: {{ csi }}</p>
        <p>Вывод: {{ result }}</p>
    {% endif %}
</body>
</html>
"""

def calculate_csi_and_check(p1, p2, p3, nps):
    score = p1 + p2 + p3
    weights = [p / score for p in (p1, p2, p3)]
    s_values = [p * w for p, w in zip((p1, p2, p3), weights)]
    csi = round(sum(s_values), 2)

    if isinstance(nps, str) and nps.strip().lower() == "не смогу оценить":
        result = "опрос не нужно проводить" if csi > 4.5 else "опрос нужно провести"
        return result, nps, csi

    try:
        nps = int(nps)
        if not (1 <= nps <= 10):
            raise ValueError()
        if nps >= 9:
            result = "опрос не нужно проводить" if csi >= 3.76 else "опрос нужно провести"
        elif 7 <= nps <= 8:
            result = "опрос не нужно проводить" if csi >= 4.5 else "опрос нужно провести"
        else:
            result = "опрос нужно провести"
    except:
        result = "ошибка: некорректное значение NPS"

    return result, nps, csi

@app.route("/", methods=["GET", "POST"])
def index():
    result = csi = nps = None
    if request.method == "POST":
        try:
            nps_input = request.form["nps"]
            p1 = int(request.form["p1"])
            p2 = int(request.form["p2"])
            p3 = int(request.form["p3"])
            result, nps, csi = calculate_csi_and_check(p1, p2, p3, nps_input)
        except Exception as e:
            result = f"Ошибка: {e}"
    return render_template_string(html_form, result=result, csi=csi, nps=nps)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
