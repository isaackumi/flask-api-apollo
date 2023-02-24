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
    query['per_page'] = post_data.get('per_page')
    # print(query)
    response = requests.post(url=API_URL, json=query)
    response_data = response.json() if response.status_code == 200 else {}
    # return jsonify(response_data)



    #  Looop through data a save releveant information to csv file
    people = response_data.get('people')
    print(f" Type -> {type(people)}")
    print(f" All records -> {len(people)}")
    # print(f" People -> {people}")

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

    
# save CSV to local machine
    with open('{}.csv'.format('extracted_data'),'w', encoding='UTF8', newline="") as file:
                writer = csv.writer(file)
                print("Writing data to CSV.....")
                writer.writerow(csv_headers)
                writer.writerows(extracted_data)

# save CSV to S3 bucket

    return extracted_data



    
        








