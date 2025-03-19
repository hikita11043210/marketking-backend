from typing import List
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_email = 'hikita11043210@gmail.com'
        self.sender_password = 'skkd srpi mblx qbtc'
        
    def send_email_to_multiple_users(self, recipient_emails: List[str], subject: str, message: str) -> dict:
        """
        複数のメールアドレスにメールを送信する

        Args:
            recipient_emails (List[str]): 送信先メールアドレスのリスト
            subject (str): メールの件名
            message (str): メール本文

        Returns:
            dict: 送信結果の辞書
                {
                    'success': List[str],  # 送信成功したメールアドレスのリスト
                    'failed': List[str]    # 送信失敗したメールアドレスのリスト
                }
        """
        result = {
            'success': [],
            'failed': []
        }

        for recipient_email in recipient_emails:
            try:
                # メールメッセージの作成
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                # 本文の追加
                msg.attach(MIMEText(message, 'plain'))

                # SMTPサーバーへの接続とメール送信
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)

                result['success'].append(recipient_email)
            except Exception as e:
                print(f"Error sending email to {recipient_email}: {str(e)}")
                result['failed'].append(recipient_email)

        return result
