# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template, request, make_response, redirect, url_for
from jinja2 import Environment, meta, exceptions
from random import choice
from html import escape
import json
import yaml
from yaml import Loader
import base64


app = Flask(__name__)

@app.route("/")
def home():
    encoded_custom_tabs = request.cookies.get("custom_tabs")
    print(encoded_custom_tabs)
    custom_tabs = json.loads(base64.b64decode(encoded_custom_tabs).decode('utf-8')) if encoded_custom_tabs else []
    return render_template('index.html', tabs=custom_tabs)


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    jinja2_env = Environment()

    try:
        jinja2_tpl = jinja2_env.from_string(request.form['template'])
    except (exceptions.TemplateSyntaxError, exceptions.TemplateError) as e:
        return "Syntax error in jinja2 template: {0}".format(e)

    values = {}

    if request.form['type'] == "json":
        try:
            values = json.loads(request.form['values'])
        except ValueError as e:
            return "Value error in JSON: {0}".format(e)

    elif request.form['type'] == "yaml":
        try:
            values = yaml.load(
                stream=request.form['values'],
                Loader=Loader
            )
        except (ValueError, yaml.parser.ParserError, TypeError) as e:
            return "Value error in YAML: {0}".format(e)
    else:
        return "Undefined input_type: {0}".format(request.form['type'])

    try:
        rendered_jinja2_tpl = jinja2_tpl.render(values)
    except (exceptions.TemplateRuntimeError, ValueError, TypeError) as e:
        return "Error in your values input filed: {0}".format(e)

    return escape(rendered_jinja2_tpl).replace('\n', '<br />')

@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.form.get("title")
        template = request.form.get("template")
        values = request.form.get("values")
        tab_id = request.form.get("tab_id")

        if not title or not template or not values:
            return "Missing title, template or values", 400

        # Charger les onglets existants depuis les cookies
        encoded_custom_tabs = request.cookies.get("custom_tabs")
        custom_tabs = json.loads(base64.b64decode(encoded_custom_tabs).decode()) if encoded_custom_tabs else []

        if tab_id:
            # Mettre à jour l'onglet
            try:
                custom_tabs[int(tab_id)] = {
                    "title": title,
                    "template": template,
                    "values": values
                }
            except KeyError:
                return "Tab not found", 404
        else:
            # Ajouter un nouvel onglet
            custom_tabs.append({
                "title": title,
                "template": template,
                "values": values
            })

        # Sauvegarder les onglets dans les cookies
        encoded_custom_tabs = base64.b64encode(json.dumps(custom_tabs).encode()).decode('utf-8')
        response = make_response(json.dumps({"tab_id": len(custom_tabs) - 1}))
        response.set_cookie("custom_tabs", encoded_custom_tabs)

        return response

    return render_template('add_tab.html')

@app.route('/get-tab', methods=['POST'])
def get():
    tab_id = request.form.get("tab_id")

    if not tab_id:
        return "Missing tab_id", 400

    # Charger les onglets depuis les cookies
    encoded_custom_tabs = request.cookies.get("custom_tabs")
    custom_tabs = json.loads(base64.b64decode(encoded_custom_tabs).decode()) if encoded_custom_tabs else []

    try:
        tab = custom_tabs[int(tab_id)]
    except KeyError:
        return "Tab not found", 404

    return json.dumps(tab)

@app.route('/del-tab', methods=['POST'])
def delete():
    tab_id = request.form.get("tab_id")

    if not tab_id:
        return "Missing tab_id", 400

    # Charger les onglets depuis les cookies
    encoded_custom_tabs = request.cookies.get("custom_tabs")
    custom_tabs = json.loads(base64.b64decode(encoded_custom_tabs).decode()) if encoded_custom_tabs else []

    # Supprimer l'onglet
    try:
        del custom_tabs[int(tab_id)]
    except KeyError:
        return "Tab not found", 404

    # Sauvegarder les onglets dans les cookies
    encoded_custom_tabs = base64.b64encode(json.dumps(custom_tabs).encode()).decode('utf-8')
    response = make_response(redirect(url_for('home')))
    response.set_cookie("custom_tabs", encoded_custom_tabs)

    return response


app.run(debug=True)