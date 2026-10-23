from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Mock rule-based resolution engine (simulating AI log analysis)
def analyze_log_text(log_message):
    log_message_upper = log_message.upper()
    
    if "SLA_BREACH" in log_message_upper or "TIMEOUT" in log_message_upper:
        return {
            "issue_type": "Network / SLA Breach",
            "suggested_action": "Check network bandwidth or increase SLA timeout limits in Rubrik SLA domain settings.",
            "severity": "HIGH"
        }
    elif "STORAGE_FULL" in log_message_upper or "DISK_SPACE" in log_message_upper:
        return {
            "issue_type": "Storage Capacity Exceeded",
            "suggested_action": "Clean up older snapshots or expand cloud Blob storage quota.",
            "severity": "CRITICAL"
        }
    elif "AUTH_FAILED" in log_message_upper or "PERMISSION_DENIED" in log_message_upper:
        return {
            "issue_type": "Access Control Issue",
            "suggested_action": "Verify Azure IAM credentials and service principal permissions.",
            "severity": "MEDIUM"
        }
    else:
        return {
            "issue_type": "General System Warning",
            "suggested_action": "Review system event logs and re-trigger backup job manually.",
            "severity": "LOW"
        }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker/Cloud platforms"""
    return jsonify({"status": "Healthy", "service": "Cloud Log Analyzer"}), 200

@app.route('/api/analyze-log', methods=['POST'])
def analyze_log():
    """API endpoint to parse log text and output diagnostic summaries"""
    data = request.get_json()
    
    if not data or 'log_message' not in data:
        return jsonify({"error": "Missing 'log_message' in request body"}), 400
    
    raw_log = data.get('log_message')
    job_id = data.get('job_id', 'N/A')
    
    analysis = analyze_log_text(raw_log)
    
    response = {
        "job_id": job_id,
        "input_log": raw_log,
        "diagnostic_result": analysis
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)