#!/usr/bin/env python

#func[0x00] = func_0x32  byte/buf 0x84

# This was created using via the following vim command from the comment block in the released source:
# :'<,'>normal 0dt[f]cf_,^[f c2f ,^[A],
data = [
    [0x00,0x32,0x84],
    [0x01,0x33,0x88],
    [0x02,0x34,0x8c],
    [0x03,0x35,0x90],
    [0x04,0x36,0x94],
    [0x05,0x37,0x98],
    [0x06,0x38,0x9c],
    [0x07,0x39,0xa0],
    [0x08,0x3a,0xa4],
    [0x09,0x3b,0xa8],
    [0x0a,0x3c,0xac],
    [0x0b,0x3d,0xb0],
    [0x0c,0x3e,0xb4],
    [0x0d,0x3f,0xb8],
    [0x0e,0x40,0xbc],
    [0x0f,0x41,0xc0],
    [0x10,0x42,0xc4],
    [0x11,0x43,0xc8],
    [0x12,0x44,0xcc],
    [0x13,0x45,0xd0],
    [0x14,0x46,0xd4],
    [0x15,0x47,0xd8],
    [0x16,0x48,0xdc],
    [0x17,0x49,0xe0],
    [0x18,0x4a,0xe4],
    [0x19,0x4b,0xe8],
    [0x1a,0x4c,0xec],
    [0x1b,0x4d,0xf0],
    [0x1c,0x4e,0xf4],
    [0x1d,0x4f,0xf8],
    [0x1e,0x50,0xfc],
    [0x1f,0x51,0x00],
    [0x20,0x52,0x04],
    [0x21,0x53,0x08],
    [0x22,0x54,0x0c],
    [0x23,0x55,0x10],
    [0x24,0x56,0x14],
    [0x25,0x57,0x18],
    [0x26,0x58,0x1c],
    [0x27,0x59,0x20],
    [0x28,0x5a,0x24],
    [0x29,0x5b,0x28],
    [0x2a,0x5c,0x2c],
    [0x2b,0x5d,0x30],
    [0x2c,0x5e,0x34],
    [0x2d,0x5f,0x38],
    [0x2e,0x60,0x3c],
    [0x2f,0x61,0x40],
    [0x30,0x62,0x44],
    [0x31,0x63,0x48],
    [0x32,0x64,0x4c],
    [0x33,0x65,0x50],
    [0x34,0x66,0x54],
    [0x35,0x67,0x58],
    [0x36,0x68,0x5c],
    [0x37,0x69,0x60],
    [0x38,0x6a,0x64],
    [0x39,0x6b,0x68],
    [0x3a,0x6c,0x6c],
    [0x3b,0x6d,0x70],
    [0x3c,0x6e,0x74],
    [0x3d,0x6f,0x78],
    [0x3e,0x70,0x7c],
    [0x3f,0x71,0x80],
    [0x40,0x72,0x84],
    [0x41,0x73,0x88],
    [0x42,0x74,0x8c],
    [0x43,0x75,0x90],
    [0x44,0x76,0x94],
    [0x45,0x77,0x98],
    [0x46,0x78,0x9c],
    [0x47,0x79,0xa0],
    [0x48,0x7a,0xa4],
    [0x49,0x7b,0xa8],
    [0x4a,0x7c,0xac],
    [0x4b,0x7d,0xb0],
    [0x4c,0x7e,0xb4],
    [0x4d,0x7f,0xb8],
    [0x4e,0x80,0xbc],
    [0x4f,0x81,0xc0],
    [0x50,0x82,0xc4],
    [0x51,0x83,0xc8],
    [0x52,0x84,0xcc],
    [0x53,0x85,0xd0],
    [0x54,0x86,0xd4],
    [0x55,0x87,0xd8],
    [0x56,0x88,0xdc],
    [0x57,0x89,0xe0],
    [0x58,0x8a,0xe4],
    [0x59,0x8b,0xe8],
    [0x5a,0x8c,0xec],
    [0x5b,0x8d,0xf0],
    [0x5c,0x8e,0xf4],
    [0x5d,0x8f,0xf8],
    [0x5e,0x90,0xfc],
    [0x5f,0x91,0x00],
    [0x60,0x92,0x04],
    [0x61,0x93,0x08],
    [0x62,0x94,0x0c],
    [0x63,0x95,0x10],
    [0x64,0x96,0x14],
    [0x65,0x97,0x18],
    [0x66,0x98,0x1c],
    [0x67,0x99,0x20],
    [0x68,0x9a,0x24],
    [0x69,0x9b,0x28],
    [0x6a,0x9c,0x2c],
    [0x6b,0x9d,0x30],
    [0x6c,0x9e,0x34],
    [0x6d,0x9f,0x38],
    [0x6e,0xa0,0x3c],
    [0x6f,0xa1,0x40],
    [0x70,0xa2,0x44],
    [0x71,0xa3,0x48],
    [0x72,0xa4,0x4c],
    [0x73,0xa5,0x50],
    [0x74,0xa6,0x54],
    [0x75,0xa7,0x58],
    [0x76,0xa8,0x5c],
    [0x77,0xa9,0x60],
    [0x78,0xaa,0x64],
    [0x79,0xab,0x68],
    [0x7a,0xac,0x6c],
    [0x7b,0xad,0x70],
    [0x7c,0xae,0x74],
    [0x7d,0xaf,0x78],
    [0x7e,0xb0,0x7c],
    [0x7f,0xb1,0x80],
    [0x80,0xb2,0x84],
    [0x81,0xb3,0x88],
    [0x82,0xb4,0x8c],
    [0x83,0xb5,0x90],
    [0x84,0xb6,0x94],
    [0x85,0xb7,0x98],
    [0x86,0xb8,0x9c],
    [0x87,0xb9,0xa0],
    [0x88,0xba,0xa4],
    [0x89,0xbb,0xa8],
    [0x8a,0xbc,0xac],
    [0x8b,0xbd,0xb0],
    [0x8c,0xbe,0xb4],
    [0x8d,0xbf,0xb8],
    [0x8e,0xc0,0xbc],
    [0x8f,0xc1,0xc0],
    [0x90,0xc2,0xc4],
    [0x91,0xc3,0xc8],
    [0x92,0xc4,0xcc],
    [0x93,0xc5,0xd0],
    [0x94,0xc6,0xd4],
    [0x95,0xc7,0xd8],
    [0x96,0xc8,0xdc],
    [0x97,0xc9,0xe0],
    [0x98,0xca,0xe4],
    [0x99,0xcb,0xe8],
    [0x9a,0xcc,0xec],
    [0x9b,0xcd,0xf0],
    [0x9c,0xce,0xf4],
    [0x9d,0xcf,0xf8],
    [0x9e,0xd0,0xfc],
    [0x9f,0xd1,0x00],
    [0xa0,0xd2,0x04],
    [0xa1,0xd3,0x08],
    [0xa2,0xd4,0x0c],
    [0xa3,0xd5,0x10],
    [0xa4,0xd6,0x14],
    [0xa5,0xd7,0x18],
    [0xa6,0xd8,0x1c],
    [0xa7,0xd9,0x20],
    [0xa8,0xda,0x24],
    [0xa9,0xdb,0x28],
    [0xaa,0xdc,0x2c],
    [0xab,0xdd,0x30],
    [0xac,0xde,0x34],
    [0xad,0xdf,0x38],
    [0xae,0xe0,0x3c],
    [0xaf,0xe1,0x40],
    [0xb0,0xe2,0x44],
    [0xb1,0xe3,0x48],
    [0xb2,0xe4,0x4c],
    [0xb3,0xe5,0x50],
    [0xb4,0xe6,0x54],
    [0xb5,0xe7,0x58],
    [0xb6,0xe8,0x5c],
    [0xb7,0xe9,0x60],
    [0xb8,0xea,0x64],
    [0xb9,0xeb,0x68],
    [0xba,0xec,0x6c],
    [0xbb,0xed,0x70],
    [0xbc,0xee,0x74],
    [0xbd,0xef,0x78],
    [0xbe,0xf0,0x7c],
    [0xbf,0xf1,0x80],
    [0xc0,0xf2,0x84],
    [0xc1,0xf3,0x88],
    [0xc2,0xf4,0x8c],
    [0xc3,0xf5,0x90],
    [0xc4,0xf6,0x94],
    [0xc5,0xf7,0x98],
    [0xc6,0xf8,0x9c],
    [0xc7,0xf9,0xa0],
    [0xc8,0xfa,0xa4],
    [0xc9,0xfb,0xa8],
    [0xca,0xfc,0xac],
    [0xcb,0xfd,0xb0],
    [0xcc,0xfe,0xb4],
    [0xcd,0xff,0xb8],
    [0xce,0x00,0xbc],
    [0xcf,0x01,0xc0],
    [0xd0,0x02,0xc4],
    [0xd1,0x03,0xc8],
    [0xd2,0x04,0xcc],
    [0xd3,0x05,0xd0],
    [0xd4,0x06,0xd4],
    [0xd5,0x07,0xd8],
    [0xd6,0x08,0xdc],
    [0xd7,0x09,0xe0],
    [0xd8,0x0a,0xe4],
    [0xd9,0x0b,0xe8],
    [0xda,0x0c,0xec],
    [0xdb,0x0d,0xf0],
    [0xdc,0x0e,0xf4],
    [0xdd,0x0f,0xf8],
    [0xde,0x10,0xfc],
    [0xdf,0x11,0x00],
    [0xe0,0x12,0x04],
    [0xe1,0x13,0x08],
    [0xe2,0x14,0x0c],
    [0xe3,0x15,0x10],
    [0xe4,0x16,0x14],
    [0xe5,0x17,0x18],
    [0xe6,0x18,0x1c],
    [0xe7,0x19,0x20],
    [0xe8,0x1a,0x24],
    [0xe9,0x1b,0x28],
    [0xea,0x1c,0x2c],
    [0xeb,0x1d,0x30],
    [0xec,0x1e,0x34],
    [0xed,0x1f,0x38],
    [0xee,0x20,0x3c],
    [0xef,0x21,0x40],
    [0xf0,0x22,0x44],
    [0xf1,0x23,0x48],
    [0xf2,0x24,0x4c],
    [0xf3,0x25,0x50],
    [0xf4,0x26,0x54],
    [0xf5,0x27,0x58],
    [0xf6,0x28,0x5c],
    [0xf7,0x29,0x60],
    [0xf8,0x2a,0x64],
    [0xf9,0x2b,0x68],
    [0xfa,0x2c,0x6c],
    [0xfb,0x2d,0x70],
    [0xfc,0x2e,0x74],
    [0xfd,0x2f,0x78],
    [0xfe,0x30,0x7c],
    [0xff,0x31,0x80],
    ]

successor = lambda x: x[0]^x[2]
filterindex = lambda f, xs: list(filter(f, enumerate(xs)))

successors = [successor(x) for x in data]

findsuccessorsize = lambda size: filterindex(lambda x: data[x[1]][2] == size, successors)

x = filterindex(lambda x: x[1] == 0, successors)
y = filterindex(lambda x: data[x[1]][2] == 0, successors)
z = filterindex(lambda x: data[x[1]][2] == 0xd8, successors)

'''
In [8]: findsuccessorsize(0x90)
Out[8]: [(19, 195), (83, 131), (147, 67), (211, 3)]

In [9]: findsuccessorsize(0x88)
Out[9]: [(41, 1), (105, 65), (169, 129), (233, 193)]
'''

import IPython
IPython.embed()
