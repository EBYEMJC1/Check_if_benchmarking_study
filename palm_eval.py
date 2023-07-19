import pprint
import google.generativeai as palm

palm.configure(api_key='AIzaSyCmpDSQdoPRCHas9YPU-ztGYgoYHRa3lyc')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
print(models)
model = models[0].name

def process_extracted_text(pmc_id, text, tool_name):
    '''if len(text.encode('utf-8')) >= 49900:
        print(f"File size for {pmc_id} is too large.")
        return'''
    
    chunk_size = 30000  # Adjust the chunk size as needed
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    is_benchmarking = False
    tools_compared = []
    
    for chunk in chunks:
        prompt = f'''{chunk}
        This is text from an article. Evaluate whether or not this is a benchmarking study based on the text that is given above.
        If it is a benchmarking study, format your answer as:
        yes, {pmc_id} is a benchmarking study [tools compared]
        Inside [], include all the tools that the study compared as part of the benchmarking study.
        If it is not a benchmarking study, format your answer as:
        no, {pmc_id} is not a benchmarking study
        Do not add anything extra to your response.
        '''
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            candidate_count=1,
            # The maximum length of the response
            max_output_tokens=100
        )
        
        result = completion.result
        print(result)
        
        if result is not None and 'yes' in result:
            is_benchmarking = True
            tools = result.split('[', 1)[1].split(']', 1)[0]
            tools_compared.append(tools.strip())
    
    if is_benchmarking:
        with open(f"{tool_name}_responses.txt", "a", encoding="utf-8") as file:
            file.write(f"yes, {pmc_id} is a benchmarking study [{', '.join(tools_compared)}]\n")
    '''else:
        with open(f"{tool_name}_responses.txt", "a", encoding="utf-8") as file:
            file.write(f"no, {pmc_id} is not a benchmarking study\n")
'''