import requests
import datetime
import string


def load_schedule(id="rwl2", schedule_name="schedule"):
    schedule = requests.get("https://horaro.org/-/api/v1/events/"+id+"/schedules/"+schedule_name+"/ticker")
    if schedule.status_code == 200:
        schedule_json = schedule.json()
        cols = []
        for item in schedule_json['data']['schedule']['columns']:
            cols.append(item)
        get_current(schedule_json, cols)
        get_next(schedule_json, cols)
    else:
        print "Not found"


def get_current(schedule, columns):

    current_run = schedule['data']['ticker']['current']
    if current_run != None:
        run = {}
        run['estimate'] = str(datetime.timedelta(seconds=current_run['length_t']))
        for item in columns:
            run[item] = current_run['data'][columns.index(item)]
        print "Current run:\n", run
        generate_text(run, "current_")
    else:
        print "Current run not found"

def get_next(schedule, columns):

    next_run = schedule['data']['ticker']['next']
    if next_run != None:
        run = {}
        #run['estimate'] = str(datetime.timedelta(seconds=next_run['length_t']))
        for item in columns:
            run[item] = next_run['data'][columns.index(item)]
        print "Next run:\n", run
        generate_text(run, "next_")
    else:
        print "Next run not found"

def generate_text(run, prepend):
    for item in run:
        filename = prepend+item+".txt"
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = "".join(x for x in filename if x in valid_chars)
        file = open("text_files/"+filename, "w")
        file.write(run[item])

def main():
    id = "rwl2"
    schedule = "schedule"
    load_schedule(id, schedule)

main()