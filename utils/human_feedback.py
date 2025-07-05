def ask_human_for_feedback(prompt, responses):
    print("Human Feedback Simulation")
    for i, (model, response) in enumerate(responses.items()):
        print(f"\n{i+1}. {model.upper()}:\n{response[:300]}...")

    choice = input("Enter number of best response [or press Enter to skip]: ")
    try:
        choice = int(choice)
        selected_model = list(responses.keys())[choice - 1]
        return selected_model
    except:
        return None
