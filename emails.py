from app import MailingGroup

# emails = MailingGroup.query.all()
#
# for email in emails:
#     print(email.__dict__)


print(bool(MailingGroup.query.filter_by(mail='mark.lastovskyy@gmai.com').first()))