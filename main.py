import dota2api,time,pickle




with open('outfile','rb') as fp:
    itemlist=pickle.load(fp)

x=2




#matches2=api.get_match_history(start_at_match_id=id-1)

#next((item for item in matches if item['lobby_type']==8))