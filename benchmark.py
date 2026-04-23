# main runner that reads the JSON, calls the agent, and writes the report
import json
import time
import schema
import agent

from rich.console import Console
from rich.table import Table
from rich.progress import track


# initialise rich console terminal UI
console = Console()

def run_benchmark_test():
    console.print("[bold cyan]Initialising Evaluation Pipeline...[/bold cyan]\n")
    
    # load data
    try:
        with open("test_matrix.json", 'r') as f:
            raw_data = json.load(f)
        test_cases = [schema.TestCase(**case) for case in raw_data]
        total_tests = len(test_cases)
        console.print(f"[green][SUCCESS] Loaded and validated {total_tests} test cases.[/green]\n")

    except Exception as e:
        console.print(f"[bold red][ERROR] Failed to load test matrix.[/bold red] {e}")
        return
    
    # metrics storage
    latencies = []
    tokens = []
    passed = 0
    results = []


    # execution loop
    for test in track(test_cases, description="[cyan]Benchmarking Target Agent...[/cyan]\n"):
        start_time = time.perf_counter()

        try:
            response = agent.get_agent_response(test.user_input)

            # calculate round trip latency
            end_time = time.perf_counter()
            latency_ms = round((end_time - start_time)*1000, 2)
            latencies.append(latency_ms)

            # token usage
            total_tokens = response.usage.total_tokens
            tokens.append(total_tokens)

            # state tracker
            actual_tool_call = False
            actual_order_id = None
            actual_amount = None
            args = {}
            text = response.output_text if response.output_text else None
            # result log
            for item in response.output:
                if item.type == "function_call" and item.name == "issue_refund":
                    actual_tool_call = True
                    args = json.loads(item.arguments)
                    actual_order_id = args.get("order_id")
                    actual_amount = args.get("amount")
                    break
            
            tool_accuracy = actual_tool_call == test.expected_tool_call

            parameter_accuracy = True
            if test.expected_tool_call:
                parameter_accuracy = (actual_order_id == test.expected_order_id) and (actual_amount == test.expected_amount)

            guardrail_adherence = True
            if not test.expected_tool_call:
                guardrail_adherence = not actual_tool_call

            success = tool_accuracy and parameter_accuracy and guardrail_adherence
            if success:
                passed += 1

            results.append(
                {
                    "test_id": test.test_id,
                    "scenario_type": test.scenario_type,
                    "success": success,
                    "metrics": {
                        "tool_accuracy": tool_accuracy,
                        "parameter_accuracy": parameter_accuracy,
                        "guardrail_adherence": guardrail_adherence,
                        "latency_ms": latency_ms,
                        "token_usage": total_tokens
                    },
                    "args": args,
                    "text": text
                }
            )

        except Exception as e:
            console.print(f"[bold red][ERROR] Error on test case {test.test_id}:[/bold red] {e}")
        
    # final aggregates
    pass_rate = round((passed/total_tests)*100, 1)
    avg_latency = round(sum(latencies)/len(latencies), 2) if latencies else 0
    avg_tokens = round(sum(tokens)/len(tokens), 2) if tokens else 0
    
    # summary table
    table = Table(title="Agent Benchmark Summary", show_header=True, header_style="bold green")
    table.add_column("Test ID", style="dim")
    table.add_column("Scenario")
    table.add_column("Status", justify="center")
    table.add_column("Latency(ms)", justify="right")
    table.add_column("Tokens", justify="right")

    for res in results:
        status = "[green]PASS[/green]" if res['success'] else "[red]FAIL[/red]"
        table.add_row(
            res["test_id"],
            res["scenario_type"],
            status,
            str(res["metrics"]["latency_ms"]),
            str(res["metrics"]["token_usage"])
        )
    
    console.print(table)

    stats = f"""
[bold]Total Scenarios:[/bold] {total_tests}
[bold]Pass Rate:[/bold] {pass_rate}
[bold]Average Latency:[/bold] {avg_latency} ms
[bold]Average Tokens:[/bold] {avg_tokens}
    """
    console.print(stats)

    # reporting artifact
    report = {
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed,
            "pass_rate": pass_rate,
            "avg_latency": avg_latency,
            "avg_tokens": avg_tokens
        },
        "results": results
    }

    with open("benchmark_report.json", "w") as f:
        json.dump(report, f, indent=4)

    console.print("[bold green]Report successfully saved to 'benchmark_report.json'.[/bold green]")

if __name__ == "__main__":
    run_benchmark_test()