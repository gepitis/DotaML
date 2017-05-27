import dota2api,time,pickle

api = dota2api.Initialise("2FCB78DAFC1178FA4981A64F78CE46D1")
#mymatches1=api.get_match_history(account_id=76561198044313708 )

def search(lobby_type,matches):
    ret_matches=[]
    for m in matches:
        if m["lobby_type"]==lobby_type:
            ret_matches.append(m)

    return ret_matches

call=api.get_match_history(skill=3)
id = call['matches'][-1]['match_id']
matches=call['matches']
matches=search(7,matches)
for i in range(0,100):
    api = dota2api.Initialise("2FCB78DAFC1178FA4981A64F78CE46D1")
    call = api.get_match_history(skill=3,start_at_match_id=id-1)
    id = call['matches'][-1]['match_id']
    matches=matches+search(7,call['matches'])
    time.sleep(1)

with open('outfile','wb') as fp:
    pickle.dump(matches,fp)

#with open('outfile','rb') as fp:
#    itemlist=pickle.load(fp)



#matches2=api.get_match_history(start_at_match_id=id-1)

#next((item for item in matches if item['lobby_type']==8))