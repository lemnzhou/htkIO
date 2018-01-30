#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:14:46 2018

@author: lemn
"""
import struct
import numpy as np

def htkread(filename):
    fid = open(filename, 'rb')
    readbytes = fid.read()
    fid.close()
    nframe = readbytes[0:4]
    nframe,= struct.unpack('i',bytes(reversed(nframe)))
    frate  = readbytes[4:8]
    frate, = struct.unpack('i',bytes(reversed(frate)))
    nfeat  = readbytes[8:10]
    nfeat, = struct.unpack('h',bytes(reversed(nfeat)))
    nfeat /= 4
    nfeat = int(nfeat)
    nframe = nframe
    data = np.zeros((nfeat,nframe))
    feakind = readbytes[10:12]
    feakind = struct.unpack('h',bytes(reversed(feakind)))
    feakind = int(feakind)
    startIndex = 12
    for i in range(nframe):
        for j in range(nfeat):
            value = readbytes[startIndex:startIndex+4]
            value, = struct.unpack('f',bytes(reversed(value)))
            data[j][i] = value
            startIndex += 4
    return [data,frate,feakind]

def htkwrite(htkfile, data, frate, feakind):
    f = open(htkfile,'wb')
    [ndim,nframe] = np.shape(data)
    nframeBytes = struct.pack('i',nframe)
    nframeBytes = bytes(reversed(nframeBytes))
    f.write(nframeBytes)
    frateBytes = bytes(reversed(struct.pack('i',frate)))
    f.write(frateBytes)
    ndimBytes = bytes(reversed(struct.pack('h',ndim*4)))
    f.write(ndimBytes)
    feakindBytes = bytes(reversed(struct.pack('h',feakind)))
    f.write(feakindBytes)
    for i in range(nframe):
        for j in range(ndim):
            value = data[j][i]
            valueBytes = bytes(reversed(struct.pack('f',value)))
            f.write(valueBytes)
    f.close()
    
    

if __name__ =='__main__':
    #test htkread
    htkfile = '/home/lemn/experiment/data/ASVspoof2017/cqt/dev/D_1000001.cqt.htk'
    txtfile = '/home/lemn/experiment/data/ASVspoof2017/cqt/dev/D_1000001.cqt.img'
    f = open(txtfile)
    lines = f.readlines()
    f.close()
    data1 = [[float(x) for x in line.strip().split(' ')] for line in lines]
    data2 = htkread(htkfile)
    
    #test htkwrite
    htkfile = 'htktest.htk'
    filename = '/home/lemn/experiment/data/ASVspoof2017/cqt/dev/D_1000001.cqt.htk'
#    f = open(filename)
#    lines = f.readlines()
#    f.close()
#    data = [[float(x) for x in line.strip().split(' ')] for line in lines]
    [data,frate,feakind] = htkread(filename)
    htkwrite(htkfile,data,frate,feakind)
    
