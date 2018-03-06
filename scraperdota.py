import dota2api,time,pickle
import pandas as pd

api = dota2api.Initialise("2FCB78DAFC1178FA4981A64F78CE46D1")
#mymatches1=api.get_match_history(account_id=76561198044313708 )


player_list=['player' + str(i) for i in range(0,10)]
matches=pd.DataFrame(columns=player_list)
matches['radiant_win']=None
matches['match_id']=None
matches
skill=3#3<-very high skill
count=0
for i in range(0,100):
    time.sleep(60)
    print('iteration ' + str(i) + '\n')
    job=0
    while job==0:
        try:
            hist=api.get_match_history(skill=skill)
            job=1;
        except :
            print("Api connection error")
            time.sleep(20)

    id = hist['matches'][-1]['match_id']
    num_results=hist['num_results']
    for j in range(0,num_results):
        job=0
        while job==0:
            try:
                time.sleep(2)
                match=api.get_match_details(match_id=hist['matches'][j]['match_id'])
                job=1
            except:
                print("Api connection error")
                time.sleep(2)
               
        if match['game_mode']==22:
            matches.loc[count,player_list]= [match['players'][z]['hero_id'] for z in range(0,10)]
            matches.loc[count,['radiant_win','match_id']]=[match['radiant_win'],match['match_id']]            
            count=count+1
    
    
       
    while hist['num_results']>0:
        time.sleep(2)
        job=0
        while job==0:
            try:
                hist=api.get_match_history(skill=skill,start_at_match_id=id-1)
                job=1;
            except :
                print("Api connection error")
        if hist['num_results']>0:
            id = hist['matches'][-1]['match_id']
            num_results=hist['num_results']
            for j in range(0,num_results):
                 job=0
                 while job==0:
                     try:
                         time.sleep(2)
                         match=api.get_match_details(match_id=hist['matches'][j]['match_id'])
                         job=1
                     except:
                         print("Api connection error")
                         time.sleep(2)
               
                 if match['game_mode']==22:
                     matches.loc[count,player_list]= [match['players'][z]['hero_id'] for z in range(0,10)]
                     matches.loc[count,['radiant_win','match_id']]=[match['radiant_win'],match['match_id']]            
                     count=count+1



with open('matches','wb') as fp:
    pickle.dump(matches,fp)

#with open('outfile','rb') as fp:
#    itemlist=pickle.load(fp)



#matches2=api.get_match_history(start_at_match_id=id-1)

#next((item for item in matches if item['lobby_type']==8))
    
#sqnum = [hist['matches'][z]['match_seq_num'] for z in range(0,100)]
#hist_seq_num=api.get_match_history_by_seq_num(start_at_match_seq_num=min(sqnum))
#sqnum_new = [hist_seq_num['matches'][z]['match_seq_num'] for z in range(0,100)]
