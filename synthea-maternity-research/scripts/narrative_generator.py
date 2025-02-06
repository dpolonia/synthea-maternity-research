#!/usr/bin/env python3

import os
import pandas as pd
import openai

# If you have Anthropic's Python library installed, import it.
# Otherwise, you may have a custom implementation to call Anthropic's API.
try:
    import anthropic
except ImportError:
    anthropic = None

# Retrieve the API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# (Optional) Configure Anthropic if the library is available
anthropic_client = None
if ANTHROPIC_API_KEY and anthropic is not None:
    anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)


def generate_persona_narrative_with_openai(prompt: str) -> str:
    """
    Generate a persona narrative using OpenAI's API.
    """
    if not OPENAI_API_KEY:
        raise ValueError("No OpenAI API Key found in environment.")
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def generate_persona_narrative_with_anthropic(prompt: str) -> str:
    """
    Generate a persona narrative using Anthropic's API (Claude).
    """
    if not ANTHROPIC_API_KEY or anthropic_client is None:
        raise ValueError("No Anthropic API Key found, or anthropic library not installed.")
    
    # Anthropic usage may vary by version; adjust accordingly if needed
    response = anthropic_client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        max_tokens_to_sample=300,
        model="claude-v1",  # or your chosen Claude model variant
        temperature=0.7
    )
    # 'completion' contains the generated text
    return response["completion"].strip()


def main():
    # Example: Load data with cluster assignments
    df = pd.read_csv("data/clustered_data.csv")
    
    persona_reports = []

    for cluster_id in df["cluster"].unique():
        cluster_slice = df[df["cluster"] == cluster_id]
        
        # Summarize cluster characteristics (just an example)
        summary_stats = cluster_slice.describe(include="all").to_dict()
        
        # Create a prompt that includes the cluster stats
        prompt = f"""
        You are given the following cluster characteristics: {summary_stats}.
        Generate a persona that describes typical demographics, social context, 
        financial stress, emotional needs, and potential fears or doubts.
        """

        # Option 1: Use OpenAI
        try:
            openai_narrative = generate_persona_narrative_with_openai(prompt)
        except ValueError as e:
            openai_narrative = f"OpenAI error: {e}"

        # Option 2: Use Anthropic
        try:
            anthropic_narrative = generate_persona_narrative_with_anthropic(prompt)
        except ValueError as e:
            anthropic_narrative = f"Anthropic error: {e}"

        # Combine or choose one
        combined_narrative = f"**OpenAI**:\n{openai_narrative}\n\n**Anthropic**:\n{anthropic_narrative}"
        
        persona_reports.append({
            "cluster_id": cluster_id,
            "narrative": combined_narrative
        })

    # Save persona narratives to a CSV or JSON
    output_df = pd.DataFrame(persona_reports)
    output_df.to_csv("reports/persona_narratives.csv", index=False)
    print("Narratives generated and saved to reports/persona_narratives.csv.")


if __name__ == "__main__":
    main()
