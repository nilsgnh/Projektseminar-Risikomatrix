# main.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/display', methods=['POST'])
def display():
    print("display")
    # aus Textfeld mit id "input" den Inhalt auslesen
    input_text = request.form['input']
    # Inhalt des Textfeldes in div mit id "output" schreiben
    return render_template("index.html", input=input_text)