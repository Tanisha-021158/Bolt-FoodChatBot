import re
def extract_session_id(session_id:str):
    match=re.search(r"/sessions/(.*?)/contexts/",session_id)
    if match:
        extracted_str=match.group(1)
        return extracted_str
    return ""

def get_str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key,value in food_dict.items()])




if __name__=="__main__":
    print(get_str_from_food_dict({"samosa":5,"chole bhature":2}))