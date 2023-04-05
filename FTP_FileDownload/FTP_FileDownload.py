import ftplib
import datetime



# ************************* Fuunctions ***********************
def string_date(date):                    # Return Date formt to String
    if (date.month<=9):
        month_str="0"+str(date.month)
    else:
        month_str=str(date.month)
    if (date.day<=9):
        day_str="0"+str(date.day)
    else:
        day_str=str(date.day)
    Day=str(date.year)+"_"+month_str+"_"+day_str
    return(Day)


def string_Todate(Day):                # Return String formt to Date
       Date=datetime.datetime(int(Day[0:4]), int(Day[5:7]), int(Day[8:10]))
       return(Date)


# ******************************** Data upload Interval *********************************
Day_back_ind=10
d=0
Sub_date=datetime.datetime.now() + datetime.timedelta(Day_back_ind)
Sub_date_days = string_date(Sub_date)
Currect_date=datetime.datetime.now()
Currect_date_day=string_date(Currect_date)

with open('Config.txt') as f:
    Config = f.readlines()

# We detect FTP Addrress in Config file
for config in Config:
    if (config[0:3]=='FTP'):

        FTP_Data = config
        Indexes = []
        Index = 0

        for ind in FTP_Data:

            if ind == '"':
                Indexes.append(Index)
            Index = Index + 1

        # Connecting to the FTP server
        FTP_Address = FTP_Data[Indexes[0] + 1:Indexes[1]]
        PORT = '21'
        FTP_USER = FTP_Data[Indexes[2] + 1:Indexes[3]]
        FTP_PASS = FTP_Data[Indexes[4] + 1:Indexes[5]]
        main_dir1 = FTP_Data[Indexes[6] + 1:Indexes[7]]


        while d<=Day_back_ind:
            Day_back=0-d
            Sub_date = datetime.datetime.now() + datetime.timedelta(Day_back)
            if d == 0:
                main_dir = main_dir1 + "//Today"                     # Download Toady Files
            else:
                main_dir= main_dir1 + "//" + string_date(Sub_date)   # Download Files with older Dates
            d = d + 1

            ftp = ftplib.FTP(FTP_Address, FTP_USER, FTP_PASS)
            ftp.encoding = "utf-8"

            ftp.cwd(main_dir)
            Folder_list = ftp.nlst()

            Reports = []
            for x in Config:
                if x[0:3] == 'FTP':
                    continue
                Candidate_File = x[0:len(x) - 1]


                Date_Vec = []

                NameFile_Len = len(Candidate_File)

                File_Name_Len = len(Candidate_File)
                for i in range(len(Folder_list)):

                    File_Name = Folder_list[i]
                    if (File_Name[0:File_Name_Len] == Candidate_File and NameFile_Len + 15 == len(File_Name)):
                        Reports.append(File_Name)


            Text_Log = open("D:\\Users\\AS0533288215\\PycharmProjects\\FTPDownload\\Log.txt", "r")

            for k in range(len(Reports)):
                filename = Reports[k]
                File_name_Log=filename[0:len(filename)-5]
                item_date = File_name_Log


                # If flag=1 it means that we have file in our database and log file
                flag = 0
                if (File_name_Log != ""):
                    for x in Text_Log:
                        item_old = x
                        if item_old[0:len(filename)-5] == File_name_Log:
                            flag = flag + 1
                            #item_date.append(item_date)
                            break

                # If flag=0 it means that we must add file in the text log file and also into the database
                if (flag == 0 and File_name_Log != ""):
                    with open(filename, 'wb') as file:
                        ftp.retrbinary(f'RETR {filename}', file.write)

                    with open('Log.txt', 'a+') as f:
                        f.write(File_name_Log)
                        f.write('\n')

        main_dir=main_dir1

        ftp = ftplib.FTP(FTP_Address, FTP_USER, FTP_PASS)
        ftp.encoding = "utf-8"

        ftp.cwd(main_dir)
        Folder_list = ftp.nlst()

        Reports = []

        for x in Config:
            if x[0:3] == 'FTP':
                continue
            Candidate_File = x[0:len(x) - 1]

            Date_Vec = []

            NameFile_Len = len(Candidate_File)

            File_Name_Len = len(Candidate_File)
            for i in range(len(Folder_list)):

                File_Name = Folder_list[i]
                if File_Name[len(File_Name)-15:len(File_Name)-14]!='2':   # due to remove some file names with wrong notations
                    continue
                File_Date=string_Todate(File_Name[len(File_Name)-15:len(File_Name)-5])

                if File_Date.date()>=Sub_date.date():
                    if (File_Name[0:File_Name_Len] == Candidate_File and NameFile_Len + 15 == len(File_Name)):
                        Reports.append(File_Name)

        Text_Log = open("D:\\Users\\AS0533288215\\PycharmProjects\\FTPDownload\\Log.txt", "r")

        for k in range(len(Reports)):
            filename = Reports[k]
            File_name_Log = filename[0:len(filename) - 5]
            item_date = File_name_Log

            # If flag=1 it means that we have file in our database and log file
            flag = 0
            if (File_name_Log != ""):
                for x in Text_Log:
                    item_old = x
                    if item_old[0:len(filename) - 5] == File_name_Log:
                        flag = flag + 1
                        # item_date.append(item_date)
                        break

            # If flag=0 it means that we must add file in the text log file and also into the database
            if (flag == 0 and File_name_Log != ""):
                with open(filename, 'wb') as file:
                    ftp.retrbinary(f'RETR {filename}', file.write)

                with open('Log.txt', 'a+') as f:
                    f.write(File_name_Log)
                    f.write('\n')

