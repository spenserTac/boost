import openpyxl
import csv
import datetime



# return data, total_views, year, month
def csv_parser(file):

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    time = datetime.datetime.now()

    year = time.year
    month = (time.month - 1) # For list above -> 10

    new_months = months[month:] + months[:month]
    new_months.append(months[month])

    try:
        reader = csv.reader(file)
        data_list = list(reader)



        nums = data_list[7:20]
        total_views = (str(data_list[20][1]))

        for l in nums:
            if l[1].find(',') != -1:

                s = l[1].replace(',', '')
                l[1] = s


        data = [list(map(int, lst)) for lst in nums]

        return data, total_views, year, new_months

    except:
        return None





#f = open('Analytics All Web Site Data Overview 20191001-20201001 (1).csv')
#data, total_views = csv_parser(f)

#print('Data: ', data, 'Total Views for the year: ', total_views)
#print(csv_parser(f))
