import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route('/api/alive', methods=['GET'])
def alive():
    return jsonify({"message": "Alive"}), 200


@app.route('/api/associations', methods=['GET'])
def get_associations():
    associations_list = associations_df.to_dict(orient='records')
    return jsonify(associations_list), 200


@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id].to_dict(orient='records')
    if not association:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(association[0]), 200

@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    evenements_list = evenements_df.to_dict(orient='records')
    return jsonify(evenements_list), 200


@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    evenement = evenements_df[evenements_df['id'] == id].to_dict(orient='records')
    if not evenement:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(evenement[0]), 200

@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_evenements_association(id):
    association = associations_df[associations_df['id'] == id].to_dict(orient='records')
    if not association:
        return jsonify({"error": "Association not found"}), 404
    evenements = evenements_df[evenements_df['association_id'] == id].to_dict(orient='records')
    return jsonify(evenements), 200


@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    filtered_associations = associations_df[associations_df['type'] == type].to_dict(orient='records')
    return jsonify(filtered_associations), 200


if __name__ == '__main__':
    app.run(debug=False)
