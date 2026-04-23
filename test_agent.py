import json
import agent

def run_sanity_check():
    print("Running sanity check...\n")
    
    test_prompt = "My order A1B2 arrived completely broken. Please refund my $50.00 immediately."
    print(f"User Input: '{test_prompt}'\n")

    try:
        response = agent.get_agent_response(test_prompt)
        print("Token Usage:")
        print(f"{response.output}\n")
        
        tool_call_detected = False
        for item in response.output:
            if item.type == "function_call":
                tool_call_detected = True
                print("Agent successfully triggered a tool call!")
                print(f"Tool executed: {item.name}")
                
                args = json.loads(item.arguments)
                print(f"Extracted arguments: {json.dumps(args)}")
                
        if not tool_call_detected:
            print("The agent ignored the tool.")
            print(f"Response: {response.output_text}")

    except Exception as e:
        print(f"Pipeline Error: {e}")

if __name__ == "__main__":
    run_sanity_check()
