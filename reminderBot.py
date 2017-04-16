from telegram.ext import CommandHandler, Updater, Job, JobQueue
import datetime
# import logging

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

token = '334181320:AAGh2awo4I9MnxHc5GsRguRXUa5voMNI0Qs'
u = Updater(token=token)
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

weekdays = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}


def time2seconds(time):
	next_datetime = datetime.datetime.combine(datetime.date.today(), time)

	if datetime.datetime.now().time() > time:
		next_datetime += datetime.timedelta(days=1)

	next_t = (next_datetime - datetime.datetime.now()).total_seconds()

	return next_t


def callback_reminder_message(bot, job):
	print('alarm triggered')
	text = job.context['text']
	chat_id = job.context['chat_id']
	bot.sendMessage(chat_id=chat_id, text=text)

def callback_reminder_weekly(bot, update, job_queue, args):
	global weekdays

	dayStr = args[0].lower()
	day = weekdays[dayStr]

	print(day)

	timeArgs = map(int, args[1].split(':'))
	
	text = ' '.join(args[2:])

	job_context = {
					'text': text,
					'chat_id': update.message.chat_id
				  }
	time = datetime.time(*timeArgs)

	next_t = time2seconds(time)
	# print(datetime.datetime.now())

	interval = datetime.timedelta(weeks=1)
	print(interval)

	bot.sendMessage(chat_id=update.message.chat_id, text='Setting a reminder every '+dayStr.capitalize()+' @'+str(time)+' for: '+text)

	job_alarm = Job(callback_reminder_message, interval, repeat=True, context=job_context)
	print('created job')
	job_queue.put(job_alarm, next_t=next_t)
	print('put in queue')



def callback_stop_jobqueue(bot, update, job_queue):
	job_queue.stop()
	bot.sendMessage(chat_id=update.message.chat_id, text='Stopped jobqueue')

weekly_reminder_handler = CommandHandler('weekly', callback_reminder_weekly, pass_job_queue=True, pass_args=True)
u.dispatcher.add_handler(weekly_reminder_handler)

stop_handler = CommandHandler('stop', callback_stop_jobqueue, pass_job_queue=True)
u.dispatcher.add_handler(stop_handler)

u.start_polling()
print('started polling')
u.idle()
print('stopped')