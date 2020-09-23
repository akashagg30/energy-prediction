from subprocess import Popen,PIPE

# user name
user = "team07"

ps = Popen(['ps','aux'], stdout = PIPE)
ps = ps.communicate()[0]
grep = Popen(['grep',user], stdout = PIPE, stdin = PIPE)
output = grep.communicate(ps)[0].decode("utf-8")
output = output.split('\n')
data= {'cpu':0.0,'memory':0.0}
for x in output:
    info=list(filter(None,x.split(' ')))
    if(len(x)>1):
        data['cpu']+=float(info[2])
        data['memory']+=float(info[3])
print(data)