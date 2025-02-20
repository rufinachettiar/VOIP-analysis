
# coding: utf-8

# In[1]:

url="https://www.dropbox.com/home?preview=session_challenger_dropboxdownload.pcap"


# In[2]:

import urllib
urllib.urlretrieve(url, "/home/rufina/Documents/github-dropbox/rename/dropboxdownload.pcap")


# In[3]:

ls -l /home/rufina/Documents/github-dropbox/rename/session_challenger_dropboxdownload.pcap


# In[4]:

get_ipython().system(u'md5sum /home/rufina/Documents/github-dropbox/rename/session_challenger_dropboxdownload.pcap')


# In[5]:

get_ipython().system(u'tshark -v')


# In[6]:

get_ipython().system(u'tshark -n -r /home/rufina/Documents/github-dropbox/rename/session_challenger_dropboxdownload.pcap -T fields -Eheader=y -e frame.number -e frame.len > frame.len')


# In[7]:

get_ipython().system(u'head -10 frame.len')


# In[8]:

import pandas as pd


# In[9]:

df=pd.read_table("frame.len")


# In[10]:

df


# In[11]:

df["frame.len"].describe()


# In[12]:

get_ipython().magic(u'pylab inline')


# In[13]:

figsize(10,6)


# In[14]:

df["frame.len"].plot(style=".", alpha=0.2)
title("Frame length")
ylabel("bytes")
xlabel("frame number")


# In[15]:

import subprocess
import datetime
import pandas as pd

def read_pcap(filename, fields=[], display_filter="", 
              timeseries=False, strict=False):
    if timeseries:
        fields = ["frame.time_epoch"] + fields
    fieldspec = " ".join("-e %s" % f for f in fields)

    display_filters = fields if strict else []
    if display_filter:
        display_filters.append(display_filter)
    filterspec = "-R '%s'" % " and ".join(f for f in display_filters)

    options = "-r %s -n -T fields -Eheader=y" % filename
    cmd = "tshark %s %s %s" % (options, filterspec, fieldspec)
    proc = subprocess.Popen(cmd, shell = True, 
                                 stdout=subprocess.PIPE)
    if timeseries:
        df = pd.read_table(proc.stdout, 
                        index_col = "frame.time_epoch", 
                        parse_dates=True, 
                        date_parser=datetime.datetime.fromtimestamp)
    else:
        df = pd.read_table(proc.stdout)
    return df


# In[16]:

framelen=read_pcap("/home/rufina/Documents/github-dropbox/rename/session_challenger_dropboxdownload.pcap", ["frame.len"], timeseries=True)
framelen


# In[17]:

bytes_per_second=framelen.resample("S", how="sum")


# In[18]:

bytes_per_second.head()


# In[19]:

bytes_per_second.plot()


# In[20]:

fields=["tcp.stream", "ip.src", "ip.dst", "tcp.seq", "tcp.ack", "tcp.window_size", "tcp.len"]
ts=read_pcap("/home/rufina/Documents/github-dropbox/rename/session_challenger_dropboxdownload.pcap", fields, timeseries=True, strict=True)
ts


# In[42]:

stream=ts[ts["tcp.stream"] == 10]


# In[43]:

stream


# In[44]:

per_stream=ts.groupby("tcp.stream")
per_stream.head()


# In[45]:

bytes_per_stream = per_stream["tcp.len"].sum()
bytes_per_stream.head()


# In[46]:

bytes_per_stream.plot()


# In[47]:

bytes_per_stream.max()


# In[48]:

biggest_stream=bytes_per_stream.idxmax()
biggest_stream


# In[49]:

bytes_per_stream.ix[biggest_stream]


# In[ ]:



