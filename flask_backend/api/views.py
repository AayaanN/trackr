from flask import Blueprint, jsonify, request
import random

main = Blueprint('main', __name__)

@main.route('/add_data', methods=['POST'])

def add_data():


    return 'added'

@main.route('/get_data', methods = ['GET'])

def get_data():

    stocks = []

    return jsonify({'stocks':stocks})

