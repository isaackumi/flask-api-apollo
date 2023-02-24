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
    # query['q_organization_domains'] = "apollo.io\ngoogle.com"
    query['q_organization_domains'] = "apollo.io"
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
    
                "first_name","last_name","title", "company", "Company Names for Emails", "Email",
                "Email Status",  "Email Confidence", "Seniority", "Department", "Departments",
                "Contact Owner", "First Phone", "Work Direct Phone", "Home Phone", "Mobile Phone"
                "Corporate Phone", "Other Phone", "Stage","List", "Last Contacted", "Account Owner",
                "#Employees", "Industry","KeyWords","Person LinkedIn Url","Website", "company LinkedIn Url",
                "Facebook Url", "Twitter Url", "City", "State", "Country", 
                "Company Address"
                
            ]
    for person in range(len(people)):
        extracted_data.append([
             people[person].get('first_name'),
                    people[person].get('last_name'),
                    people[person].get('title'),
                    people[person].get('employment_history')[0].get('organization_name'),
                    people[person].get('employment_history')[0].get('organization_name'), # verify from api res again
                    people[person].get('email'),
                    people[person].get('email_status'),
                    people[person].get('extrapolated_email_confidence'),
                    people[person].get('seniority'),
                    [dept for dept in people[person].get('departments')],
                    "john.aacht@cloudfruition.com", # get auth user email
                    people[person].get('sanitized_phone'),
                    "",
                    "",
                    "",
                    people[person].get('sanitized_phone'),
                    "",
                    "Stage/NaN",
                    "List/NaN",
                    "NaN",
                    "john.aacht@cloudfruition.com", # get auth user email,
                    "#Employees",
                    "#Industry",
                    "#Keywords",
                    people[person].get('linkedin_url'),
                    "#Website url",
                    "#company linkedin url",
                    "#company Facebook url",
                    "#company twitter url",
                    people[person].get('city'),
                    people[person].get('state'),
                    people[person].get('country'),

                    



                    
        #             people[person].get('sanitized_phone'),
        #             people[person].get('linkedin_url'),
        #             people[person].get('photo_url'),
        #             people[person].get('twitter_url'),
        ])

    # filepath = os.path.join(app.root_path,'extracted_data/extracted_data.csv')
# save CSV to local machine
    with open(os.path.join(app.root_path,'extracted_data/extracted_data.csv'),'w', encoding='UTF8', newline="") as file:
                writer = csv.writer(file)
                print("Writing data to CSV.....")
                writer.writerow(csv_headers)
                writer.writerows(extracted_data)

# save CSV to S3 bucket

# TODO: return value should be the link to the file stored in s3 bucket
    return people



    
        








