from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# ユーザー登フォーム
# UserCreationForm:User作成に特化したForm(厳密にはModelForm)
class SignupForm(UserCreationForm):
    """
    Formが受け取った情報を本クラスに保存するわけではない。
    Formが受け取った情報をmodelに保存する形
    Formと直接的に関わる情報ではないため Meta クラスを使用
    """

    class Meta:
        model = User
        fields = ("username",)
