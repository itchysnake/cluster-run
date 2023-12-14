from flask import Flask, request
import search
import json
import gcs
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def event_handler():
    """
    Args:
    * query (str): search term to be scraped for NIFs

    Returns:
    * OK
    """

    # Receive and process payload
    payload = json.loads(request.data)
    query = payload.get("query")
    

    # Payload checks
    assert isinstance(query, str), "query not str"
    print("Payload received: ",query)

    # Retrieve and format
    cifs = search.google_search(query)
    data = "\n".join(cifs)

    # Save to Cloud Storage
    bucket = "cif-clusters"
    filename = query.replace(" ", "_") + ".csv"
    filename = filename.lower()
    gcs.upload(bucket, filename, data)

    return "OK", 200

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))