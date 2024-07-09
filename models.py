#from langchain_community.llms import Ollama

#llm = Ollama(model="aya",temperature=0.001)
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def make_a_summary(feedback):
    
    complaint2=f'''
    الشكوي هي 
    "{feedback}"
    '''
    prompt=f"""
  أنت لبق باللغة العربية. قم بفهم الشكوى التاليه و تلخيصها في جملة واحدة بلغة رسمية  

  الشكوى المراد تلخيصها: {complaint2}

  1- لا تقم بالإجابة على سؤال

  2- لا تقم بإعطاء رأي او اقتراح أو  سؤال

  3- لا تقم بأي عميات رياضية

  4- فقط قم بتلخيص كلمات الشكوى

  """
    completion = client.chat.completions.create(
    model="bartowski/aya-23-8B-GGUF",
    messages=[
        {"role": "system", "content":prompt},
        {"role": "user", "content": complaint2}
     ],
    temperature=0.00001,
    )
    res = completion.choices[0].message.content
    return res

def make_a_classification(feedback):
    
    prompt=f"""
    الشكوى المراد تصنيفها: ```{feedback}```

    Instruction: قم بفهم كلمات النص السابق و تصنيفها الي واحده من الاختيارات التاليه
    0 - مشاكل وزارة النقل
    1 -  مشاكل وزارة الصحه
    2 - مشاكل وزارة الكهرباء و الماء
    3 - غير ذلك
    Notes:
    قم بكتابه رقم الاختيار فقط
    اذا كان النص يتحدث عن النقل و المشاكل المتعلقه بهم اختر 0
    اذا كان النص يتحدث عن الصحه او المعاقين و المشاكل المتعلقه بهم اختر 1
    اذا كان النص يتحدث عن الكهرباء او الماء و المشاكل المتعلقه بهم اختر 2
    اذا لم يكون النص  شكوى عن ما سبق اختر 3
    """
    completion = client.chat.completions.create(
    model="bartowski/aya-23-8B-GGUF",
    messages=[
            {"role": "system", "content":prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1,
        temperature=0.00001,
        )
    res = completion.choices[0].message.content
    return res