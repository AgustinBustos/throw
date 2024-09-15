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

# print(get_job_links(html))
# print(len(jobers))