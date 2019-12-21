# Мы устроились на новую работу. Бывший сотрудник начал разрабатывать модуль для работы с почтой,
# но не успел доделать его. Код рабочий. Нужно только провести рефакторинг кода.
# Создать класс для работы с почтой;
# Создать методы для отправки и получения писем;
# Убрать "захардкоженный" код. Все значения должны определяться как аттрибуты класса, либо аргументы методов;
# Переменные должны быть названы по стандарту PEP8;
# Весь остальной код должен соответствовать стандарту PEP8;

# import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MyEmail:
    def __init__(self, smtp_server, imap_server, login, password):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.login = login
        self.password = password

    def send_message(self, subject, recipients, message, header):
        """
        Отправялем письмо
        :return:
        """
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header

        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))

        ms = smtplib.SMTP(self.smtp_server, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()

    def receive_message(self, folder, header):
        """
        Принимаем письмо
        :return:
        """
        self.folder = folder
        self.header = header
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.login, self.password)
        mail.list()
        mail.select(self.folder)
        self.criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, self.criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()


def main():
    example_message = MyEmail('smtp.gmail.com', 'imap.gmail.com', 'login@gmail.com', 'qwerty')
    # example_message.send_message('Subject', ['vasya@email.com', 'petya@email.com'], 'Message', None)
    example_message.receive_message("inbox", None)

if __name__ == '__main__':
    main()


