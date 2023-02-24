from flask import Flask, request as rq, jsonify
import requests
import json
import os
import csv
import pandas as pd

app = Flask(__name__)

API_KEY = "_MMrEbBZaxCKKJm_iPx3Zg"
API_URL = "https://api.apollo.io/v1/mixed_people/search"
@app.post("/contacts")
def get_contacts():
    post_data = rq.json
    query = {}
    query['api_key'] = API_KEY
    query['q_organization_domains'] = "apollo.io\ngoogle.com"
    query['page'] = post_data.get('page')
    query['page_titles'] = post_data.get('person_titles')
    response = requests.post(url=API_URL, json=query)
    response_data = response.json() if response.status_code == 200 else {}
    # return jsonify(response_data)



    #  Looop through data a save releveant information to csv file
    people = response_data.get('people')
    extracted_data = []
    csv_headers = [
    
                "first_name","last_name", "full_name","title","sanitized_phone","linkedin_url"
                ,"photo_url","twitter_url"
                
            ]
    for person in range(len(people)):
        extracted_data.append([
             people[person].get('first_name'),
                    people[person].get('last_name'),
                    people[person].get('name'),
                    people[person].get('title'),
                    people[person].get('sanitized_phone'),
                    people[person].get('linkedin_url'),
                    people[person].get('photo_url'),
                    people[person].get('twitter_url'),
        ])

    

    return extracted_data



    
        








