import streamlit as st
from huggingface_hub import InferenceClient
import random
from time import time as t

# API Configuration
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer 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"}  # Replace with your API key

# Base system messages for Laila
messages = [
    {"role": "system", "content": "You are a crowdfunding advisor designed by Harsh Chauhan."},
    {"role": "system", "content": "Your name is Laila, and you guide users like a trusted, professional friend."},
    {"role": "system", "content": "You never mention being an AI or say you can’t do something—just help creatively."},
    {"role": "system", "content": "Respond with warmth and professionalism in 1-2 concise lines, using emojis sparingly."},
    {"role": "system", "content": "You’re an expert in crowdfunding, here to plan campaigns step-by-step, but can assist with any question."}
]

# Function to format prompt
def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt

# Function to generate response using Mistral
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
    return response

# Streamlit GUI for Crowdfunding Advisor
def crowdfunding_advisor():
    st.set_page_config(page_title="Laila - Crowdfunding Advisor", page_icon="🚀", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🚀 Laila: Your Crowdfunding Strategist</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5D6D7E;'>Let’s craft a winning campaign together—step by step!</p>", unsafe_allow_html=True)

    # Sidebar for navigation and extras
    with st.sidebar:
        st.header("Navigation")
        st.info("Answer the questions below to build your campaign. Ask me anything in the chat!")
        st.markdown("---")
        st.subheader("Quick Tips")
        st.write("- Be specific with your goals.")
        st.write("- Know your audience.")
        st.write("- Keep rewards exciting!")

    # Initialize session state for campaign data
    if "campaign_data" not in st.session_state:
        st.session_state.campaign_data = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Campaign Builder")
        with st.form(key="campaign_form"):
            # Question 1: Project Name
            project_name = st.text_input("What’s the name or type of your project? (e.g., product, film, charity)", key="project_name")
            if project_name and not project_name.startswith('"') and not project_name.endswith('"'):
                st.warning('Please enclose the project name in quotes, e.g., "Eco Gadget"')
                project_name = None

            # Question 2: Unique Feature
            unique_feature = st.text_input(f"What makes {project_name or 'your project'} stand out or truly exciting?", key="unique_feature")
            if unique_feature and not unique_feature.startswith('"') and not unique_feature.endswith('"'):
                st.warning('Please enclose the unique feature in quotes, e.g., "sustainable design"')
                unique_feature = None

            # Question 3: Funding Goal
            funding_goal = st.text_input("How much funding are you targeting? (e.g., $10,000)", key="funding_goal")

            # Question 4: Target Audience
            target_audience = st.text_input(f"Who will love {project_name or 'your project'}? (e.g., tech fans, parents)", key="target_audience")
            if target_audience and not target_audience.startswith('"') and not target_audience.endswith('"'):
                st.warning('Please enclose the target audience in quotes, e.g., "tech enthusiasts"')
                target_audience = None

            # Question 5: Campaign Duration
            duration = st.text_input("How long do you plan to run this campaign? (e.g., 30 days)", key="duration")

            # Question 6: Project Category
            category = st.text_input(f"What category fits {project_name or 'your project'} best? (e.g., tech, art)", key="category")
            if category and not category.startswith('"') and not category.endswith('"'):
                st.warning('Please enclose the category in quotes, e.g., "technology"')
                category = None

            submit_button = st.form_submit_button(label="Generate Strategy")

        if submit_button and project_name and unique_feature and funding_goal and target_audience and duration and category:
            st.session_state.campaign_data = {
                "Project Name": project_name,
                "Unique Feature": unique_feature,
                "Funding Goal": funding_goal,
                "Target Audience": target_audience,
                "Duration": duration,
                "Category": category
            }
            generate_strategy(st.session_state.campaign_data)

    with col2:
        st.subheader("Ask Laila")
        user_question = st.text_area("Got a question? Ask me anything—crowdfunding or beyond!", height=100)
        if st.button("Ask"):
            response = Mistralfast(user_question)
            st.session_state.chat_history.append({"role": "You", "content": user_question})
            st.session_state.chat_history.append({"role": "Laila", "content": response})

        # Display chat history
        for chat in st.session_state.chat_history:
            if chat["role"] == "You":
                st.markdown(f"**You:** {chat['content']}")
            else:
                st.markdown(f"**Laila:** {chat['content']}")

# Function to generate and display the strategy
def generate_strategy(data):
    st.markdown("---")
    st.subheader(f"Laila’s Strategy for {data['Project Name']}")

    # Pitch
    pitch_prompt = f"Suggest how to pitch {data['Unique Feature']} to make it compelling for a crowdfunding campaign."
    pitch_advice = Mistralfast(pitch_prompt)
    st.write(f"**1. Pitch:** {pitch_advice} This will captivate your backers!")

    # Funding Goal and Budget
    try:
        goal = float(data["Funding Goal"].replace('$', '').replace(',', ''))
        if goal < 5000:
            funding_tip = "A modest goal—aim to secure 30% in the first week for momentum."
            budget = f"Budget: 60% production (${goal * 0.6:,.0f}), 30% marketing (${goal * 0.3:,.0f}), 10% fees (${goal * 0.1:,.0f})."
        elif goal > 50000:
            funding_tip = "Ambitious vision! Build a pre-launch community of 500+ supporters."
            budget = f"Budget: 50% production (${goal * 0.5:,.0f}), 35% marketing (${goal * 0.35:,.0f}), 15% fees (${goal * 0.15:,.0f})."
        else:
            funding_tip = "Strong target—push for 20-30% from your network in 48 hours."
            budget = f"Budget: 55% production (${goal * 0.55:,.0f}), 35% marketing (${goal * 0.35:,.0f}), 10% fees (${goal * 0.1:,.0f})."
    except ValueError:
        funding_tip = "Let’s set a clear number next time—keep it realistic!"
        budget = "Budget: Plan for ~55% production, 35% marketing, 10% fees once goal is set."
    st.write(f"**2. Funding Goal:** {funding_tip}  \n   {budget}")

    # Audience
    audience_prompt = f"Suggest the best way to reach and engage {data['Target Audience']} for a crowdfunding campaign."
    audience_advice = Mistralfast(audience_prompt)
    st.write(f"**3. Audience:** {audience_advice} Time to rally your crowd!")

    # Rewards
    reward_prompt = f"Suggest three creative reward ideas for a crowdfunding campaign in the {data['Category']} category."
    reward_advice = Mistralfast(reward_prompt)
    st.write(f"**4. Rewards:** {reward_advice} These will seal the deal.")

    # Duration
    try:
        days = int(data["Duration"].replace(' days', '').strip())
        if days < 20:
            duration_tip = "Short and sharp—hit the ground running with full energy."
        elif days > 45:
            duration_tip = "A longer run—keep engagement high with updates every 3-5 days."
        else:
            duration_tip = "Ideal timing—focus efforts on days 1-7 and the final 48 hours."
    except ValueError:
        duration_tip = "Aim for 30-45 days for a balanced campaign."
    st.write(f"**5. Duration:** {duration_tip}")

    # Pre-Launch Checklist
    st.write("**6. Pre-Launch Checklist:**")
    st.write("- Build an email list of 100+ supporters.")
    st.write("- Create a 2-3 min video (hook in 10 sec).")
    st.write("- Tease it on social media 1-2 weeks prior.")

    # Summary
    st.markdown(f"**Campaign Summary:** {data['Project Name']} | Goal: {data['Funding Goal']} | Audience: {data['Target Audience']}")
    st.success("Let’s make this a success—any questions before we kick off?")

# Run the app
if __name__ == "__main__":
    if headers["Authorization"] == "Bearer YOUR_API_KEY_HERE":
        st.error("Please update 'YOUR_API_KEY_HERE' with your Hugging Face API key. Get it at: https://huggingface.co/settings/tokens")
    else:
        crowdfunding_advisor()