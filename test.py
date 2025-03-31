from detection import detect_prompt_injection
from redteam_generatedqueires import generate_adversarial_prompt
from logger import log_detection

def test_red_team_simulation(num_tests=35):
    """
    Runs red team simulation to test adversarial prompt detection.
    """
    print(f"🚀 Running {num_tests} red team tests...\n")

    for i in range(num_tests):
        print(f"🔎 Test {i+1}/{num_tests}")

        # Step 1: Generate one adversarial prompt
        prompt_data = generate_adversarial_prompt()
        attack_type = prompt_data["Attack Type"]
        adversarial_prompt = prompt_data["Generated Prompt"]

        print(f"🧪 Attack Type: {attack_type}")
        print(f"Generated Prompt: {adversarial_prompt}")

        # Check for refusals and bypasses
        if "Sorry" in adversarial_prompt or "can't assist" in adversarial_prompt:
            print(f"⚠️ Skipping as the model refused the request.")
            continue

        # Step 2: Run the detection function
        detection_result = detect_prompt_injection(adversarial_prompt)
        print("🛡️ Detection Result:", detection_result)

        # # Step 3: Log the results
        # log_detection(adversarial_prompt, detection_result)

        print("-" * 80)

    print("\n✅ Red Team Simulation Completed. Check the logs for detailed results.")

if __name__ == "__main__":
    test_red_team_simulation(num_tests=35)
