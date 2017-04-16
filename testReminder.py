from telegram.ext import CommandHandler, Updater, Job, JobQueue
import datetime
# import logging

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

token = '334181320:AAGh2awo4I9MnxHc5GsRguRXUa5voMNI0Qs'
u = Updater(token=token)
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


def time2datetime(time):
	next_datetime = datetime.datetime.combine(datetime.date.today(), time)

	if datetime.datetime.now().time() > time:
		next_datetime += datetime.timedelta(days=1)

	next_t = (next_datetime - datetime.datetime.now()).total_seconds()

	return next_t


def callback_alarm(bot, job):
	print('alarm triggered')
	text = job.context['text']
	chat_id = job.context['chat_id']
	bot.sendMessage(chat_id=chat_id, text=text)

def callback_timer(bot, update, job_queue, args):
	timeArgs = map(int, args[0].split(':'))
	text = ' '.join(args[1:])

	job_context = {
					'text': text,
					'chat_id': update.message.chat_id
				  }
	time = datetime.time(*timeArgs)
	print(time)
	next_t = time2datetime(time)
	# print(datetime.datetime.now())

	interval = datetime.timedelta(weeks=1)
	print(interval)

	bot.sendMessage(chat_id=update.message.chat_id, text='Setting a timer @'+str(time))

	job_alarm = Job(callback_alarm, interval, repeat=True, context=job_context)
	print('created job')
	job_queue.put(job_alarm, next_t=next_t)
	print('put in queue')

def callback_stop_jobqueue(bot, update, job_queue):
	job_queue.stop()
	bot.sendMessage(chat_id=update.message.chat_id, text='Stopped jobqueue')

timer_handler = CommandHandler('timer', callback_timer, pass_job_queue=True, pass_args=True)
u.dispatcher.add_handler(timer_handler)

stop_handler = CommandHandler('stop', callback_stop_jobqueue, pass_job_queue=True)
u.dispatcher.add_handler(stop_handler)

u.start_polling()
print('started polling')
u.idle()
print('stopped')