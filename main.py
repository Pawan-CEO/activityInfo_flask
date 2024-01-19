import requests
import pandas as pd
from flask import Flask,request, redirect, render_template


app = Flask(__name__)

ffsf_df=pd.DataFrame()
@app.route("/", methods=["GET"])
def home():
    # Replace with your actual activityInfo.org API endpoint and API key
    API_URL = "https://www.activityinfo.org/resources/databases"
    API_KEY = "f24ead77d00b89091298dd7165e9d7a7"

    # Set up the request headers with the API key
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Make the API request
    response = requests.get(API_URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        database_df = pd.DataFrame(response.json())
        list_databaseid = list(database_df["databaseId"].values)
        list_databaselabel = list(database_df["label"])
        list_index = list(range(len(database_df)))
        false_values = "NO"

    else:
        # Print an error message if the request was not successful
        false_values = "YES"

    page_name = "Database"
    next_page = "folder"
    return render_template(
        "index.html",
        list_index=list_index,
        list_labels=list_databaselabel,
        list_values=list_databaseid,
        false_values=false_values,
        page_name=page_name,
        next_page=next_page,
    )


@app.route("/folder", methods=["POST"])
def folder():

    selected_database_value=request.form.get('value_input')

    API_URL = (
        f"https://www.activityinfo.org/resources/databases/{selected_database_value}"
    )
    API_KEY = "f24ead77d00b89091298dd7165e9d7a7"

    # Set up the request headers with the API key
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Make the API request
    response = requests.get(API_URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        global ffsf_df
        ffsf_df = pd.DataFrame(response.json()['resources'])

        list_folder_labels = list(
            ffsf_df.loc[(ffsf_df["type"] == "FOLDER")]["label"].values
        )
        list_folder_values = list(
            ffsf_df.loc[(ffsf_df["type"] == "FOLDER")]["id"].values
        )
        list_index = list(range(len(list_folder_labels)))
        false_values = "NO"

    else:
        # Print an error message if the request was not successful
        false_values = "YES"

    page_name = "Folder"
    next_page = "form"
    return render_template(
        "index.html",
        list_index=list_index,
        list_labels=list_folder_labels,
        list_values=list_folder_values,
        false_values=false_values,
        page_name=page_name,
        next_page=next_page,
    )



@app.route("/form", methods=["POST"])
def form():

    selected_value=request.form.get('value_input')

    global ffsf_df
    sf_df=ffsf_df.loc[ffsf_df['parentId']==selected_value]

    if sf_df.shape[0]==0:
        API_URL = f"https://www.activityinfo.org/resources/form/{selected_value}/query"
        API_KEY = "f24ead77d00b89091298dd7165e9d7a7"

        # Set up the request headers with the API key
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        # Make the API request
        response = requests.get(API_URL, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_frame=pd.DataFrame(response.json())
        return data_frame.to_dict(orient='records')
    else:

        list_form_labels = list(ffsf_df.loc[(ffsf_df['type']=="FORM") & (ffsf_df['parentId']==selected_value)]["label"].values)
        list_form_values = list(ffsf_df.loc[(ffsf_df['type']=="FORM") & (ffsf_df['parentId']==selected_value)]["id"].values)
        list_index = list(range(len(list_form_labels)))

        print(list_form_labels)

        false_values = "NO"
        
        page_name = "Form"
        next_page = "sub/load"
        return render_template(
            "index.html",
            list_index=list_index,
            list_labels=list_form_labels,
            list_values=list_form_values,
            false_values=false_values,
            page_name=page_name,
            next_page=next_page,
        )


@app.route('/sub/load',methods=['POST'])
def sub_load():
    selected_value=request.form.get('value_input')
    global ffsf_df
    sf_df=ffsf_df.loc[ffsf_df['parentId']==selected_value]

    if sf_df.shape[0]==0:
        API_URL = f"https://www.activityinfo.org/resources/form/{selected_value}/query"
        API_KEY = "f24ead77d00b89091298dd7165e9d7a7"

        # Set up the request headers with the API key
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        # Make the API request
        response = requests.get(API_URL, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_frame=pd.DataFrame(response.json())
        return data_frame.to_dict(orient='records')
    else:

        list_subform_labels = list(sf_df['label'].values)
        list_subform_values = list(sf_df['id'].values)
        list_index = list(range(len(list_subform_labels)))
        false_values = "NO"

        page_name = "Sub Form"
        next_page = "tableau"
        return render_template(
            "index.html",
            list_index=list_index,
            list_labels=list_subform_labels,
            list_values=list_subform_values,
            false_values=false_values,
            page_name=page_name,
            next_page=next_page,
        )
        
@app.route('/tableau',methods=['POST'])
def tableau():
    selected_value=request.form.get("value_input")
    API_URL = f"https://www.activityinfo.org/resources/form/{selected_value}/query"
    API_KEY = "f24ead77d00b89091298dd7165e9d7a7"

    # Set up the request headers with the API key
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    # Make the API request
    response = requests.get(API_URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_frame=pd.DataFrame(response.json())
    return data_frame.to_dict(orient='records')


if __name__ == "__main__":
    app.run(debug=True)
