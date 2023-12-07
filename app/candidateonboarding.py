import json
import openai
from config import OpenAI
 
class candidateonboarding:
 
    def gen_email(self):
        openai.api_type = OpenAI.API_TYPE
        openai.api_version = OpenAI.API_VERSION
        openai.api_base = OpenAI.API_BASE
        openai.api_key = OpenAI.API_KEY
 
        prompt = """
            Act as AI assistant and generate a email considering the below mentioned points:
            Important:
            1. Generate a email which shall be used to share a onboarding survey link.
            2. A field by the name of ["Survey Link"] only shall be given in which the survey link shall be pasted.
            3. Use the below mentioned details to generate the email. Recipient Name contains the name of the person to which the email is intented to share. The Sender company contains the name of the organization pn behalf of which the mail is shared. Timeframe contains the time by which the survey is expected to be filled.
 
            Recipient Name: [CandidateName]
            Timeframe: [Timeframe]
 
            In Sender Signature Please use the below mentioned details only
            Sender Name: [Name]
            Sender Position: [JobPosition]
            Sender Company: [CompanyName]
           
            Generate the email within 250 - 300 words """
 
        response = openai.ChatCompletion.create(
            engine="Eximius-Resume",
            messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information in specfied format only."},
            {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=5000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
            )  
 
        generated_text = response['choices'][0]['message']['content'].strip()
        body_start = generated_text.find("\n\n") + 2
 
        subject =  "Onboarding Survey for New Employee - Action Required"
        body = generated_text[body_start:].strip()
 
 
        return subject,body,generated_text,prompt
 
    def gen_survey(self):
        openai.api_type = OpenAI.API_TYPE
        openai.api_version = OpenAI.API_VERSION
        openai.api_base = OpenAI.API_BASE
        openai.api_key = OpenAI.API_KEY
 
        prompt = """
        Generate a set of questionnaire for onboarding which shall contain atleast 10 questions or 15 questions. The survey covers the following aspects:
        1. Pre-Onboarding Communication:
            a. Clarity of instructions provided before the first day
            b. Adequacy of information regarding background checks, documentation, and drug testing
        2. First Day Experience:
            a. Welcoming atmosphere and introductions to the team
            b.  Effectiveness of the orientation session
        3. Documentation and Setup:
            a. Ease of completing required documents
            b. Timeliness of receiving access credentials and IT setup
        4. Overall Support:
            a. Responsiveness of the onboarding team to questions or concerns
            b. Overall satisfaction with the onboarding process
        5. Feedback and Suggestions
 
        The questionnaire shall be formatted in below given json format only:
        {
            "surveyTitle": "Candidate Onboarding Survey",
            "questions": [
            {
                "questionId": 1,
                "questionText": "<question>",
                "responseType": "<response type>",
                "responseOptions": ["Response Options"]
            },
            {
                "questionId": 2,
                "questionText": "<question>",
                "responseType":"<response type>",
                "responseOptions": ["Response Options"]
            },
            {
                "questionId": 3,
                "questionText": "<question>",
                "responseType":"<response type>",
                "responseOptions": ["Response Options"]
            },
            {
                "questionId": N,
                "questionText": "<question>",
                "responseType": "<response type>",
                "responseOptions": ["Response Options"]
            }
            ]
        }
        IMPORTANT:
        1. The structure of the json shall always be maintained.
        2. Response Type can be ratings(multiple choics), Binary, user input.
        3. responseOption shall only contain the options and if it is a user input set it as [].
        4. The questionaire shall contain either 10 questions or 15 questions"""
 
        response = openai.ChatCompletion.create(
            engine="Eximius-Resume",
            messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information in specfied format only."},
            {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=5000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
            )  
 
        generated_text = json.loads(response['choices'][0]['message']['content'].strip())
        return generated_text,prompt
 
    def get_email(self):
        try:
            questionaire,surveyprompt = self.gen_survey()
            subject,body,response,mailprompt = self.gen_email()
            response = {
                "message":"Success",
                "messageList" : [{          
                "subject":subject,
                "body":body,
                "survey":questionaire,
                }],
                "response":None,
                "search_query": None,
                "prompt": [surveyprompt,mailprompt]
               
            }
            return response
        except Exception:
            response = {
                "message":"Failure",
                "messageList" : [{          
                "email": None,
                "subject":None,
                "body": None,
                "survey": {
                    "surveyTitle": None,
                    "questions": [
                    {
                        "questionId": None,
                        "questionText": None,
                        "responseOptions": [],
                        "responseType": None
                    }]    
                }
                }],
                "response":"Internal Server Issue",
                "search_query": None,
                "prompt": []
           
            }
            return response
       