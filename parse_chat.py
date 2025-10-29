#!/usr/bin/env python3
"""Parse and display GitHub Copilot chat.json as a readable conversation."""

import json
import sys

def format_conversation(chat_data):
    """Format the chat data as a readable conversation."""
    
    requester = chat_data.get('requesterUsername', 'User')
    responder = chat_data.get('responderUsername', 'Assistant')
    
    print(f"=== CONVERSATION: {requester} ⇄ {responder} ===\n")
    print(f"Location: {chat_data.get('initialLocation', 'unknown')}\n")
    print("=" * 70)
    
    requests = chat_data.get('requests', [])
    
    for idx, request in enumerate(requests, 1):
        print(f"\n{'─' * 70}")
        print(f"EXCHANGE #{idx}")
        print(f"{'─' * 70}\n")
        
        # Extract user message
        message = request.get('message', {})
        user_text = message.get('text', '').strip()
        
        if user_text:
            print(f"👤 {requester}:")
            print(f"{user_text}\n")
        
        # Extract assistant response
        response_parts = request.get('response', [])
        
        if response_parts:
            print(f"🤖 {responder}:")
            
            for part in response_parts:
                if isinstance(part, dict):
                    value = part.get('value', '')
                    if value and isinstance(value, str) and value.strip():
                        # Clean output - skip tool invocation messages
                        if not any(skip in value for skip in ['Reading', 'Read ', 'file:///']):
                            print(f"{value.strip()}\n")

def main():
    try:
        with open('chat.json', 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        
        format_conversation(chat_data)
        
    except FileNotFoundError:
        print("Error: chat.json not found in current directory")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
