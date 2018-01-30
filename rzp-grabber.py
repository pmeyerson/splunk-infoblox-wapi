#!/usr/bin/python
# requires dnspython compliments dnspython.org; install via pip
import glob
import os
import difflib
import datetime
import dns.query
import dns.zone
import dns.tsigkeyring


#print("Begin execution at: " + str(datetime.datetime.today()))

mykeyhash ='' #api credential from csp.infoblox.com
host = '' # rpz distribution server IP from csp.infoblox.com
# enter the names of the Infoblox RPZ Feeds you are subscribed to here, listed in csp.infoblox.com  
feeds = ['base.rpz.infoblox.local','antimalware.rpz.infoblox.local','ransomware.rpz.infoblox.local']
mykeyname = '' # api credential from csp.infoblox.com

mykeyring = dns.tsigkeyring.from_text({ mykeyname : mykeyhash })
result_files = []

datestr = str(datetime.date.today())       # append datestring to each file
#Download dns zone feeds and write to file
for rpz in feeds:
        z = dns.zone.from_xfr(dns.query.xfr(host, rpz, keyname = mykeyname,keyring = mykeyring))
        filename = rpz + '_' + datestr + '.rpz'
        z.to_file(filename, sorted=True)
        result_files.append(filename)

# remove lines without domain names present and remove unnecessary text
for item in result_files:
        filename = "./" + item

        with open(filename, "r") as infile:
                with open(filename+".mod","w") as outfile:

                        for line in infile:
                                if "14400" in line:
                                        text=line.split(" 14400 IN")[0]+'\n'
                                        outfile.write(text)
                                        
# Use only the above code to write out daily rpz feed snapshots.

### historical diff --- may need more error checking.
with open("rpz_additions.csv","wb") as master_modfile:

        for item in result_files:
        # compute diff from yesterday for each rpz feed downloaded
                olddata = []
                newdata = []
                rpz_name = item.split('.')[0]
                with open(item+".mod","r") as newfile:
                        newdata=newfile.read().split('\n')

                # Find most recent (yesterday or prior) rpz file with same rpz_name
                files = glob.glob('./' + rpz_name + '*.mod')
                files.sort(key=os.path.getmtime, reverse=True)

                with open(files[1],"r") as oldfile:
                        olddata=oldfile.read().split('\n')

                print("Beginning compare of " + rpz_name + str(datetime.datetime.now())+ " " + oldfile.name + " " + newfile.name+"\n")

                oldset=set(sorted(olddata))
                newset=set(sorted(newdata))

                additions=newset-oldset
                removals=oldset-newset

                print(rpz_name + " " + str(len(additions)) + " additions:\n")
                print(rpz_name + " " + str(len(removals)) + " removals:\n")

                with open("additions." + newfile.name ,"wb") as rpz_additions:
                        while len(additions) > 0:
                                item=additions.pop()
                                # write additions for this rpz feed in a file
                                rpz_additions.write(str(item)+'\n')
                                # write additions to master file as well (all rpz feeds)
master_modfile.write(str(item)+'\n')
