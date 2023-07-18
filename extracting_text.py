import PyPDF2

def extract_text_from_pdf_paths(pmc_id, paths):
    extracted_text = []
    if paths is None:
        return extracted_text
    
    # Function to extract text from a PDF file
    def extract_text_from_pdf(file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    
    for path in paths:
        text = extract_text_from_pdf(path)
        
        intro_start = None
        keywords = ['introduction', 'background', 'abstract']
        
        # Find the starting point of the desired text
        for keyword in keywords:
            keyword_index = text.lower().find(keyword)
            if keyword_index != -1:
                intro_start = keyword_index
                break
        
        ref_index = text.lower().find('references')
        
        # Extract the desired text and append it to the list
        if intro_start is not None and ref_index != -1:
            intro_text = text[intro_start:ref_index]
            extracted_text.append((pmc_id, intro_text))
    
    return extracted_text

