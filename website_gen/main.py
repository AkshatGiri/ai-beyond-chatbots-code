import openai
from typing import List, Dict
import re
import json

# Initialize OpenAI client
client = openai.OpenAI(api_key="<your-api-key>")

def parse_list_response(response: str) -> List[str]:
    # Remove code blocks if present
    cleaned_response = re.sub(r'```(?:python)?\n?(.*?)```', r'\1', response, flags=re.DOTALL)
    
    # Try to parse as JSON first
    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        pass
    
    # If JSON fails, try to eval (assuming it's a Python list representation)
    try:
        return eval(cleaned_response)
    except:
        pass
    
    # If all else fails, split by newlines and clean up
    return [item.strip() for item in cleaned_response.split('\n') if item.strip()]

def generate_pages(company_info: str) -> List[str]:
    prompt = f"Based on this company information: '{company_info}', generate 5 appropriate website page names. Return only a Python list of strings."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates website structures."},
            {"role": "user", "content": prompt}
        ]
    )
    return parse_list_response(response.choices[0].message.content)

def generate_sections(page: str) -> List[str]:
    prompt = f"For a website page titled '{page}', suggest 3-5 appropriate section names. Return only a Python list of strings."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates website structures."},
            {"role": "user", "content": prompt}
        ]
    )
    return parse_list_response(response.choices[0].message.content)

def generate_copy(section: str, company_info: str) -> str:
    prompt = f"Write a short paragraph of website copy for a section titled '{section}'. Some information about the company '{company_info}' Return only the paragraph text."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes website copy."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_sitemap(company_info: str) -> Dict[str, Dict[str, str]]:
    sitemap = {}
    pages = generate_pages(company_info)
    
    for page in pages:
        sitemap[page] = {}
        sections = generate_sections(page)
        for section in sections:
            copy = generate_copy(section, company_info)
            sitemap[page][section] = copy
    
    return sitemap

def main():
    company_info = input("Please enter information about your company: ")
    print("Generating...")
    sitemap = generate_sitemap(company_info)
    
    print("\nGenerated Sitemap:")
    for page, sections in sitemap.items():
        print(f"\n{page}:")
        for section, copy in sections.items():
            print(f"  {section}:")
            print(f"    {copy[:100]}...")  # Print first 100 characters of copy

if __name__ == "__main__":
    main()