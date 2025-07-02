from flask import Flask, request, jsonify, render_template
import json
import hashlib
import hmac
from datetime import datetime
from config import Config
from models import GitHubEventDB, GitHubEvent
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = GitHubEventDB()

def verify_signature(payload_body, signature_header):
    """Verify the GitHub webhook signature"""
    if not Config.GITHUB_WEBHOOK_SECRET:
        return True  # Skip verification if no secret is configured
    
    if not signature_header:
        return False
    
    expected_signature = "sha256=" + hmac.new(
        Config.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return timestamp.strftime("%d %B %Y - %I:%M %p UTC")

def format_event_message(event):
    """Format event message according to requirements"""
    author = event.get('author', 'Unknown')
    timestamp = format_timestamp(event.get('timestamp'))
    
    if event['event_type'] == 'push':
        to_branch = event.get('to_branch', 'unknown')
        return f'"{author}" pushed to "{to_branch}" on {timestamp}'
    
    elif event['event_type'] == 'pull_request':
        from_branch = event.get('from_branch', 'unknown')
        to_branch = event.get('to_branch', 'unknown')
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    
    elif event['event_type'] == 'merge':
        from_branch = event.get('from_branch', 'unknown')
        to_branch = event.get('to_branch', 'unknown')
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    
    return f'Unknown event by "{author}" on {timestamp}'

@app.route('/')
def index():
    """Main UI page"""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    try:
        # Get the signature from headers
        signature = request.headers.get('X-Hub-Signature-256')
        
        # Verify the signature
        if not verify_signature(request.get_data(), signature):
            logger.warning("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 401
        
        # Get the event type
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            logger.warning("Empty payload received")
            return jsonify({"error": "Empty payload"}), 400
        
        logger.info(f"Received {event_type} event")
        
        # Process different event types
        event_data = None
        
        if event_type == 'push':
            event_data = GitHubEvent.create_push_event(payload)
        
        elif event_type == 'pull_request':
            action = payload.get('action')
            if action == 'closed' and payload.get('pull_request', {}).get('merged'):
                # This is a merge event
                event_data = GitHubEvent.create_merge_event(payload)
            elif action in ['opened', 'reopened']:
                # This is a pull request event
                event_data = GitHubEvent.create_pull_request_event(payload)
        
        # Store the event in database
        if event_data:
            result = db.insert_event(event_data)
            if result:
                logger.info(f"Successfully stored {event_data['event_type']} event")
                return jsonify({"message": "Event stored successfully"}), 200
            else:
                logger.error("Failed to store event in database")
                return jsonify({"error": "Failed to store event"}), 500
        else:
            logger.info(f"Ignoring {event_type} event with action: {payload.get('action', 'N/A')}")
            return jsonify({"message": "Event ignored"}), 200
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/events')
def get_events():
    """API endpoint to get recent events"""
    try:
        events = db.get_recent_events()
        formatted_events = []
        
        for event in events:
            formatted_event = {
                'id': event['_id'],
                'type': event['event_type'],
                'message': format_event_message(event),
                'timestamp': event['timestamp'].isoformat() if isinstance(event['timestamp'], datetime) else event['timestamp'],
                'repository': event.get('repository', 'Unknown')
            }
            formatted_events.append(formatted_event)
        
        return jsonify(formatted_events)
    
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG) 