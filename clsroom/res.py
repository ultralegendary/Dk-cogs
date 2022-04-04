from datetime import date, timedelta


def create_dates(sdate, edate):
    sdate = date(*[int(i) for i in sdate.split(",")])  # start date
    edate = date(*[int(i) for i in edate.split(",")])  # end date
    print(sdate)
    delta = edate - sdate  # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        with open(r"g_class\resources\days.txt", "a") as f:
            f.write(",\n" + str(day) + ": ")
        print(day)


# mtech
mtech2 = {
    # "Day-1": ["DS", "CA", "OS-LAB", "OS-LAB"],
    # "Day-2": ["OOP", "DAA", "DS", "OS"],
    # "Day-3": ["OS", "CA", "DAA", "AC"],
    # "Day-4": ["DAA", "OOP", "AA-LAB", "AA-LAB"],
    # "Day-5": ["CA", "DS", "OOP-LAB", "OOP-LAB"],
    # "Day-6": ["OOP", "DS", "OS", "AC"],
}
mtech2_links = {
    "OS-LAB": "https://meet.google.com/lookup/gysmi2d4b2",
    "OS": "https://meet.google.com/lookup/f67mr7goeg",
    "OOP": " https://meet.google.com/lookup/bpecf37dx4",
    "OOP-LAB": "https://meet.google.com/lookup/f5kjz4yy2p",
    "DS": "https://meet.google.com/lookup/cqbwumwxii",
    "DAA": "https://meet.google.com/lookup/gm5kc24tch",
    "AA-LAB": "https://meet.google.com/lookup/hhqownlv75",
    "CA": "https://meet.google.com/lookup/gyrebbdgtd",
    "AC": "https://meet.google.com/lookup/b3mrxnc4ts",
}

# CSE 3b
cse3b_b1 = {
    "Day-1": ["VCD", "PL", "DA", "PE4"],
    "Day-2": ["OE1", "PE3", "CD-LAB", "CD-LAB"],
    "Day-3": ["PE4", "VCD", "PCD", "OE1"],
    "Day-4": ["PCD", "VCD", "PE3", "PL"],
    "Day-5": ["OE1", "PE3", "DA", "DA-LAB"],
    "Day-6": ["PCD", "PE4", "DA", "VCD-LAB"],
}
cse3b_b2 = {
    # "Day-1": ["PE4", "PL", "VCD", "DA"],
    # "Day-2": ["OE1", "PCD", "PE3", "DA-LAB"],
    # "Day-3": ["VCD", "PE3", "DA", "PCD"],
    # "Day-4": ["DA", "PE4", "PCD", "PL"],
    # "Day-5": ["OE1", "PE4", "VCD", "VCD-LAB"],
    # "Day-6": ["PE3", "OE1", "CD-LAB", "CD-LAB"],
}
cse3b1_links = {
    
    "OE1": "https://meet.google.com/yqr-zxie-rxs",
    "VCD": "https://meet.google.com/agu-kzaf-vkr",
    "VCD-LAB": "https://meet.google.com/agu-kzaf-vkr",
    "PE4": "https://meet.google.com/unr-yapc-zzf",
    "DA": "https://meet.google.com/qte-dfya-eyy",
    "DA-LAB": "https://meet.google.com/qte-dfya-eyy",
    "CD-LAB": "https://meet.google.com/gfd-avfv-hqc",
    "PE3": "https://meet.google.com/hqg-uttt-uyr",
    "PCD": "https://meet.google.com/ftv-tsnh-fir",
    "PL":"https://youtube.com/watch?v=dQw4w9WgXcQ",

}
cse3b2_links={

}
"""linkscse3c = {
    "TOC": "https://meet.google.com/lookup/cssg54qozm?authuser=1&hs=179",
    "DCN": "https://meet.google.com/lookup/gl7ckyp4je?authuser=1&hs=179",
    "DCN-LAB": "https://meet.google.com/lookup/a5ek2k3ykp?authuser=1&hs=179",
    "AI": "https://meet.google.com/lookup/abmcib32u2?authuser=1&hs=179",
    "AI-LAB": "https://meet.google.com/lookup/abmcib32u2?authuser=1&hs=179",
    "PE1": "https://meet.google.com/lookup/gnmgayz63c?authuser=1&hs=179",
    "MES": " https://meet.google.com/lookup/boyuqmfxqm?authuser=1&hs=179",
    "MES-LAB": "https://meet.google.com/lookup/gqfeoictnj?authuser=1&hs=179",
    "PE2": "https://meet.google.com/lookup/cy5q5hmd6e?authuser=1&hs=179",
    "Mini Project": "https://meet.google.com/lookup/eljjxxguwn?authuser=1&hs=179",
}
"""
# CSE 3c
cse3c_b1 = {
    # "Day-1": ["PE1", "PL", "AI", "MES"],
    # "Day-2": ["TOC", "PE2", "MES", "DCN-LAB"],
    # "Day-3": ["AI", "TOC", "DCN", "PE1"],
    # "Day-4": ["MES", "MES-LAB", "PE2", "PL"],
    # "Day-5": ["PE1", "PE2", "DCN", "AI-LAB"],
    # "Day-6": ["DCN", "AI", "TOC", "Mini Project"],
}
cse3c_b2 = {
    # "Day-1": ["AI", "PL", "PE1", "TOC"],
    # "Day-2": ["PE2", "TOC", "DCN", "AI-LAB"],
    # "Day-3": ["TOC", "PE2", "PE1", "MES"],
    # "Day-4": ["AI", "DCN-LAB", "DCN", "PL"],
    # "Day-5": ["DCN", "AI", "MES", "MES-LAB"],
    # "Day-6": ["PE2", "PE1", "MES", "Mini Project"],
}

