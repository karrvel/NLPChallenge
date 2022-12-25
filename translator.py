import pdfplumber
from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize
from fpdf import FPDF

def extract(page):
  """Extract PDF text and Delete in-paragraph line breaks."""  

  # Get text  
  extracted = page.extract_text()  

  # Delete in-paragraph line breaks
  extracted = extracted.replace(".\n", "**/m" # keep par breaks
                      ).replace(". \n", "**/m" # keep par breaks
                      ).replace("\n", "" # delete in-par breaks     
                      ).replace("**/m", ".\n\n") # restore par break
  return extracted

def translate_extracted(Extracted):
  """Wrapper for Google Translate with upload workaround."""
  # Set-up and wrap translation client
  translate = GoogleTranslator(source='en', target='uz').translate  # Split input text into a list of sentences
  sentences = sent_tokenize(Extracted)  # Initialize containers
  translated_text = ''
  source_text_chunk = ''  # collect chuncks of sentences, translate individually
  for sentence in sentences:
    # if chunck + current sentence < limit, add the sentence
    if ((len(sentence.encode('utf-8')) +  len(source_text_chunk.encode('utf-8')) < 5000)):
      source_text_chunk += ' ' + sentence    # else translate chunck and start new one with current sentence
    else:
      translated_text += ' ' + translate(source_text_chunk)     # if current sentence smaller than 5000 chars, start new chunck
      if (len(sentence.encode('utf-8')) < 5000):
        source_text_chunk = sentence     # else, replace sentence with notification message
      else:
        message = "<<Omitted Word longer than 5000bytes>>"
        translated_text += ' ' + translate(message)       # Re-set text container to empty
        source_text_chunk = ''  # Translate the final chunk of input text, if there is any valid   text left to translate
  if translate(source_text_chunk) != None:
    translated_text += ' ' + translate(source_text_chunk)

  return translated_text

class Translate():
  def __init__(self):
    translate = GoogleTranslator(source='en', target='uz').translate

  async def to_Uz(self, file):
    # Open PDF
    with pdfplumber.open(file) as pdf:

      # Initialize FPDF file to write on
      fpdf = FPDF()
      fpdf.set_font("Helvetica", size = 11)  # Treat each page individually

      for page in pdf.pages:
        # Extract Page
        extracted = extract(page)    # Translate Page

        if extracted != "":
          # Translate paragraphs individually to keep breaks
          paragraphs = extracted.split("\n\n")
          translated = "\n\n".join(
            [translate_extracted(paragraph) for paragraph in paragraphs]
            )

        else:
          translated = extracted    # Write Page
 
        fpdf.add_page()
        fpdf.multi_cell(w=0, h=5,
                       txt= translated.encode("latin-1",
                                              errors = "replace"
                                     ).decode("latin-1")) # Save all FPDF pages
    fpdf.output(file[:-4] + "-uz.pdf")
    return file[:-4] + "-uz.pdf"