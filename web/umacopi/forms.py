from django import forms



class MemberForm(forms.Form):
    first_name = forms.CharField(label= "名前")
    last_name = forms.CharField(label= "苗字")
    address = forms.CharField(label="住所")
    age = forms.IntegerField(label= "年齢")
    Mail = forms.EmailField(label="メールアドレス")





















# class SelectQuestionForm(forms.Form):
#     answers = forms.fields.ChoiceField(
#         choices = (
#             (1, 1),
#             (3, 3),
#             (5, 5),
#             (10, 10),
#             (20, 20),
#             (30, 30),
#             (40, 40),
#             (75, 75),
#             (999, 'ALL')
#         ),
#         initial=10,
#         required=False,
#         widget=forms.widgets.Select()
#     )
# <h2>会員登録フォーム</h2>
# <form class="" action="" method="post" enctype="multipart/form-data">
#     {% csrf_token %}
#     {{ form.as_p }}
#     <button type="submit" name="submit">Submit</button>
# </form>