cse3c_links = {
    "TOC": "https://meet.google.com/lookup/cssg54qozm?authuser=1&hs=179",
    "DCN": "https://meet.google.com/lookup/gl7ckyp4je?authuser=1&hs=179",
    "DCN-LAB": "https://meet.google.com/lookup/a5ek2k3ykp?authuser=1&hs=179",
    "AI": "https://meet.google.com/lookup/abmcib32u2?authuser=1&hs=179",
    "AI-LAB": "https://meet.google.com/lookup/abmcib32u2?authuser=1&hs=179",
    "PE1": "https://meet.google.com/lookup/gnmgayz63c?authuser=1&hs=179",
    "MES": " https://meet.google.com/lookup/boyuqmfxqm?authuser=1&hs=179",
    "MES-LAB": "https://meet.google.com/lookup/gqfeoictnj?authuser=1&hs=179",
    "PE2": "https://meet.google.com/lookup/cy5q5hmd6e?authuser=1&hs=179",
    "Mini Project": "https://meet.google.com/lookup/eljjxxguwn?authuser=1&hs=179",
}

# CSE 2c
cse2c_b1 = {
    "Day-1": ["WT", "TOC", "RVS", "DAA"],
    "Day-2": ["OOPJ", "TOC", "DBMS", "RVS"],
    "Day-3": ["OOPJ", "DAA", "WT", "OOPJ-LAB"],
    "Day-4": ["DBMS", "OOPJ", "DBMS-LAB", "DBMS-LAB"],
    "Day-5": ["WT", "DBMS", "RVS", "WT-LAB"],
    "Day-6": ["TOC", "DAA", "RVS-LAB", "RVS-LAB"],
}

cse2c_b2 = {
    "Day-1": ["DAA", "DBMS", "WT-LAB", "OOPJ-LAB"],
    "Day-2": ["DAA", "WT", "DBMS-LAB", "DBMS-LAB"],
    "Day-3": ["DBMS", "OOPJ", "RVS-LAB", "RVS-LAB"],
    "Day-4": ["TOC", "RVS", "WT", "TOC"],
    "Day-5": ["RVS", "TOC", "DAA", "OOPJ"],
    "Day-6": ["RVS", "DBMS", "WT", "OOPJ"],
}

