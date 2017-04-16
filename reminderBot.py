from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue, Job
import datetime

token = "334181320:AAGh2awo4I9MnxHc5GsRguRXUa5voMNI0Qs"
updater = Updater(token=token)
dispatcher = updater.dispatcher
# jobs = updater.job_queue

print('Starting bot')

def test(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="TEST")

# def echo(bot, update):
# 	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def test_job(bot, job):
	print("Job started")
	bot.sendMessage(chat_id=job.context, text="text")

def reminder(bot, update, job_queue, args):
	print('hoi')
	# day = args[0]
	# time = args[1].split(":")
	# text = ' '.join(args[2:])

	# bot.sendMessage(chat_id=update.message.chat_id, text="Day: " + day)
	# bot.sendMessage(chat_id=update.message.chat_id, text='Time: ' + ':'.join(time))
	# bot.sendMessage(chat_id=update.message.chat_id, text='Message: ' + text)

	# print(time)
	# new_job = Job(test, days=(1))
	print(job_queue)
	time = datetime.time(15,10)
	print(time)
	dailyJob = job_queue.run_daily(test_job, time=time, context=update.message.chat_id)
	# job_queue.put(dailyJob)
	print('reminder set')



test_handler = CommandHandler('test', test)
dispatcher.add_handler(test_handler)

reminder_handler = CommandHandler('reminder', reminder, pass_job_queue=True, pass_args=True)
dispatcher.add_handler(reminder_handler)

# weekday = date.today().weekday()
# if weekday == 1:
# 	print(weekday)


updater.start_polling()
print('Started polling')

updater.idle()