import re

def pretty_print(stri,indent=2):
    sl =stri.split()
    F=filter(None, re.split("(,|{|})", stri))
    ret=""
    ind=0
    for s in F:
        if s=="{":
            ret+="{\n"
            ind+=1
            ret+=" "*(ind*indent)
        elif s==",":
            ret+=",\n"
            ret+=" "*(ind*indent)
        elif s=="}":
            ret+="}"
            ind-=1
            ind=max(ind,0)
        else:
            ret+=s.strip()
    return ret
    
S=pretty_print("{'_effective_message': {'supergroup_chat_created': False, 'date': 1534601386, 'delete_chat_photo': False, 'message_id': 44, 'caption_entities': [], 'photo': [], 'from': {'is_bot': False, 'first_name': 'Henrik', 'id': 557609229, 'language_code': 'de'}, 'chat': {'type': 'private', 'first_name': 'Henrik', 'id': 557609229}, 'new_chat_members': [], 'entities': [], 'channel_chat_created': False, 'new_chat_photo': [], 'text': 'Test', 'group_chat_created': False}, 'update_id': 358195587, 'message': {'supergroup_chat_created': False, 'date': 1534601386, 'delete_chat_photo': False, 'message_id': 44, 'caption_entities': [], 'photo': [], 'from': {'is_bot': False, 'first_name': 'Henrik', 'id': 557609229, 'language_code': 'de'}, 'chat': {'type': 'private', 'first_name': 'Henrik', 'id': 557609229}, 'new_chat_members': [], 'entities': [], 'channel_chat_created': False, 'new_chat_photo': [], 'text': 'Test', 'group_chat_created': False}}")
print(S)