cse2c1_links = {
    "MS": "https://meet.google.com/lookup/awwqw6otky?authuser=1&hs=179",
    "MS-LAB": "https://meet.google.com/lookup/awwqw6otky?authuser=1&hs=179",
    "CA": "https://meet.google.com/lookup/dihoecr5x6?authuser=1&hs=179",
    "DLD": "https://meet.google.com/irnpzjiduc",
    "DLD-LAB": "https://meet.google.com/lookup/gi4l2zqwgu",
    "CADS": "https://meet.google.com/lookup/foag677pqn",
    "CADS-LAB": "https://meet.google.com/lookup/fhechbx6ta",
    "SEM": "https://meet.google.com/lookup/gcwwhxssgp",
    "SEM-LAB": "https://meet.google.com/lookup/a5oudfavwj",
    "OS": "https://meet.google.com/pnwejxkxoy",
    "OS-LAB": "https://meet.google.com/kxadyxvhiy",
    "MC": "https://meet.google.com/lookup/hi6nyyrn5d",

    "OOPJ" : "https://meet.google.com/ehk-jirs-jan",
    "DAA" : "https://meet.google.com/yzt-iayi-yft",
    "OOPJ-LAB" : "https://meet.google.com/tug-okbf-zwq",
    "RVS" : "https://meet.google.com/fnq-isjg-puq",
    "RVS-LAB" : "https://meet.google.com/fnq-isjg-puq",
    "WT" : " https://meet.google.com/zfw-gyum-rai",
    "WT-LAB" : " https://meet.google.com/zfw-gyum-rai",
    "DBMS-LAB" : "https://meet.google.com/zor-ttut-yzd",
    "DBMS" : "https://meet.google.com/crn-rwwz-zut",
    "TOC" : "https://meet.google.com/aba-wixw-jkz",
}
cse2c2_links={
  "OOPJ" : "https://meet.google.com/ehk-jirs-jan",
  "DAA" : "https://meet.google.com/yzt-iayi-yft",
  "OOPJ-LAB" : "https://meet.google.com/tug-okbf-zwq",
  "RVS-LAB" : "https://meet.google.com/fnq-isjg-puq",
  "RVS" : "https://meet.google.com/fnq-isjg-puq",
  "WT" : " https://meet.google.com/zfw-gyum-rai",
  "WT-LAB" : " https://meet.google.com/zfw-gyum-rai",
  "DBMS" : "https://meet.google.com/crn-rwwz-zut",
  "TOC" : "https://meet.google.com/aba-wixw-jkz",
  "DBMS-LAB" : "https://meet.google.com/fbs-bmch-hza"
}



# AI
aids_b1 = {
    # time  9:15,10:15,11:30,12:30
    "Day-1": ["SE", "ML", "DCN", "RVS" ],
    "Day-2": ["RVS", "BE", "ML", "DCN" ],
    "Day-3": ["SE", "DWM", "ML-LAB", "ML-LAB",],
    "Day-4": ["BE", "DWM", "SE", "ML" ],
    "Day-5": ["CN-LAB", "CN-LAB", "RVS-LAB", "RVS-LAB"],
    "Day-6": ["DWM", "RVS", "BE", "DCN"],
}
aids_b2 = {
    "Day-1": ["ML", "DWM", "RVS", "BE"],
    "Day-2": ["DCN", "DWM", "SE", "ML"],
    "Day-3": ["CN-LAB", "CN-LAB", "DWM", "BE"],
    "Day-4": ["RVS", "BE", "DCN", "SE"],
    "Day-5": ["RVS-LAB", "RVS-LAB", "ML-LAB", "ML-LAB"],
    "Day-6": ["SE", "ML", "DCN", "RVS"],
}

aids2_links = {
    "MS": "https://meet.google.com/ubu-ppnj-bvc",
    "MS-LAB": "https://meet.google.com/ubu-ppnj-bvc",
    "OOP": "https://meet.google.com/qjp-uctf-gao",
    "OOP-LAB": "https://meet.google.com/ftd-bnzh-cmh",
    "MC": "https://meet.google.com/jvq-drjp-hwa",
    "DBMS": "https://meet.google.com/uvv-mypm-mbi",
    "DBMS-LAB": "https://meet.google.com/bne-dqig-ndh",
    "AI": "https://meet.google.com/trf-hgzj-cih",
    "DAA": "https://meet.google.com/dxr-erkg-ruc",
    "FOS": "https://meet.google.com/pcy-pzbk-she",
    "FOS-LAB": "https://meet.google.com/pcn-ibbc-hou",
    "NILL": "https://youtube.com/watch?v=dQw4w9WgXcQ",
    "DWM": "https://meet.google.com/kpv-zboh-vib",
    "BE":"https://meet.google.com/rty-cxke-etv",
    "DCN":"https://meet.google.com/vmd-eugo-xhu",
    "ML":"https://meet.google.com/zje-quqx-doq",
    "SE":"https://meet.google.com/wqa-nqnz-dke",
    "RVS":"https://meet.google.com/yyc-devv-wqh",
    "CN-LAB":"https://meet.google.com/rbh-yavb-wmu",
    "ML-LAB":"https://meet.google.com/dtd-dpnv-xxi",
    "RVS-LAB":"https://meet.google.com/yyc-devv-wqh",

}

