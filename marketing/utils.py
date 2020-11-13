import hashlib
import re

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

from ecomm.settings import MAILCHIMP_API_KEY, MAILCHIMP_DATA_CENTER, MAILCHIMP_EMAIL_LIST_ID


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError("String passed is not a valid email address.")
    return email


def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": MAILCHIMP_API_KEY,
            "server": MAILCHIMP_DATA_CENTER
        })
        self.list_id = MAILCHIMP_EMAIL_LIST_ID

    def check_subscription_status(self, email):
        try:
            hashed_email = get_subscriber_hash(email)
            r = self.client.lists.get_list_member(MAILCHIMP_EMAIL_LIST_ID, hashed_email)
            return r.get("status")
        except ApiClientError as error:
            print("Error(check_subscription_status) : {}".format(error.text))
            return None

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError("Not a valid choice for email status")
        return status

    def add_or_update_email(self, email, status="subscribed"):
        try:
            status = self.check_valid_status(status)
            current_status = self.check_subscription_status(email)
            data = {
                "email_address": email,
                "status_if_new": "subscribed",
                "status": status
            }
            if current_status:
                r = self.client.lists.update_list_member(self.list_id, email, data)
            else:
                r = self.client.lists.add_list_member(self.list_id, email)
            return r
        except ValueError:
            return "Not Valid Email Address"
        except ApiClientError as error:
            print("Error(add_or_update_email): {}".format(error.text))

    def unsubscribe(self, email):
        return self.add_or_update_email(email, status="unsubscribed")

    def subscribe(self, email):
        return self.add_or_update_email(email, status="subscribed")

    def pending(self, email):
        return self.add_or_update_email(email, status="pending")
