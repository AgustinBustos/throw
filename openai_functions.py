from keys import openai_key
from pydantic import BaseModel
from openai import OpenAI
 
def get_job_links(html):
    client = OpenAI(api_key=openai_key)
    class JobDescriptions(BaseModel):
        jobs_name: str
        jobs_link: str


    class ListOfLinks(BaseModel):
        jobs_list: list[JobDescriptions]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract a list of url links and names of job postings where the job is related to Data Science, economics, statistics or econometrics. At minimum extract 6 urls."},
            {"role": "user", "content": html},
        ],
        response_format=ListOfLinks,
    )

    result = completion.choices[0].message.parsed.jobs_list
    return result

def get_easy_apply_xpath(html):
    client = OpenAI(api_key=openai_key)

    class XpathOfButtonForEasyApply(BaseModel):
        xpath_button: str

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Get the xpath of the easy apply button, notice that there maybe be more than one option but you have to distinguish wich one is the actually clickable one, i will pass that as an argument for selenium selector"},
            {"role": "user", "content": html},
        ],
        response_format=XpathOfButtonForEasyApply,
    )

    result = completion.choices[0].message.parsed.xpath_button
    return result
def get_answers(html):
    client = OpenAI(api_key=openai_key)


    class ListOfAnswers(BaseModel):
        answers: list[str]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": '''I will give you a list of HTML elements 
             from a form to complete, i will use selenium to complete element by element 
             using the following pseudo-code for i in result: if select_box:  select.select_by_visible_text(i) else: element.send_keys(i). Where result is the result of this function.
             With respect to the answer, i want to get the job, so respond positevly, in general use 2 to 4 years of experience when asked but answer only one number, and the expected salary is 3000000. Very important, if there is a Select tag, then you have to choose the text of one of the options.'''},
            {"role": "user", "content": html},
        ],
        response_format=ListOfAnswers,
    )

    result = completion.choices[0].message.parsed.answers
    return result
# print(get_job_links(html))
# print(len(jobers))