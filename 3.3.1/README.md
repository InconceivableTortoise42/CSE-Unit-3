# Math Practice Web Application
## Project installation

Run uv sync to sync dependencies and download requirements:
```bash
uv sync
```

or alternatively use pip on pregenerated requirements after manually creating venv:

```bash
python -m venv venv
pip install -r requirements.txt
```

Activate virtual environment:
```bash
.venv\Scripts\activate.bat
```


Run main script:
```bash
python main.py
```


To see web interface visit ```http://localhost:5000```


\* The default port can be configured in config.py

Backend: (Flask + Mathgenerator) <br>
https://github.com/pallets/flask - Web server<br>
https://github.com/lukew3/mathgenerator - Problem Generation <br>

Frontend: (Mathjax + Mathlive + Bootstrap) <br>
https://github.com/arnog/mathlive - Math input<br>
https://github.com/mathjax/MathJax - Parse latex notation <br>
https://github.com/twbs/bootstrap - Frontend css framework<br>

