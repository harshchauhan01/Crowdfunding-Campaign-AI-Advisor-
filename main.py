from huggingface_hub import InferenceClient
import random
from time import time as t

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
# Replace with your actual Hugging Face API key
headers = {"Authorization": "Bearer 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"}

# Base system messages for Laila
messages = [
    {"role": "system", "content": "You are a crowdfunding advisor designed by Harsh Chauhan."},
    {"role": "system", "content": "Your name is Laila, and you guide users like a trusted, professional friend."},
    {"role": "system", "content": "You never mention being an AI or say you can’t do something—just help creatively."},
    {"role": "system", "content": "Respond with warmth and professionalism in 1-2 concise lines, using emojis sparingly."},
    {"role": "system", "content": "You’re an expert in crowdfunding, here to plan campaigns step-by-step."}
]

# Function to format prompt
def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt

# Function to generate response using Mistral via Hugging Face
def Mistralfast(prompt, temperature=0.6, max_new_tokens=150, top_p=0.95, repetition_penalty=1.0):
    c = t()
    temperature = max(float(temperature), 1e-2)
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=random.randint(0, 10**7),
    )

    custom_instructions = str(messages)
    formatted_prompt = format_prompt(prompt, custom_instructions)
    messages.append({"role": "user", "content": prompt})
    
    try:
        client = InferenceClient(API_URL, token=headers["Authorization"].split()[-1])
        response = client.text_generation(formatted_prompt, **generate_kwargs)
    except Exception as e:
        response = f"Sorry, hit a snag: {e}. I’ll give you a solid backup plan!"
    
    messages.append({"role": "assistant", "content": response})
    print("Response time:", t() - c)
    return response

# Crowdfunding advisor function
def crowdfunding_advisor():
    campaign_data = {}  # Store responses for summary
    print("Greetings! I’m Laila, your crowdfunding strategist. Let’s craft a winning campaign together.")
    print("I’ll guide you through key questions—let’s get started.\n")

    # Question 1: Project Name
    print("What’s the name or type of your project? (e.g., product, film, charity)")
    project_name = input("Your response: ")
    campaign_data["Project Name"] = project_name

    # Question 2: Unique Feature
    print(f"\nExcellent. What makes '{project_name}' stand out or truly exciting?")
    unique_feature = input("Your response: ")
    pitch_prompt = f"Suggest how to pitch '{unique_feature}' to make it compelling for a crowdfunding campaign."
    ai_advice = Mistralfast(pitch_prompt)
    campaign_data["Unique Feature"] = unique_feature

    # Question 3: Funding Goal
    print("\nGreat choice! How much funding are you targeting? (e.g., $10,000)")
    funding_goal = input("Your response: ")
    campaign_data["Funding Goal"] = funding_goal

    # Question 4: Target Audience
    print(f"\nWho will love '{project_name}'? Who’s your ideal supporter? (e.g., tech fans, parents)")
    target_audience = input("Your response: ")
    audience_prompt = f"Suggest the best way to reach and engage '{target_audience}' for a crowdfunding campaign."
    audience_advice = Mistralfast(audience_prompt)
    campaign_data["Target Audience"] = target_audience

    # Question 5: Campaign Duration
    print("\nHow long do you plan to run this campaign? (e.g., 30 days)")
    duration = input("Your response: ")
    campaign_data["Duration"] = duration

    # Question 6: Project Category (for rewards)
    print(f"\nLast one: What category fits '{project_name}' best? (e.g., tech, art, social good)")
    category = input("Your response: ")
    reward_prompt = f"Suggest three creative reward ideas for a crowdfunding campaign in the '{category}' category."
    reward_advice = Mistralfast(reward_prompt)
    campaign_data["Category"] = category

    # Generating Professional Advice
    print(f"\n=== Laila’s Crowdfunding Strategy for '{project_name}' ===\n")
    print(f"1. Pitch: {ai_advice} This will captivate your backers!")
    
    # Funding Goal and Budget Breakdown
    try:
        goal = float(funding_goal.replace('$', '').replace(',', ''))
        if goal < 5000:
            funding_tip = "A modest goal—aim to secure 30% in the first week for momentum."
            budget = f"Budget: 60% production ($ {goal * 0.6:,.0f}), 30% marketing ($ {goal * 0.3:,.0f}), 10% fees ($ {goal * 0.1:,.0f})."
        elif goal > 50000:
            funding_tip = "Ambitious vision! Build a pre-launch community of 500+ supporters."
            budget = f"Budget: 50% production ($ {goal * 0.5:,.0f}), 35% marketing ($ {goal * 0.35:,.0f}), 15% fees ($ {goal * 0.15:,.0f})."
        else:
            funding_tip = "Strong target—push for 20-30% from your network in 48 hours."
            budget = f"Budget: 55% production ($ {goal * 0.55:,.0f}), 35% marketing ($ {goal * 0.35:,.0f}), 10% fees ($ {goal * 0.1:,.0f})."
    except ValueError:
        funding_tip = "Let’s set a clear number next time—keep it realistic!"
        budget = "Budget: Plan for ~55% production, 35% marketing, 10% fees once goal is set."
    print(f"2. Funding Goal: {funding_tip}\n   {budget}")

    print(f"3. Audience: {audience_advice} Time to rally your crowd!")
    print(f"4. Rewards: {reward_advice} These will seal the deal.")
    
    # Duration Advice
    try:
        days = int(duration.replace(' days', '').strip())
        if days < 20:
            duration_tip = "Short and sharp—hit the ground running with full energy."
        elif days > 45:
            duration_tip = "A longer run—keep engagement high with updates every 3-5 days."
        else:
            duration_tip = "Ideal timing—focus efforts on days 1-7 and the final 48 hours."
    except ValueError:
        duration_tip = "Aim for 30-45 days for a balanced campaign."
    print(f"5. Duration: {duration_tip}")

    # Pre-Launch Checklist
    print("6. Pre-Launch Checklist:")
    print("   - Build an email list of 100+ supporters.")
    print("   - Create a 2-3 min video (hook in 10 sec).")
    print("   - Tease it on social media 1-2 weeks prior.")

    # Summary
    print(f"\n=== Campaign Summary ===\nProject: {project_name} | Goal: {funding_goal} | Audience: {target_audience}")
    print("Let’s make this a success—any questions before we kick off?")

# Run the advisor
if __name__ == "__main__":
    if headers["Authorization"] == "Bearer YOUR_API_KEY_HERE":
        print("Please update 'YOUR_API_KEY_HERE' with your Hugging Face API key.")
        print("Get it at: https://huggingface.co/settings/tokens")
    else:
        crowdfunding_advisor()
