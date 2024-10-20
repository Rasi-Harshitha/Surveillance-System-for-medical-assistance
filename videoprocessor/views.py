import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utils import FrameCapture, start_predictions
from collections import Counter

def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        fs = FileSystemStorage()
        video_path = fs.save(video.name, video)
        video_path = fs.url(video_path)

        # Process the video
        FrameCapture(os.path.join(settings.MEDIA_ROOT, video.name))
        lst = start_predictions()
        email='#########'
        from collections import Counter
        if len(lst)>0:
            c = Counter(lst)
            m = c.most_common(7)
            print("most common===", m)
            c1 = m[0]
            # c2 = m[1]
            c1 = c1[0]
            # c2 = c2[0]
            result = f"An unusual incident {c1} is detected in video"
        else:
            result=f"No unusual incident detected"
        try:
            send_mail_Notification(c1, email)
        except Exception as ex:
            print(ex)
            pass
           



        return render(request, 'index.html', {'video_url': video_path, 'results': result})
    return render(request, 'upload.html')
def send_mail_Notification(c1, email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    import geocoder
    g = geocoder.ip('me')
    l = g.latlng
    url = f'https://www.google.com/maps?q={l[0]},{l[1]}'

    mail_content = f"An unusual incident {c1} is detected in campus and its google map link {url}"
    # The mail addresses and password
    sender_address = '#####'
    sender_pass = '#######' # 'bagzgresybtfeqpf'
    receiver_address = email
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'Emergency required '  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
