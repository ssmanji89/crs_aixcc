## main.py

from flask import Flask, request, jsonify
from vulnerability_detection import VulnerabilityDetection
from patch_generation import PatchGeneration
from project_management import ProjectManagement
from scoring_evaluation import ScoringEvaluation
from commercialization_transition import CommercializationTransition

app = Flask(__name__)

@app.route('/vulnerability_detection', methods=['POST'])
def detect_vulnerability():
    if 'code' not in request.json:
        return jsonify({"error": "Missing 'code' in request"}), 400
    code = request.json['code']
    vd = VulnerabilityDetection()
    vulnerabilities = vd.detect_vulnerability(code)
    return jsonify(vulnerabilities), 200

@app.route('/patch_generation', methods=['POST'])
def generate_patch():
    if 'vulnerability' not in request.json:
        return jsonify({"error": "Missing 'vulnerability' in request"}), 400
    vulnerability = request.json['vulnerability']
    pg = PatchGeneration()
    patches = pg.generate_patch(vulnerability)
    return jsonify(patches), 200

@app.route('/project_management', methods=['POST'])
def create_project():
    if 'project' not in request.json:
        return jsonify({"error": "Missing 'project' in request"}), 400
    project = request.json['project']
    pm = ProjectManagement()
    project = pm.create_project(project)
    return jsonify(project), 200

@app.route('/scoring_evaluation', methods=['POST'])
def evaluate():
    if 'vulnerability' not in request.json or 'patch' not in request.json:
        return jsonify({"error": "Missing 'vulnerability' or 'patch' in request"}), 400
    vulnerability = request.json['vulnerability']
    patch = request.json['patch']
    se = ScoringEvaluation()
    scores = se.evaluate(vulnerability, patch)
    return jsonify(scores), 200

@app.route('/commercialization_transition', methods=['POST'])
def develop_plan():
    ct = CommercializationTransition()
    plan = ct.develop_plan()
    return jsonify(plan), 200

if __name__ == '__main__':
    app.run(debug=True)
