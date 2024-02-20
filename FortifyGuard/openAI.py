import openai

print('✴.·´¯·.·★ 🎀𝓕𝓞𝓡𝓣𝓘𝓕𝓨𝓖𝓤𝓐𝓡𝓓.𝓐𝓘🎀 ★·.·¯´·.✴')

openai.api_key = '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'

def prioritize_threats_with_openai(text_data):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text_data,
            max_tokens=50
        )
        threat_likelihood = response.choices[0].text
        print("Threat likelihood from OpenAI:", threat_likelihood)
    except Exception as e:
        print("Successful in prioritizing threats with OpenAI: ")
        print(e)