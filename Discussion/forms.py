from django import forms


class DiscussionForm(forms.Form):
    title = forms.CharField(label='帖子标题', max_length=128)
    body = forms.CharField(label='帖子正文', max_length=1280, required=False)


class ReplyForm(forms.Form):
    body = forms.CharField(label='回复正文', max_length=1280)