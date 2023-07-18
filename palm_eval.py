import pprint
import google.generativeai as palm

palm.configure(api_key='AIzaSyCmpDSQdoPRCHas9YPU-ztGYgoYHRa3lyc')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
print(models)
model = models[0].name

def process_extracted_text(pmc_id, text):
    if len(text.encode('utf-8')) > 50000:
        print(f"File size for {pmc_id} is too large.")
    prompt=f'''{text}
    this is text from an article. Evaluate whether or not this is a benchmarking study based on the text that is given above
    if it is a benchmarking study then format your answer as 
    yes, {pmc_id} is a benchmarking study []
    inside [] should be all the tools that the study compared as part of the benchmarking study
    if it is not a benchmarking study format your answer as
    no, {pmc_id} is not a benchmarking study
    do not add anything extra to your response
    '''
    completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0.7,
    candidate_count=1,
    # The maximum length of the response
    max_output_tokens=70)

    print(completion.result)