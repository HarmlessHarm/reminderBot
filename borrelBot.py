from telegram.ext import CommandHandler, Updater, Job, JobQueue
from telegram import User
import datetime


token = '363179481:AAGQpEzLZ5lQaTHM-XWbECzK1fLttCd96OU'
u = Updater(token=token)

weekdays = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
HARM = 18051322

def isAdmin(bot, update):
	if update.message.from_user.id != HARM:
		return False
	else:
		return True

def isBarco(bot, update):
	if update.message.chat_id == -234559880:
		return True
	return False

# Helper function to add reminders for barco chat
def callback_start_barco(bot, update, job_queue):
	if isAdmin(bot, update):
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '9:00', 'Check of de fusten koud liggen!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '13:00', 'IJsmachine klaar zetten!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '16:00', 'Set speciaalbier opties (/setSpeciaal <speciaalbier>)'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '17:00', 'Zijn alle fusten geteld?'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '21:25', 'Over 5 min laatste ronde!'])

# Helper function to add reminders for via chat
def callback_start_viachat(bot, update, job_queue):
	if isAdmin(bot, update):
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '17:00', 'Het is tijd om te borrelen!!'])
		callback_reminder_weekly(bot, update, job_queue, ['thursday', '21:30', 'DE LAATSTE RONDE!!'])

# Test helper funciton
def callback_start_test(bot, update, job_queue):
	if isAdmin(bot, update):
		callback_reminder_weekly(bot, update, job_queue, ['tuesday', '15:35', 'TEST TEST TEST'])

def callback_set_speciaalbier(bot, update, args):
	if isBarco(bot, update) or isAdmin(bot, update):
		with open('speciaalbier', 'w') as f:
			text = ' '.join(args)
			f.write(text)
			print(update.message.chat_id)
			bot.sendMessage(chat_id=update.message.chat_id, text='Set speciaalbier to: '+text)


# Main function to set a weekly reminder
def callback_reminder_weekly(bot, update, job_queue, args):
	if isAdmin(bot, update):
		global weekdays

		# Extract Weekday from args
		dayStr = args[0].lower()
		day = weekdays[dayStr]
		
		# Extract Time from args
		timeArgs = map(int, args[1].split(':'))
		time = datetime.time(*timeArgs)

		# Calculates target day
		today = datetime.date.today()
		target_day = today + datetime.timedelta(days=(7 - today.weekday() + day) % 7)

		# Calculates target time
		now =  datetime.datetime.now()
		dt = datetime.datetime.combine(target_day, time)
		next_t = (dt - now).total_seconds()

		# Extracts message from args
		text = ' '.join(args[2:])
		
		job_context = {
						'text': text,
						'chat_id': update.message.chat_id
					  }

		interval = datetime.timedelta(weeks=1)

		# Sends message to chat with info about reminder
		bot.sendMessage(chat_id=update.message.chat_id, text='Setting a reminder every '+
						dayStr.capitalize()+' @'+str(time)+'\nStarting: '+str(target_day)+'\nWith text: '+text)

		# Creates Job and adds to jobqueue
		job_alarm = Job(callback_reminder_message, interval, repeat=True, context=job_context)
		job_queue.put(job_alarm, next_t=next_t)
		print('Added job to queue')

# Sends message to chat
def callback_reminder_message(bot, job):
	text = job.context['text']
	chat_id = job.context['chat_id']
	bot.sendMessage(chat_id=chat_id, text=text)

# Remove all jobs in queue
def callback_stop_jobqueue(bot, update, job_queue):
	if isAdmin(bot, update):
		job_queue.stop()
		bot.sendMessage(chat_id=update.message.chat_id, text='Stopped all jobs')

def callback_get_chatinfo(bot, update):
	if isAdmin(bot, update):
		text = '''
			chat_id = %s
		'''
		bot.sendMessage(chat_id=update.message.chat_id, text=text)


start_barco_handler = CommandHandler('startBarco', callback_start_barco, pass_job_queue=True)
u.dispatcher.add_handler(start_barco_handler)

start_viachat_handler = CommandHandler('startVia', callback_start_viachat, pass_job_queue=True)
u.dispatcher.add_handler(start_viachat_handler)

start_test_handler = CommandHandler('startTest', callback_start_test, pass_job_queue=True)
u.dispatcher.add_handler(start_test_handler)

set_speciaalbier_handler = CommandHandler('setSpeciaal', callback_set_speciaalbier, pass_args=True)
u.dispatcher.add_handler(set_speciaalbier_handler)

get_chatinfo_handler = CommandHandler('getInfo', callback_get_chatinfo)
u.dispatcher.add_handler(get_chatinfo_handler)

# weekly_reminder_handler = CommandHandler('weekly', callback_reminder_weekly, pass_job_queue=True, pass_args=True)
# u.dispatcher.add_handler(weekly_reminder_handler)

stop_handler = CommandHandler('stop', callback_stop_jobqueue, pass_job_queue=True)
u.dispatcher.add_handler(stop_handler)

u.start_polling()
print('started polling')
u.idle()
print('stopped')