day_order = {
    "2021-07-29": "Day-4",
    "2021-07-30": "Day-5",
    "2021-07-31": "Day-6",
    "2021-08-01": "Day-0",
    "2021-08-02": "Day-1",
    "2021-08-03": "Day-2",
    "2021-08-04": "Day-3",
    "2021-08-05": "Day-4",
    "2021-08-06": "Day-5",
    "2021-08-07": "Day-0",
    "2021-08-08": "Day-0",
    "2021-08-09": "Day-6",
    "2021-08-10": "Day-1",
    "2021-08-11": "Day-2",
    "2021-08-12": "Day-3",
    "2021-08-13": "Day-4",
    "2021-08-14": "Day-0",
    "2021-08-15": "Day-0",
    "2021-08-16": "Day-5",
    "2021-08-17": "Day-6",
    "2021-08-18": "Day-1",
    "2021-08-19": "Day-2",
    "2021-08-20": "Day-0",
    "2021-08-21": "Day-0",
    "2021-08-22": "Day-0",
    "2021-08-23": "Day-3",
    "2021-08-24": "Day-4",
    "2021-08-25": "Day-5",
    "2021-08-26": "Day-6",
    "2021-08-27": "Day-1",
    "2021-08-28": "Day-0",
    "2021-08-29": "Day-0",
    "2021-08-30": "Day-0",
    "2021-08-31": "Day-2",
    "2021-09-01": "Day-3",
    "2021-09-02": "Day-4",
    "2021-09-03": "Day-5",
    "2021-09-04": "Day-0",
    "2021-09-05": "Day-0",
    "2021-09-06": "Day-6",
    "2021-09-07": "Day-1",
    "2021-09-08": "Day-2",
    "2021-09-09": "Day-3",
    "2021-09-10": "Day-0",
    "2021-09-11": "Day-0",
    "2021-09-12": "Day-0",
    "2021-09-13": "Day-4",
    "2021-09-14": "Day-5",
    "2021-09-15": "Day-6",
    "2021-09-16": "Day-1",
    "2021-09-17": "Day-2",
    "2021-09-18": "Day-0",
    "2021-09-19": "Day-0",
    "2021-09-20": "Day-3",
    "2021-09-21": "Day-4",
    "2021-09-22": "Day-5",
    "2021-09-23": "Day-6",
    "2021-09-24": "Day-1",
    "2021-09-25": "Day-0",
    "2021-09-26": "Day-0",
    "2021-09-27": "Day-2",
    "2021-09-28": "Day-3",
    "2021-09-29": "Day-4",
    "2021-09-30": "Day-5",
    "2021-10-01": "Day-6",
    "2021-10-02": "Day-0",
    "2021-10-03": "Day-0",
    "2021-10-04": "Day-1",
    "2021-10-05": "Day-2",
    "2021-10-06": "Day-3",
    "2021-10-07": "Day-4",
    "2021-10-08": "Day-5",
    "2021-10-09": "Day-0",
    "2021-10-10": "Day-0",
    "2021-10-11": "Day-6",
    "2021-10-12": "Day-1",
    "2021-10-13": "Day-2",
    "2021-10-14": "Day-0",
    "2021-10-15": "Day-0",
    "2021-10-16": "Day-0",
    "2021-10-17": "Day-0",
    "2021-10-18": "Day-3",
    "2021-10-19": "Day-0",
    "2021-10-20": "Day-4",
    "2021-10-21": "Day-5",
    "2021-10-22": "Day-6",
    "2021-10-23": "Day-0",
    "2021-10-24": "Day-0",
    "2021-10-25": "Day-1",
    "2021-10-26": "Day-2",
    "2021-10-27": "Day-3",
    "2021-10-28": "Day-4",
    "2021-10-29": "Day-5",
    "2021-10-30": "Day-0",
    "2021-10-31": "Day-0",
    "2021-11-01": "Day-6",
    "2021-11-02": "Day-1",
    "2021-11-03": "Day-2",
    "2021-11-04": "Day-0",
    "2021-11-05": "Day-3",
    "2021-11-06": "Day-0",
    "2021-11-07": "Day-0",
    "2021-11-08": "Day-4",
    "2021-11-09": "Day-5",
    "2021-11-10": "Day-6",
    "2021-11-11": "Day-1",
    "2021-11-12": "Day-2",
    "2021-11-13": "Day-0",
    "2021-11-14": "Day-0",
    "2021-11-15": "Day-3",
    "2021-11-16": "Day-4",
    "2021-11-17": "Day-5",
    "2021-11-18": "Day-1",
    "2021-11-19": "Day-2",
    "2021-11-20": "Day-0",
    "2021-11-21": "Day-0",
    "2021-11-22": "Day-3",
    "2021-11-23": "Day-4",
    "2021-11-24": "Day-5",
    "2021-11-25": "Day-0",
    "2022-01-24": "Day-1",
    "2022-01-25": "Day-2",
    "2022-01-26": "Day-0",
    "2022-01-27": "Day-3",
    "2022-01-28": "Day-4",
    "2022-01-29": "Day-5",
    "2022-01-30": "Day-6",
    }
