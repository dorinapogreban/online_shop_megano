# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
#
#
# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password', 'avatar']
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
#             raise ValidationError('This email address is already in use.')
#         return email
#
#     def clean_avatar(self):
#         avatar = self.cleaned_data.get('avatar', False)
#         if avatar and avatar.size > 2 * 1024 * 1024:
#             raise ValidationError('The avatar size should not exceed 2 MB.')
#         return avatar
