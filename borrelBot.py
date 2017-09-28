from telegram.ext import CommandHandler, Updater, Job, JobQueue
from telegram import User
import datetime


token = '363179481:AAGQpEzLZ5lQaTHM-XWbECzK1fLttCd96OU'
u = Updater(token=token)

weekdays = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
HARM = 18051322

def callback_reminder_message(bot, job):
	print('alarm triggered')
	text = job.context['text']
	chat_id = job.context['chat_id']
	bot.sendMessage(chat_id=chat_id, text=text)


def callback_start_barco(bot, update, job_queue):
	if update.message.from_user.id!= HARM:
		bot.sendMessage(chat_id=update.message.chat_id, text="You are not a bot admin")
	else:
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '9:00', 'Check of de fusten koud liggen!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '13:00', 'IJsmachine klaar zetten!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '17:00', 'Zijn alle fusten geteld?'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '21:25', 'Over 5 min laatste ronde!'])

def callback_start_viachat(bot, update, job_queue):
	if update.message.from_user.id!= HARM:
		bot.sendMessage(chat_id=update.message.chat_id, text="You are not a bot admin")
	else:
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '17:00', 'Het is tijd om te borrelen!!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '21:30', 'DE LAATSTE RONDE!!'])

def callback_start_test(bot, update, job_queue):
	# print(type(update.message.from_user.id))
	if update.message.from_user.id != HARM:
		bot.sendMessage(chat_id=update.message.chat_id, text="You are not a bot admin")
	else:
		print("Admin rights!")
		callback_reminder_weekly(bot, update, job_queue, ['tuesday', '15:35', 'TEST TEST TEST'])

def callback_reminder_weekly(bot, update, job_queue, args):
	if update.message.from_user.id!= HARM:
		bot.sendMessage(chat_id=update.message.chat_id, text="You are not a bot admin")
	else:
		global weekdays

		dayStr = args[0].lower()
		day = weekdays[dayStr]
		
		timeArgs = map(int, args[1].split(':'))
		time = datetime.time(*timeArgs)

		today = datetime.date.today()
		target_day = today + datetime.timedelta(days=(7 - today.weekday() + day) % 7)

		now =  datetime.datetime.now()
		dt = datetime.datetime.combine(target_day, time)
		next_t = (dt - now).total_seconds()

		text = ' '.join(args[2:])
		
		job_context = {
						'text': text,
						'chat_id': update.message.chat_id
					  }

		interval = datetime.timedelta(weeks=1)

		bot.sendMessage(chat_id=update.message.chat_id, text='Setting a reminder every '+
						dayStr.capitalize()+' @'+str(time)+'\nStarting: '+str(target_day)+'\nWith text: '+text)

		job_alarm = Job(callback_reminder_message, interval, repeat=True, context=job_context)
		job_queue.put(job_alarm, next_t=next_t)
		print('Added job to queue')



def callback_stop_jobqueue(bot, update, job_queue):
	job_queue.stop()
	bot.sendMessage(chat_id=update.message.chat_id, text='Stopped all jobs')


start_barco_handler = CommandHandler('startBarco', callback_start_barco, pass_job_queue=True)
u.dispatcher.add_handler(start_barco_handler)

start_viachat_handler = CommandHandler('startVia', callback_start_viachat, pass_job_queue=True)
u.dispatcher.add_handler(start_viachat_handler)

start_test_handler = CommandHandler('startTest', callback_start_test, pass_job_queue=True)
u.dispatcher.add_handler(start_test_handler)

weekly_reminder_handler = CommandHandler('weekly', callback_reminder_weekly, pass_job_queue=True, pass_args=True)
u.dispatcher.add_handler(weekly_reminder_handler)

stop_handler = CommandHandler('stop', callback_stop_jobqueue, pass_job_queue=True)
u.dispatcher.add_handler(stop_handler)

u.start_polling()
print('started polling')
u.idle()
print('stopped')
