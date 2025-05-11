from flask import Flask, request, jsonify
import ai
import json

app = Flask(__name__)

@app.route('/validate-ebook-review', methods=['POST'])
def validate_ebook_review():
    """
    Receives an AdmissionReview request for ebook reviews and always approves it.
    """
    try:
        admission_review = request.get_json()
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        return jsonify({
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": False,
                "uid": admission_review.get("request", {}).get("uid"),
                "status": {
                    "code": 400,
                    "message": "Failed to decode request body as JSON."
                }
            }
        }), 400

    request_info = admission_review.get("request")
    print("admission_review: ", admission_review)
    if not request_info:
        return jsonify({
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": False,
                "uid": admission_review.get("request", {}).get("uid"),
                "status": {
                    "code": 400,
                    "message": "Malformed AdmissionReview request: missing 'request' field."
                }
            }
        }), 400

    uid = request_info.get("uid")
    if not uid:
        print("Warning: Missing UID in the admission request.")

    # In a real scenario, you would perform your validation logic here
    # based on the content of the review (request_info.object).
    # For this example, we are simply always approving.

    try:
        result = ai.validate(admission_review)
    except Exception as e:
        print("Some problem with the robot:", e)

    allowed = result['allowed']
    message = result['motivation']
    if allowed:
        print("Allowing:", message)
    admission_response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": allowed,
            "uid": uid,
            "status": {
                "code": 200 if allowed else 403,
                "message": message,
            },
            # Optionally, you can patch the object here if this were a mutating webhook
            # "patchType": "JSONPatch",
            # "patch": "W3sib3AiOiAiYWRkIiwgInBhdGgiOiAiL3NwZWMvcG9ydHMvcG9ydCIsICJ2YWx1ZSI6IDg4ODh9XQ=="
        }
    }

    return jsonify(admission_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=('server.crt', 'server.key'))
