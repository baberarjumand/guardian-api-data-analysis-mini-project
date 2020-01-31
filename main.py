# For the exercise, you can use any programming language you want to.
# However, we recommend using Python or R as it seems to be the easiest to solve the tasks with.
# Please use the Guardian Media Group Content API (https://open-platform.theguardian.com/).
# 1. Extract information about Boris Johnson.
# 2. Count the number of posted articles about Boris Johnson starting from 2018-01-01 until now.
# The output should contain two columns as shown below.
# Note: The number of articles might differ.
# Date Number of Articles
# 2018-01-01 3
# 2018-01-02 4
# 2018-01-03 2
# 3. Calculate the average over all days for the above-mentioned period of "Number of Articles"
# 4. In which section are the most articles written in?
# 5. Show the temporal development of the "Number of Articles" for the above-mentioned period.
# 6. Are there suspicious events in the time series studied?
# 7. If yes to Task 6, show these. Why are these unusual? You may want to define yourself what is (un)usual and demonstrate these.
# 8. Based on Task 1, what might be the root causes for the suspicious events?

# run 'pip install -r requirements.txt' to install dependencies
# find relevant documentation at 'https://open-platform.theguardian.com/'
# get your own API key at 'https://open-platform.theguardian.com/access/'

import datetime
import json
import os
from urllib.request import urlopen
import matplotlib.pyplot as plt


# global constants
API_KEY = "MY-API-KEY"
SEARCH_STRING = "boris johnson"
FROM_DATE = "2018-01-01"
PAGE_SIZE = 50


# global variables
dates_data = {}
sections_data = {}


def test_append():
    obj_a = [{
        'name': 'abc',
        'email': 'abc@abc.com'
    }]
    # write to file
    with open('json-data/data.json', 'w') as f:
        json.dump(obj_a, f, indent=2)
    obj_b = [{
        'name': 'def',
        'email': 'def@def.com'
    }]
    # read data from file
    with open('json-data/data.json') as json_file:
        data = json.loads(json_file.read())
    
    # append new data
    for obj in obj_b:
        data.append(obj)
    
    # write appended data back to file
    with open('json-data/data.json', 'w') as f:
        json.dump(data, f, indent=2)


# task 1
def retrieve_latest_dataset():
    query_string = SEARCH_STRING.replace(' ', '%20')
    url = "https://content.guardianapis.com/search?q=" \
          + query_string + "&from-date=" \
          + FROM_DATE + "&order-by=oldest" \
          + "&api-key=" + API_KEY \
          + "&page-size=" + str(PAGE_SIZE)
    response = urlopen(url)
    json_data = json.loads(response.read())
    number_of_pages = json_data['response']['pages']
    print('Beginning fetch operation, please wait until operation completes...')
    print('Number of pages of fetch: ' + str(number_of_pages))
    for current_page in range(1, number_of_pages+1):
        print('Fetching page number ' + str(current_page))
        url = "https://content.guardianapis.com/search?q=" \
              + query_string + "&from-date=" \
              + FROM_DATE + "&order-by=oldest" \
              + "&api-key=" + API_KEY \
              + "&page-size=" + str(PAGE_SIZE) \
              + "&page=" + str(current_page)
        response = urlopen(url)
        json_data = json.loads(response.read())
        if current_page == 1:
            # overwrite current data.json file with page 1 results
            with open('json-data/data.json', 'w') as f:
                json.dump(json_data['response']['results'], f, indent=2)
        else:
            # read current data.json file, and append to end of it
            with open('json-data/data.json') as json_file:
                data = json.loads(json_file.read())
            for result in json_data['response']['results']:
                data.append(result)
            with open('json-data/data.json', 'w') as f:
                json.dump(data, f, indent=2)
    print('Fetching data operation complete')


# task 2
def construct_results_set():
    print('Scanning local storage for dataset')
    with open('json-data/data.json') as json_file:
        data = json.loads(json_file.read())
    total_number_of_results = len(data)
    print('Number of results in local storage: ' + str(total_number_of_results))
    print('Initializing analysis...')
    for i in range(0, total_number_of_results):
        temp_date_time = datetime.datetime.strptime(data[i]['webPublicationDate'], "%Y-%m-%dT%H:%M:%S%z")
        temp_date = str(temp_date_time.date())
        if temp_date in dates_data.keys():
            dates_data[temp_date] = dates_data[temp_date] + 1
        else:
            dates_data[temp_date] = 1
    with open('results/results.txt', 'w') as file:
        file.write(json.dumps(dates_data, indent=2))
    print('Analysis complete for task 2, results stored in results/results.txt')


# task 3
def get_average_for_task_3():
    temp_list = dates_data.values()
    print('Average for task 3 = ' + str(sum(temp_list)/len(temp_list)))


# task 4
def get_max_section_for_task_4():
    with open('json-data/data.json') as json_file:
        data = json.loads(json_file.read())
    total_number_of_results = len(data)
    for i in range(0, total_number_of_results):
        temp_section = data[i]['sectionName']
        if temp_section in sections_data.keys():
            sections_data[temp_section] = sections_data[temp_section] + 1
        else:
            sections_data[temp_section] = 1
    temp_sorted = sorted(sections_data.items(), key=lambda kv: (kv[1], kv[0]))
    # print(temp_sorted)  # prints entire sorted list of sections
    print('Section with most articles (task 4): ' + str(temp_sorted.pop()))


# task 5
def generate_bar_chart_for_task_5():
    plt.subplots()
    plt.bar(dates_data.keys(), dates_data.values(), color='red')
    plt.xticks(" ")
    plt.show()


def main():
    if os.path.isfile('json-data/data.json'):
        with open('json-data/data.json') as json_file:
            data = json.loads(json_file.read())
        temp_date_time = datetime.datetime.strptime(data[len(data)-1]['webPublicationDate'], "%Y-%m-%dT%H:%M:%S%z")
        last_date_updated = str(temp_date_time.date())
        print('Local dataset last updated on ' + last_date_updated)
        print('To retrieve latest dataset, delete the data.json file and run script again')
        construct_results_set()
        get_average_for_task_3()
        get_max_section_for_task_4()
        generate_bar_chart_for_task_5()
    else:
        retrieve_latest_dataset()
        construct_results_set()


if __name__ == "__main__":
    main()
